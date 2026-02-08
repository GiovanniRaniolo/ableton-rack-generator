// frontend/src/config/launch-bonus.ts

/**
 * Launch Bonus Configuration
 * 
 * IMPORTANT: Change LAUNCH_DEADLINE_UTC to extend/end the promotion
 */

export const LAUNCH_BONUS_CONFIG = {
  // Deadline (UTC timestamp)
  // Current: 15 days from 2026-02-08 18:00 UTC
  LAUNCH_DEADLINE_UTC: new Date('2026-02-23T18:00:00Z').getTime(),
  
  // Bonus amount (REDUCED to mitigate multi-account abuse)
  STANDARD_CREDITS: 5 as const,  // Free tier (no bonus)
  BONUS_CREDITS: 10 as const,    // Launch bonus
  BONUS_EXTRA: 5 as const,       // Difference
  
  // Feature flags
  ENABLED: true, // Set to false to disable bonus globally
  SHOW_COUNTDOWN: true, // Show countdown timer in CTA
  
  // Analytics
  BONUS_TYPE: 'launch_10' as const,
} as const;

/**
 * Check if bonus is currently active
 */
export function isBonusActive(): boolean {
  if (!LAUNCH_BONUS_CONFIG.ENABLED) return false;
  return Date.now() < LAUNCH_BONUS_CONFIG.LAUNCH_DEADLINE_UTC;
}

/**
 * Get time remaining in milliseconds
 */
export function getBonusTimeRemaining(): number {
  const remaining = LAUNCH_BONUS_CONFIG.LAUNCH_DEADLINE_UTC - Date.now();
  return Math.max(0, remaining);
}

/**
 * Format time remaining as "47h 23m 15s"
 */
export function formatTimeRemaining(): string {
  const ms = getBonusTimeRemaining();
  if (ms === 0) return 'Expired';
  
  const hours = Math.floor(ms / (1000 * 60 * 60));
  const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((ms % (1000 * 60)) / 1000);
  
  return `${hours}h ${minutes}m ${seconds}s`;
}
