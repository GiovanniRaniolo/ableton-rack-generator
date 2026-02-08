import Stripe from 'stripe';
import { currentUser } from '@clerk/nextjs/server';
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
  try {
    const user = await currentUser();
    
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { priceId } = await req.json();

    // Validate price ID
    const validPrices = [
      process.env.STRIPE_PRICE_PRO,
      process.env.STRIPE_PRICE_STARTER,
      process.env.STRIPE_PRICE_POWER,
    ];

    // Debug logging
    console.log('[Checkout API] Received priceId:', priceId);
    console.log('[Checkout API] Valid prices:', validPrices);
    console.log('[Checkout API] Is valid?', validPrices.includes(priceId));

    if (!validPrices.includes(priceId)) {
      return NextResponse.json(
        { error: 'Invalid price ID' },
        { status: 400 }
      );
    }

    // Get or create Stripe customer
    const { data: profile } = await supabase
      .from('profiles')
      .select('stripe_customer_id')
      .eq('id', user.id)
      .single();

    let customerId = profile?.stripe_customer_id;

    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.emailAddresses[0].emailAddress,
        metadata: { userId: user.id },
      });
      customerId = customer.id;

      await supabase
        .from('profiles')
        .update({ stripe_customer_id: customerId })
        .eq('id', user.id);
    }

    // Determine mode based on price ID
    const mode = priceId === process.env.STRIPE_PRICE_PRO ? 'subscription' : 'payment';

    // Create checkout session
    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      client_reference_id: user.id,
      line_items: [{ price: priceId, quantity: 1 }],
      mode,
      success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard/settings?payment=success`,
      cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing?payment=cancelled`,
      metadata: {
        userId: user.id,
        priceId,
      },
    });

    return NextResponse.json({ url: session.url });
  } catch (error: any) {
    console.error('[Checkout API] Error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}
