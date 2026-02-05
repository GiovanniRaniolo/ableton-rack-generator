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
