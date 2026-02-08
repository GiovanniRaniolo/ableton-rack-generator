import Stripe from 'stripe';
import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-11-20.acacia',
});

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get('stripe-signature');

  if (!sig) {
    return NextResponse.json(
      { error: 'Missing stripe-signature header' },
      { status: 400 }
    );
  }

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err: any) {
    console.error('[Webhook] Signature verification failed:', err.message);
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    );
  }

  console.log(`[Webhook] Received event: ${event.type}`);

  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session);
        break;

      case 'customer.subscription.created':
      case 'customer.subscription.updated':
      case 'customer.subscription.deleted':
        await handleSubscriptionChange(event.data.object as Stripe.Subscription);
        break;

      case 'invoice.payment_succeeded':
        await handleInvoicePaymentSucceeded(event.data.object as Stripe.Invoice);
        break;

      case 'invoice.payment_failed':
        await handleInvoicePaymentFailed(event.data.object as Stripe.Invoice);
        break;

      default:
        console.log(`[Webhook] Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error: any) {
    console.error(`[Webhook] Error processing ${event.type}:`, error);
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const userId = session.metadata?.userId || session.client_reference_id;
  
  if (!userId) {
    console.error('[Webhook] No userId in session metadata');
    return;
  }

  const priceId = session.metadata?.priceId;

  if (session.mode === 'subscription') {
    // Pro subscription
    const subscription = await stripe.subscriptions.retrieve(session.subscription as string);
    
    await supabase
      .from('profiles')
      .update({
        is_pro: true,
        credits: 80,
        stripe_subscription_id: subscription.id,
        subscription_status: subscription.status,
        subscription_current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
      })
      .eq('id', userId);

    console.log(`[Webhook] Activated Pro subscription for user ${userId}`);
  } else {
    // One-time credit pack
    let credits = 0;

    if (priceId === process.env.STRIPE_PRICE_STARTER) {
      credits = 20;
    } else if (priceId === process.env.STRIPE_PRICE_POWER) {
      credits = 40;
    }

    if (credits > 0) {
      // Add credits using RPC function
      await supabase.rpc('add_credits', { 
        user_id: userId, 
        amount: credits 
      });

      console.log(`[Webhook] Added ${credits} credits to user ${userId}`);
    }
  }

  // Record transaction
  await supabase.from('transactions').insert({
    user_id: userId,
    stripe_payment_intent_id: session.payment_intent as string,
    amount: session.amount_total!,
    currency: session.currency!,
    status: 'succeeded',
    type: session.mode === 'subscription' ? 'subscription' : 'one_time',
    credits_awarded: session.mode === 'payment' ? 
      (priceId === process.env.STRIPE_PRICE_STARTER ? 20 : 40) : 80,
    metadata: session.metadata as any,
  });
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  const userId = subscription.metadata.userId;
  
  if (!userId) {
    console.error('[Webhook] No userId in subscription metadata');
    return;
  }

  const isActive = subscription.status === 'active';

  await supabase
    .from('profiles')
    .update({
      is_pro: isActive,
      subscription_status: subscription.status,
      subscription_current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
    })
    .eq('id', userId);

  console.log(`[Webhook] Updated subscription status to ${subscription.status} for user ${userId}`);
}

async function handleInvoicePaymentSucceeded(invoice: Stripe.Invoice) {
  console.log(`[Webhook] Invoice paid successfully: ${invoice.id}`);
  
  // For subscription renewals, credits are already set by subscription handler
  // Just log the successful payment
}

async function handleInvoicePaymentFailed(invoice: Stripe.Invoice) {
  const subscriptionId = invoice.subscription as string;
  
  if (!subscriptionId) return;

  const subscription = await stripe.subscriptions.retrieve(subscriptionId);
  const userId = subscription.metadata.userId;

  if (!userId) return;

  // Mark subscription as past_due
  await supabase
    .from('profiles')
    .update({ subscription_status: 'past_due' })
    .eq('id', userId);

  console.log(`[Webhook] Payment failed for user ${userId}`);
}
