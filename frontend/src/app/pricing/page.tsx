"use client";

import { useState, useEffect } from "react";
import { Navbar } from "@/components/landing/Navbar";
import { Footer } from "@/components/landing/Footer";
import { motion } from "framer-motion";
import { Check, Zap, Sparkles, Clock, Box, Gift } from "lucide-react";
import { SignInButton, SignedOut, SignedIn } from "@clerk/nextjs";
import Link from "next/link";
import { isBonusActive, formatTimeRemaining, LAUNCH_BONUS_CONFIG } from "@/config/launch-bonus";

const PLANS = [
  {
    id: "free",
    name: "Free Tier",
    price: "€0",
    period: "/mo",
    credits: 5,
    bonusCredits: 10,
    reset: "Resets every 30 days",
    idealFor: "Curiosity",
    features: ["Standard Generation", "Community Support"],
  },
  {
    id: "pro",
    name: "Pro Sub",
    price: "€5.90",
    period: "/mo",
    credits: 80,
    reset: "Resets every 30 days",
    idealFor: "Active Production",
    features: ["Priority Generation", "Priority Support"],
  }
];

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

export default function PricingPage() {
  const [timeRemaining, setTimeRemaining] = useState<string>('');
  const [bonusActive, setBonusActive] = useState(false);

  useEffect(() => {
    setBonusActive(isBonusActive());
    
    if (!isBonusActive()) return;
    
    const timer = setInterval(() => {
      const remaining = formatTimeRemaining();
      setTimeRemaining(remaining);
      
      if (remaining === 'Expired') {
        setBonusActive(false);
        clearInterval(timer);
      }
    }, 1000);
    
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen bg-[#0A0A0B] text-white selection:bg-accent-primary/30 font-sans flex flex-col">
      <Navbar />
      
      <main className="flex-1 flex flex-col justify-center py-20">
        <div className="max-w-6xl mx-auto px-6 w-full">
            
            <div className="text-center mb-16 space-y-4">
                <h2 className="text-xs font-black text-accent-primary uppercase tracking-[0.3em] mb-4">
                    Invest in your sound
                </h2>
                <h1 className="text-4xl md:text-6xl font-black text-white tracking-tighter">
                    Simple, Transparent <span className="text-accent-secondary">Pricing.</span>
                </h1>
                <p className="text-text-dim max-w-xl mx-auto text-lg">
                    Start for free. Upgrade for power. No hidden fees.
                </p>
            </div>

            {/* Monthly Subscriptions */}
            <div className="mb-16">
                <div className="flex items-center gap-2 text-accent-primary mb-8 justify-center">
                    <Zap className="w-5 h-5" />
                    <h3 className="text-xl font-bold uppercase tracking-wider text-white">Monthly Subscriptions</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
                    {PLANS.map((plan) => {
                        const isProPlan = plan.id === 'pro';
                        const showBonus = plan.id === 'free' && bonusActive;
                        
                        return (
                            <motion.div 
                                key={plan.id}
                                whileHover={{ y: -5 }}
                                className={`relative p-10 rounded-3xl border-2 flex flex-col gap-6 overflow-hidden transition-all ${
                                    isProPlan
                                        ? "bg-[#0f0f10] border-accent-primary/60 shadow-[0_0_50px_-10px_rgba(255,124,37,0.2)]" 
                                        : "bg-[#0a0a0b] border-white/20"
                                }`}
                            >
                                {isProPlan && (
                                    <div className="absolute top-0 right-0 bg-accent-primary text-black text-[10px] font-black uppercase tracking-widest px-4 py-2 rounded-bl-xl">
                                        Best Value
                                    </div>
                                )}

                                {showBonus && (
                                    <div className="absolute top-0 right-0 bg-gradient-to-r from-red-500 to-accent-primary text-white text-[10px] font-black uppercase tracking-widest px-4 py-2 rounded-bl-xl animate-pulse">
                                        Launch Bonus
                                    </div>
                                )}

                                <div className="space-y-2">
                                    <div className="text-xs font-mono text-text-dim uppercase tracking-wider">{plan.idealFor}</div>
                                    <h3 className="text-3xl font-black text-white">{plan.name}</h3>
                                    <div className="flex items-baseline gap-1">
                                        <span className="text-5xl font-black text-white">{plan.price}</span>
                                        <span className="text-lg text-text-dim">{plan.period}</span>
                                    </div>
                                </div>

                                {/* Credits Section with Dividers */}
                                <div className="py-6 border-t border-b border-white/10 space-y-4">
                                    <div className="flex justify-between items-center">
                                        <div className="flex items-center gap-3">
                                            <Sparkles className="w-5 h-5 text-accent-primary" />
                                            {showBonus ? (
                                                <div className="flex items-center gap-3">
                                                    {/* Strikethrough 5 with RED diagonal line */}
                                                    <div className="relative inline-block">
                                                        <span className="text-4xl font-bold text-white/30">5</span>
                                                        <div className="absolute inset-0 flex items-center justify-center">
                                                            <div className="w-full h-[3px] bg-red-500 rotate-[-15deg] shadow-lg" />
                                                        </div>
                                                    </div>
                                                    <span className="text-4xl font-black text-accent-primary">10</span>
                                                    <span className="text-lg text-white">Credits</span>
                                                </div>
                                            ) : (
                                                <span className="text-2xl font-black text-white">{plan.credits} Credits</span>
                                            )}
                                        </div>
                                        <span className="text-xs font-bold text-accent-primary bg-accent-primary/10 border border-accent-primary/30 px-3 py-1.5 rounded-md whitespace-nowrap">
                                            {plan.reset}
                                        </span>
                                    </div>
                                    
                                    {/* Enhanced Countdown */}
                                    {showBonus && timeRemaining && (
                                        <div className="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-gradient-to-r from-red-500/10 to-accent-primary/10 border border-accent-primary/40">
                                            <Clock className="w-4 h-4 text-accent-primary animate-pulse" />
                                            <span className="font-mono text-sm font-bold text-white">
                                                Bonus ends in: <strong className="text-accent-primary text-base">{timeRemaining}</strong>
                                            </span>
                                        </div>
                                    )}
                                </div>

                                {/* Features - Only show for Pro plan */}
                                {isProPlan && (
                                    <ul className="space-y-3 flex-1">
                                        {plan.features.map((feature, idx) => (
                                            <li key={idx} className="flex items-center gap-3 text-sm text-white font-medium">
                                                <Check className="w-4 h-4 text-accent-primary" />
                                                {feature}
                                            </li>
                                        ))}
                                    </ul>
                                )}
                                
                                {/* Spacer for Free tier to align button with Pro */}
                                {!isProPlan && <div className="flex-1" />}

                                {/* High Contrast Buttons */}
                                <SignedOut>
                                    <SignInButton mode="modal">
                                        <button className={`w-full py-4 rounded-xl font-black uppercase tracking-widest text-xs transition-all ${
                                            isProPlan
                                                ? "bg-accent-primary text-black hover:scale-[1.02] shadow-[0_0_30px_rgba(255,124,37,0.3)]"
                                                : showBonus
                                                    ? "bg-white text-black hover:scale-[1.02] shadow-[0_0_30px_rgba(255,255,255,0.15)]"
                                                    : "bg-white/10 hover:bg-white/20 text-white border-2 border-white/20"
                                        }`}>
                                            {showBonus ? `Claim ${plan.bonusCredits} Free Credits` : isProPlan ? 'Start Pro Trial' : 'Get Started Free'}
                                        </button>
                                    </SignInButton>
                                </SignedOut>
                                
                                <SignedIn>
                                    <Link href="/dashboard/settings">
                                        <button className={`w-full py-4 rounded-xl font-black uppercase tracking-widest text-xs transition-all ${
                                            isProPlan
                                                ? "bg-accent-primary text-black hover:scale-[1.02] shadow-[0_0_30px_rgba(255,124,37,0.3)]"
                                                : "bg-white/10 hover:bg-white/20 text-white border-2 border-white/20"
                                        }`}>
                                            {isProPlan ? 'Manage Subscription' : 'View Dashboard'}
                                        </button>
                                    </Link>
                                </SignedIn>
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* One-Time Credit Packs */}
            <div>
                <div className="flex items-center gap-2 text-accent-secondary mb-8 justify-center">
                    <Box className="w-5 h-5" />
                    <h3 className="text-xl font-bold uppercase tracking-wider text-white">One-Time Credit Packs</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10 max-w-5xl mx-auto">
                    {PACKS.map((pack) => (
                        <motion.div 
                            key={pack.id}
                            whileHover={{ y: -5 }}
                            className="relative p-10 rounded-3xl border-2 border-white/15 bg-[#0a0a0b] flex flex-col gap-6 overflow-hidden transition-all"
                        >
                            <div className="space-y-2">
                                <div className="text-xs font-mono text-text-dim uppercase tracking-wider">{pack.idealFor}</div>
                                <h3 className="text-3xl font-black text-white">{pack.name}</h3>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-5xl font-black text-white">{pack.price}</span>
                                </div>
                            </div>

                            {/* Credits Section with Dividers */}
                            <div className="py-6 border-t border-b border-white/10 space-y-4">
                                <div className="flex justify-between items-center">
                                    <div className="flex items-center gap-3">
                                        <Sparkles className="w-5 h-5 text-accent-secondary" />
                                        <span className="text-2xl font-black text-white">{pack.credits} Credits</span>
                                    </div>
                                    <span className="text-xs font-bold text-accent-success bg-accent-success/10 border border-accent-success/30 px-3 py-1.5 rounded-md whitespace-nowrap">
                                        {pack.reset}
                                    </span>
                                </div>
                            </div>

                            {/* Features */}
                            <ul className="space-y-3 flex-1">
                                <li className="flex items-center gap-3 text-sm text-text-dim">
                                    <Check className="w-4 h-4 text-accent-success" />
                                    No Subscription Required
                                </li>
                                <li className="flex items-center gap-3 text-sm text-text-dim">
                                    <Check className="w-4 h-4 text-accent-success" />
                                    Lifetime Validity
                                </li>
                                <li className="flex items-center gap-3 text-sm text-text-dim">
                                    <Check className="w-4 h-4 text-accent-success" />
                                    Instant Top-up
                                </li>
                            </ul>

                            {/* High Contrast Button */}
                            <SignedOut>
                                <SignInButton mode="modal">
                                    <button className="w-full py-4 rounded-xl bg-white text-black font-black uppercase tracking-widest hover:scale-[1.02] shadow-[0_0_30px_rgba(255,255,255,0.15)] transition-all">
                                        Buy Pack
                                    </button>
                                </SignInButton>
                            </SignedOut>
                            
                            <SignedIn>
                                <Link href="/dashboard/settings">
                                    <button className="w-full py-4 rounded-xl bg-white text-black font-black uppercase tracking-widest hover:scale-[1.02] shadow-[0_0_30px_rgba(255,255,255,0.15)] transition-all">
                                        Go to Dashboard
                                    </button>
                                </Link>
                            </SignedIn>
                        </motion.div>
                    ))}
                </div>
            </div>

        </div>
      </main>
      
      <Footer />
    </div>
  );
}
