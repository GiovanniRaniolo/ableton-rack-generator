'use server'

import { auth, currentUser } from "@clerk/nextjs/server";
import { createClient } from "@supabase/supabase-js";
import { createHash } from 'crypto'; // Node.js built-in
import { LAUNCH_BONUS_CONFIG, isBonusActive } from '@/config/launch-bonus';

export async function syncUserProfile() {
  const user = await currentUser();
  if (!user) return { success: false, error: "Not logged in" };

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  // Get primary email (Clerk normalizes this across providers)
  const primaryEmail = user.emailAddresses.find(e => e.id === user.primaryEmailAddressId)?.emailAddress;
  if (!primaryEmail) return { success: false, error: "No email found" };

  const emailHash = createHash('sha256').update(primaryEmail.toLowerCase()).digest('hex');

  // Check if profile exists by Clerk ID (including soft-deleted ones)
  const { data, error } = await supabase
    .from('profiles')
    .select('id, credits, is_pro, bonus_credits_awarded, deleted_at, created_at, stripe_subscription_id')
    .eq('id', user.id)
    .single();

  if (!data) {
    // NEW USER CREATION LOGIC
    
    // 🔒 SECURITY LAYER 2: Multi-Provider Check
    // Has this email already claimed credits under a DIFFERENT Clerk ID?
    const { data: existingEmailClaim } = await supabase
      .from('bonus_claims')
      .select('user_id, claimed_at')
      .eq('email_hash', emailHash)
      .single();

    if (existingEmailClaim && existingEmailClaim.user_id !== user.id) {
      // FRAUD DETECTED: Same email, different Clerk ID
      console.error(`⚠️ MULTI-PROVIDER FRAUD: User ${user.id} tried to claim credits with email already used by ${existingEmailClaim.user_id}`);
      
      return { 
        success: false, 
        error: "This email has already been used to claim credits. If you believe this is an error, please contact support.",
        fraudDetected: true
      };
    }
    
    // 1. Determine credits to award
    let creditsToAward: number = LAUNCH_BONUS_CONFIG.STANDARD_CREDITS; // Default: 5
    let bonusAwarded = 0;
    
    // 2. Check if bonus is active
    if (isBonusActive()) {
      // 3. 🔒 SECURITY LAYER 1: Email Hash Check (re-registration prevention)
      // Has this email already claimed the bonus?
      if (!existingEmailClaim) {
        // Email has NOT claimed bonus before → Award it!
        creditsToAward = LAUNCH_BONUS_CONFIG.BONUS_CREDITS; // 10
        bonusAwarded = LAUNCH_BONUS_CONFIG.BONUS_EXTRA; // 5
        
        // 4. Record the claim (prevents future abuse)
        await supabase.from('bonus_claims').insert({
          email_hash: emailHash,
          user_id: user.id,
          bonus_type: LAUNCH_BONUS_CONFIG.BONUS_TYPE,
        });
      } else {
        console.warn(`User ${user.id} attempted to re-claim bonus with email hash ${emailHash.substring(0, 8)}...`);
      }
    }
    
    // 5. Create profile with calculated credits
    const { error: createError } = await supabase
      .from('profiles')
      .insert({
        id: user.id,
        email: primaryEmail,
        credits: creditsToAward,
        is_pro: false,
        bonus_credits_awarded: bonusAwarded,
        deleted_at: null // Explicitly active
      });
    
    if (createError) {
      console.error('Profile creation error:', createError);
      return { success: false, error: 'Failed to create profile' };
    }
    
    return { 
      success: true, 
      credits: creditsToAward, 
      is_pro: false, 
      created: true,
      bonusAwarded: bonusAwarded > 0, // For frontend notification
      stripe_subscription_id: null
    };
  }
  
  // Profile exists - check if it was soft-deleted
  if (data.deleted_at) {
    // 🔒 SECURITY LAYER 3: Re-activation Rules
    // USER RE-REGISTERING AFTER DELETION
    
    const deletedDate = new Date(data.deleted_at);
    const now = new Date();
    const daysSinceDeletion = (now.getTime() - deletedDate.getTime()) / (1000 * 60 * 60 * 24);
    
    // RULE: Must wait 30 days before re-activating account
    if (daysSinceDeletion < 30) {
      return { 
        success: false, 
        error: `Your account was deleted ${Math.floor(daysSinceDeletion)} days ago. You can re-activate it after 30 days from deletion.`,
        daysRemaining: Math.ceil(30 - daysSinceDeletion),
        canReactivateAt: new Date(deletedDate.getTime() + (30 * 24 * 60 * 60 * 1000)).toISOString()
      };
    }
    
    // Re-activate account with SAME credits (no new credits!)
    await supabase
      .from('profiles')
      .update({ 
        deleted_at: null, // Re-activate
        deletion_reason: null 
      })
      .eq('id', user.id);
    
    return { 
      success: true, 
      credits: data.credits, // SAME credits as before deletion
      is_pro: data.is_pro,
      created: false,
      reactivated: true,
      message: "Welcome back! Your account has been re-activated with your previous credits.",
      stripe_subscription_id: data.stripe_subscription_id || null
    };
  }

  // Normal active user
  return { 
    success: true, 
    credits: data.credits, 
    is_pro: data.is_pro, 
    created: false,
    bonusAwarded: false,
    stripe_subscription_id: data.stripe_subscription_id || null
  };
}

