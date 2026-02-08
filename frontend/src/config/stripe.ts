// Stripe Price IDs Configuration
// These are PUBLIC and safe to expose in client-side code

export const STRIPE_PRICES = {
  PRO: process.env.NEXT_PUBLIC_STRIPE_PRICE_PRO!,
  STARTER: process.env.NEXT_PUBLIC_STRIPE_PRICE_STARTER!,
  POWER: process.env.NEXT_PUBLIC_STRIPE_PRICE_POWER!,
} as const;

// Validate that all price IDs are set
if (typeof window === 'undefined') {
  // Server-side validation only
  const missing = Object.entries(STRIPE_PRICES)
    .filter(([_, value]) => !value)
    .map(([key]) => key);
  
  if (missing.length > 0) {
    console.warn(`Missing Stripe Price IDs: ${missing.join(', ')}`);
  }
}
