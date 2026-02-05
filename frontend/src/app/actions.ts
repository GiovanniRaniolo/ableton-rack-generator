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

    // 3. Deduct Credit (Only on Success)
    const { error: updateError } = await supabase
      .from('profiles')
      .update({ credits: profile.credits - 1 })
      .eq('id', user.id);

    if (updateError) {
      console.error("Failed to deduct credit:", updateError);
      // Optional: rollback or log critical error
    }

    return { success: true, data: rackData, remainingCredits: profile.credits - 1 };

  } catch (err: any) {
    return { success: false, error: err.message || "Backend Error" };
  }
}
