"use client";

import { motion } from "framer-motion";
import { Check, Sparkles, Zap, Shield, HelpCircle, ExternalLink, ArrowLeft, CreditCard, Box, Home, Crown } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { syncUserProfile } from "@/app/actions";
import { STRIPE_PRICES } from "@/config/stripe";
import { useSearchParams } from "next/navigation";

const PACKS = [
  {
    id: "starter",
    name: "Starter Pack",
    price: "€2.90",
    credits: 20,
    reset: "Never Expires",
    idealFor: "Emergency Top-up",
  },
  {
    id: "power",
    name: "Power Pack",
    price: "€4.90",
    credits: 40,
    reset: "Never Expires",
    idealFor: "Casual Use",
  }
];

export default function SettingsPage() {
  const [isPro, setIsPro] = useState<boolean | null>(null);
  const [credits, setCredits] = useState<number>(0);
  const [loading, setLoading] = useState<string | null>(null);
  const searchParams = useSearchParams();
  const paymentStatus = searchParams.get('payment');

  useEffect(() => {
    syncUserProfile().then(res => {
        if (res.success) {
             setIsPro(res.is_pro || false);
             setCredits(res.credits || 0);
        } else {
             setIsPro(false);
             setCredits(0);
        }
    });
  }, []);

  async function handleCheckout(priceId: string, packId: string) {
    setLoading(packId);
    
    try {
      const res = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId }),
      });

      const data = await res.json();

      if (!res.ok || data.error) {
        alert(`Error: ${data.error || 'Failed to start checkout'}`);
        return;
      }

      window.location.href = data.url;
    } catch (error) {
      console.error('Checkout error:', error);
      alert('Failed to start checkout. Please try again.');
    } finally {
      setLoading(null);
    }
  }

  if (isPro === null) {
      return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-accent-primary border-t-transparent rounded-full animate-spin" />
        </div>
      );
  }

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-6xl mx-auto space-y-12 pb-6">
      
      {/* Header with Navigation */}
      <div className="space-y-6 animate-in fade-in slide-in-from-top-4 duration-700">
        <Link 
          href="/" 
          className="inline-flex items-center gap-2 text-text-dim hover:text-white transition-colors group"
        >
          <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          <span className="text-sm font-medium">Back to Home</span>
        </Link>
        
        <div>
          <h1 className="text-4xl font-black text-white tracking-tight">Account Settings</h1>
          <p className="text-text-dim text-lg max-w-2xl mt-2">
            Manage your subscription, credits, and billing preferences.
          </p>
        </div>
      </div>

      {/* Payment Status Notification */}
      {paymentStatus === 'success' && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-accent-success/10 border border-accent-success/30 rounded-xl p-4 flex items-center gap-3"
        >
          <Check className="w-5 h-5 text-accent-success" />
          <div>
            <p className="font-bold text-white">Payment Successful!</p>
            <p className="text-sm text-text-dim">Your credits will be added shortly.</p>
          </div>
        </motion.div>
      )}

      {paymentStatus === 'cancelled' && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-3"
        >
          <ExternalLink className="w-5 h-5 text-red-400" />
          <div>
            <p className="font-bold text-white">Payment Cancelled</p>
            <p className="text-sm text-text-dim">You can try again anytime.</p>
          </div>
        </motion.div>
      )}

      {/* Current Plan Status */}
      <section className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        <div className="flex items-center gap-2 text-accent-primary">
            <Zap className="w-5 h-5" />
            <h2 className="text-xl font-bold uppercase tracking-wider text-white">Your Current Plan</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Plan Card */}
          <motion.div 
            whileHover={{ y: -5 }}
            className={cn(
              "relative p-8 rounded-3xl border flex flex-col gap-6 overflow-hidden",
              isPro
                ? "bg-[#0f0f10] border-accent-primary/50 shadow-[0_0_40px_-10px_rgba(255,124,37,0.15)]" 
                : "bg-[#0a0a0b] border-white/10"
            )}
          >
            <div className="absolute top-0 right-0 bg-accent-success/20 text-accent-success text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-bl-xl flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-accent-success animate-pulse"/>
              Active
            </div>

            <div className="space-y-2">
              <div className="flex items-center gap-2">
                {isPro && <Crown className="w-5 h-5 text-accent-primary" />}
                <h3 className="text-2xl font-bold text-white">
                  {isPro ? "Pro Plan" : "Free Tier"}
                </h3>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-black text-white">
                  {isPro ? "€5.90" : "€0"}
                </span>
                <span className="text-text-dim">/mo</span>
              </div>
              <p className="text-sm text-text-dim">
                {isPro ? "Active Production" : "Curiosity"}
              </p>
            </div>

            <div className="py-6 border-t border-white/5">
              <ul className="space-y-2">
                <li className="flex items-center gap-2 text-sm text-text-dim">
                  <Check className="w-4 h-4 text-accent-success" />
                  {isPro ? "Priority Generation" : "Standard Generation"}
                </li>
                <li className="flex items-center gap-2 text-sm text-text-dim">
                  <Check className="w-4 h-4 text-accent-success" />
                  {isPro ? "Priority Support" : "Community Support"}
                </li>
                {isPro && (
                  <li className="flex items-center gap-2 text-sm text-text-dim">
                    <Check className="w-4 h-4 text-accent-success" />
                    Commercial License
                  </li>
                )}
              </ul>
            </div>

            {!isPro ? (
              <Link href="/pricing" className="w-full">
                <button className="w-full py-4 rounded-xl bg-white text-black font-black uppercase tracking-widest text-xs hover:scale-[1.02] shadow-lg transition-all flex items-center justify-center gap-2">
                  Upgrade to Pro
                  <Sparkles className="w-4 h-4" />
                </button>
              </Link>
            ) : (
              <button className="w-full py-4 rounded-xl bg-white/5 hover:bg-white/10 text-white font-bold uppercase tracking-widest text-xs transition-all flex items-center justify-center gap-2">
                Manage Billing
                <CreditCard className="w-4 h-4" />
              </button>
            )}
          </motion.div>

          {/* Credits Card */}
          <motion.div 
            whileHover={{ y: -5 }}
            className="relative p-8 rounded-3xl border border-white/10 bg-[#0a0a0b] flex flex-col gap-6"
          >
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-accent-primary" />
                <h3 className="text-2xl font-bold text-white">Credits</h3>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-5xl font-black text-white">{credits}</span>
                <span className="text-text-dim text-lg">available</span>
              </div>
              <p className="text-xs text-text-dim bg-white/5 px-2 py-1 rounded-md inline-block">
                Resets every 30 days
              </p>
            </div>

            <div className="py-6 border-t border-white/5 flex-1">
              <p className="text-sm text-text-dim">
                {isPro 
                  ? "Your credits reset monthly with your Pro subscription." 
                  : "Need more credits? Upgrade to Pro for 80 credits/month or buy a one-time pack below."}
              </p>
            </div>

            <Link href="/pricing" className="w-full">
              <button className="w-full py-4 rounded-xl bg-accent-primary/10 hover:bg-accent-primary/20 border-2 border-accent-primary/30 text-white font-bold uppercase tracking-widest text-xs transition-all flex items-center justify-center gap-2">
                Buy More Credits
                <Box className="w-4 h-4" />
              </button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Credit Packs Section - Simplified */}
      <section className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-accent-secondary">
              <Box className="w-5 h-5" />
              <h2 className="text-xl font-bold uppercase tracking-wider text-white">Need More Credits?</h2>
          </div>
          <Link href="/pricing" className="text-sm text-accent-primary hover:text-white transition-colors flex items-center gap-1">
            View all plans
            <ExternalLink className="w-3 h-3" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {PACKS.map((pack) => (
                <motion.div 
                    key={pack.id}
                    whileHover={{ y: -5 }}
                    className="relative p-6 rounded-2xl border border-white/10 bg-[#0a0a0b] flex flex-col gap-4"
                >
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-lg font-bold text-white">{pack.name}</h3>
                        <p className="text-xs text-text-dim">{pack.idealFor}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-black text-white">{pack.price}</div>
                        <div className="text-xs text-text-dim">{pack.credits} credits</div>
                      </div>
                    </div>

                    <div className="text-xs text-accent-success bg-accent-success/10 px-2 py-1 rounded-md inline-block self-start">
                      {pack.reset}
                    </div>

                    <button 
                        onClick={() => handleCheckout(
                          pack.id === 'starter' ? STRIPE_PRICES.STARTER : STRIPE_PRICES.POWER,
                          pack.id
                        )}
                        disabled={loading === pack.id}
                        className="w-full py-3 rounded-xl bg-white text-black font-bold uppercase tracking-widest text-xs hover:scale-[1.02] shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading === pack.id ? 'Loading...' : 'Buy Pack'}
                    </button>
                </motion.div>
            ))}
        </div>

        {!isPro && (
          <div className="text-center p-6 bg-white/5 rounded-xl border border-white/10">
            <p className="text-text-dim mb-3">
              Or upgrade to <span className="text-accent-primary font-bold">Pro</span> for 80 credits every month
            </p>
            <Link href="/pricing">
              <button className="px-6 py-3 rounded-xl bg-accent-primary text-black font-bold uppercase tracking-widest text-xs hover:scale-[1.02] shadow-lg transition-all inline-flex items-center gap-2">
                View Pro Plan
                <ArrowLeft className="w-4 h-4 rotate-180" />
              </button>
            </Link>
          </div>
        )}
      </section>
    </div>
  );
}
