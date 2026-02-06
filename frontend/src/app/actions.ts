'use server'

import { auth, currentUser } from "@clerk/nextjs/server";
import { createClient } from "@supabase/supabase-js";

export async function syncUserProfile() {
  const user = await currentUser();
  if (!user) return { success: false, error: "Not logged in" };

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );

  // Check if profile exists
  const { data, error } = await supabase
    .from('profiles')
    .select('id, credits')
    .eq('id', user.id)
    .single();

  if (!data) {
    // Create Profile
    const email = user.emailAddresses[0]?.emailAddress;
    const { error: insertError } = await supabase
      .from('profiles')
      .insert({
        id: user.id,
        email: email,
        credits: 3, // Default Free Credits
        is_pro: false
      });
      
    if (insertError) {
        console.error("Sync Error:", insertError);
        return { success: false, error: insertError.message };
    }
    return { success: true, credits: 3, created: true };
  }

  return { success: true, credits: data.credits, created: false };
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