export async function generateRackAction(prompt: string) {
  const user = await currentUser();
  if (!user) return { success: false, error: "Unauthorized" };

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  // 1. Check Credits
  const { data: profile } = await supabase
    .from('profiles')
    .select('credits')
    .eq('id', user.id)
    .single();

  if (!profile || profile.credits < 1) {
    return { success: false, error: "Insufficient credits. Please top up." };
  }

    // 2. Call Python Backend (Server-to-Server)
    try {
      const backendUrl = "http://127.0.0.1:8000"; // Local Python
    const res = await fetch(`${backendUrl}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Generation failed');
    }

    const rackData = await res.json();
    const filename = rackData.filename;

    // 3. Fetch the actual file content from Python
    const fileRes = await fetch(`${backendUrl}/download/${filename}`);
    if (!fileRes.ok) throw new Error("Failed to retrieve generated file");
    const fileBuffer = await fileRes.arrayBuffer();

    // 4. Upload to Supabase Storage
    const { error: uploadError } = await supabase.storage
      .from('racks')
      .upload(filename, fileBuffer, {
        contentType: 'application/octet-stream',
        upsert: false
      });

    if (uploadError) throw new Error(`Storage Error: ${uploadError.message}`);

    // 5. Get Public URL
    const { data: { publicUrl } } = supabase.storage
      .from('racks')
      .getPublicUrl(filename);

    // 6. Save Metadata to DB & Deduct Credit
    // We strive for atomicity but Supabase doesn't support easy multi-table transactions via JS client yet without RPC.
    // We'll update credits first (already checked > 0).
    
    const { error: dbError } = await supabase
      .from('generations')
      .insert({
        user_id: user.id,
        prompt: prompt,
        creative_name: rackData.creative_name,
        filename: filename,
        file_url: publicUrl,
        rack_data: rackData
      });

    if (dbError) throw new Error(`History Error: ${dbError.message}`);

    const { error: creditError } = await supabase
        .from('profiles')
        .update({ credits: profile.credits - 1 })
        .eq('id', user.id);
        
    if (creditError) console.error("Credit Deduction failed but file generated", creditError);

    // Return extended data including the cloud URL
    return { 
        success: true, 
        data: { ...rackData, file_url: publicUrl }, 
        remainingCredits: profile.credits - 1 
    };

  } catch (err: any) {
    console.error("Action Error:", err);
    return { success: false, error: err.message || "Backend Error" };
  }
}

export async function getUserLibrary() {
  const user = await currentUser();
  if (!user) return [];

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  const { data, error } = await supabase
    .from('generations')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false });

  if (error) {
    console.error("Library Fetch Error:", error);
    return [];
  }

  return data;
}
