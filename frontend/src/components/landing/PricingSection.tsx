"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Check, Zap, CreditCard, Sparkles, Clock, Box } from "lucide-react";
import Link from "next/link";
import { SignInButton, SignedOut } from "@clerk/nextjs";
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
    features: ["Priority Generation", "Commercial License", "Priority Support"],
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
    cta: "Buy Pack",
  },
  {
    id: "power",
    name: "Power Pack",
    price: "€4.90",
    credits: 40,
    reset: "Never Expires",
    idealFor: "Casual Use",
    cta: "Buy Pack",
  }
];

export function PricingSection() {
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
    <section id="pricing" className="py-24 px-6 bg-[#0A0A0B]">
        <div className="max-w-7xl mx-auto">
            
            <div className="text-center mb-16 space-y-4">
                <h2 className="text-3xl md:text-5xl font-black text-white tracking-tighter">
                    Simple, Transparent <span className="text-accent-secondary">Pricing.</span>
                </h2>
                <p className="text-text-dim max-w-xl mx-auto">
                    Start for free. Upgrade for power. No hidden fees.
                </p>
            </div>

            {/* Monthly Subscriptions */}
            <div className="mb-12">
                <div className="flex items-center gap-2 text-accent-primary mb-6">
                    <Zap className="w-5 h-5" />
                    <h3 className="text-xl font-bold uppercase tracking-wider text-white">Monthly Subscriptions</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {PLANS.map((plan) => {
                        const isProPlan = plan.id === 'pro';
                        const showBonus = plan.id === 'free' && bonusActive;
                        
                        return (
                            <motion.div 
                                key={plan.id}
                                whileHover={{ y: -5 }}
                                className={`relative p-8 rounded-3xl border flex flex-col gap-6 overflow-hidden group transition-all ${
                                    isProPlan
                                        ? "bg-[#0f0f10] border-accent-primary/50 shadow-[0_0_40px_-10px_rgba(255,124,37,0.15)]" 
                                        : "bg-[#0a0a0b] border-white/5"
                                }`}
                            >
                                {isProPlan && (
                                    <div className="absolute top-0 right-0 bg-accent-primary text-black text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-bl-xl">
                                        Best Value
                                    </div>
                                )}

                                {showBonus && (
                                    <div className="absolute top-0 right-0 bg-accent-primary/20 text-accent-primary text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-bl-xl flex items-center gap-1 animate-pulse">
                                        🎁 Launch Bonus
                                    </div>
                                )}

                                <div className="space-y-2">
                                    <div className="text-sm font-mono text-text-dim uppercase tracking-wider">{plan.idealFor}</div>
                                    <h3 className="text-2xl font-bold text-white">{plan.name}</h3>
                                    <div className="flex items-baseline gap-1">
                                        <span className="text-4xl font-black text-white">{plan.price}</span>
                                        <span className="text-text-dim">{plan.period}</span>
                                    </div>
                                </div>

                                <div className="space-y-3">
                                    <div className="flex items-center gap-2">
                                        {showBonus ? (
                                            <>
                                                <span className="text-2xl font-black text-white line-through decoration-2 opacity-40">{plan.credits}</span>
                                                <span className="text-3xl font-black text-accent-primary">{plan.bonusCredits}</span>
                                                <span className="text-sm text-text-dim">credits</span>
                                            </>
                                        ) : (
                                            <>
                                                <span className="text-3xl font-black text-white">{plan.credits}</span>
                                                <span className="text-sm text-text-dim">credits</span>
                                            </>
                                        )}
                                    </div>
                                    <div className="text-xs text-text-dim">{plan.reset}</div>
                                    
                                    {showBonus && timeRemaining && (
                                        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-black/40 border border-accent-primary/30 text-xs text-white">
                                            <Clock className="w-3 h-3 text-accent-primary" />
                                            <span className="font-mono">Ends in: <strong className="text-accent-primary">{timeRemaining}</strong></span>
                                        </div>
                                    )}
                                </div>

                                <ul className="space-y-3 flex-1">
                                    {plan.features.map((feature, idx) => (
                                        <li key={idx} className={`flex items-center gap-3 text-sm ${isProPlan ? 'text-white font-medium' : 'text-text-main'}`}>
                                            <Check className={`w-4 h-4 ${isProPlan ? 'text-accent-primary' : 'text-white/50'}`} />
                                            {feature}
                                        </li>
                                    ))}
                                </ul>

                                <SignedOut>
                                    <SignInButton mode="modal">
                                        <button className={`w-full py-3 rounded-xl text-xs font-bold uppercase tracking-widest transition-all ${
                                            isProPlan
                                                ? "bg-accent-primary text-black hover:brightness-110 shadow-[0_0_20px_rgba(255,124,37,0.2)]"
                                                : "border border-white/10 hover:bg-white/5"
                                        }`}>
                                            {showBonus ? `Claim ${plan.bonusCredits} Free Credits` : isProPlan ? 'Start Pro Trial' : 'Get Started Free'}
                                        </button>
                                    </SignInButton>
                                </SignedOut>
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* One-Time Credit Packs */}
            <div>
                <div className="flex items-center gap-2 text-accent-secondary mb-6">
                    <Box className="w-5 h-5" />
                    <h3 className="text-xl font-bold uppercase tracking-wider text-white">One-Time Credit Packs</h3>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {PACKS.map((pack) => (
                        <motion.div 
                            key={pack.id}
                            whileHover={{ y: -5 }}
                            className="relative p-8 rounded-3xl border border-white/5 bg-[#0a0a0b] flex flex-col gap-6 overflow-hidden group transition-all"
                        >
                            <div className="space-y-2">
                                <div className="text-sm font-mono text-text-dim uppercase tracking-wider">{pack.idealFor}</div>
                                <h3 className="text-2xl font-bold text-white">{pack.name}</h3>
                                <div className="flex items-baseline gap-1">
                                    <span className="text-4xl font-black text-white">{pack.price}</span>
                                </div>
                            </div>

                            <div className="space-y-3">
                                <div className="flex items-center gap-2">
                                    <span className="text-3xl font-black text-white">{pack.credits}</span>
                                    <span className="text-sm text-text-dim">credits</span>
                                </div>
                                <div className="text-xs text-text-dim">{pack.reset}</div>
                            </div>

                            <ul className="space-y-3 flex-1">
                                <li className="flex items-center gap-3 text-sm text-text-main">
                                    <Check className="w-4 h-4 text-white/50" />
                                    No Subscription Required
                                </li>
                                <li className="flex items-center gap-3 text-sm text-text-main">
                                    <Check className="w-4 h-4 text-white/50" />
                                    Lifetime Validity
                                </li>
                                <li className="flex items-center gap-3 text-sm text-text-main">
                                    <Check className="w-4 h-4 text-white/50" />
                                    Instant Top-up
                                </li>
                            </ul>

                            <SignedOut>
                                <SignInButton mode="modal">
                                    <button className="w-full py-3 rounded-xl border border-white/10 hover:bg-white/5 text-xs font-bold uppercase tracking-widest transition-all">
                                        {pack.cta}
                                    </button>
                                </SignInButton>
                            </SignedOut>
                        </motion.div>
                    ))}
                </div>
            </div>

        </div>
    </section>
  );
}
