"use client";

import { useEffect } from "react";
import { syncUserProfile } from "@/app/actions";

export function ProfileSyncProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    console.log("🔄 ProfileSyncProvider mounted - syncing user profile...");
    
    // Automatically sync profile on mount (first dashboard visit after login)
    syncUserProfile()
      .then(result => {
        console.log("✅ Profile sync result:", result);
      })
      .catch(err => {
        console.error("❌ Failed to sync user profile:", err);
      });
  }, []);

  return <>{children}</>;
}
