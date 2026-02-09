-- Helper script to manually test credit updates after Stripe checkout
-- Run this in Supabase SQL Editor after completing a test payment

-- 1. View recent transactions (to verify webhook would have worked)
SELECT 
  id,
  user_id,
  amount,
  currency,
  status,
  type,
  credits_awarded,
  created_at
FROM transactions
ORDER BY created_at DESC
LIMIT 10;

-- 2. Manually add credits to a user (for testing without webhook)
-- Replace 'user_xxx' with your Clerk user ID
SELECT add_credits('user_xxx', 20); -- For Starter Pack
-- SELECT add_credits('user_xxx', 40); -- For Power Pack
-- SELECT add_credits('user_xxx', 80); -- For Pro Subscription

-- 3. Manually activate Pro subscription (for testing without webhook)
-- Replace 'user_xxx' with your Clerk user ID
UPDATE profiles
SET 
  is_pro = true,
  credits = 80,
  subscription_status = 'active',
  subscription_current_period_end = NOW() + INTERVAL '30 days'
WHERE id = 'user_xxx';

-- 4. View user profile to verify changes
SELECT 
  id,
  email,
  credits,
  is_pro,
  subscription_status,
  stripe_customer_id,
  stripe_subscription_id
FROM profiles
WHERE id = 'user_xxx';

-- 5. Check if Stripe customer was created
SELECT 
  id,
  email,
  stripe_customer_id,
  created_at
FROM profiles
WHERE stripe_customer_id IS NOT NULL
ORDER BY created_at DESC
LIMIT 5;
