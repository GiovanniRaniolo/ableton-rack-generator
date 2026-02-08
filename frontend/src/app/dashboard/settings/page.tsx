"use client";

import { motion } from "framer-motion";
import { Check, Sparkles, Zap, Shield, HelpCircle, ExternalLink, ArrowLeft, CreditCard, Box } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { syncUserProfile } from "@/app/actions";

const PLANS = [
  {
    id: "free",
    name: "Free Tier",
    price: "€0",
    period: "/mo",
    credits: 10,
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

export default function PlansPage() {
  const [isPro, setIsPro] = useState<boolean | null>(null);

  useEffect(() => {
    syncUserProfile().then(res => {
        if (res.success && res.is_pro !== undefined) {
             setIsPro(res.is_pro);
        } else {
             setIsPro(false); // Default to free if unknown
        }
    });
  }, []);

  if (isPro === null) {
      return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-accent-primary border-t-transparent rounded-full animate-spin" />
        </div>
      );
  }

  return (
    <div className="min-h-screen p-6 md:p-12 max-w-6xl mx-auto space-y-16 pb-6">
      
      {/* Header */}
      <div className="space-y-4 animate-in fade-in slide-in-from-top-4 duration-700">
        <h1 className="text-4xl font-black text-white tracking-tight">Plans & Credits</h1>
        <p className="text-text-dim text-lg max-w-2xl">
          Choose the best plan for your production needs or top up your credits.
        </p>
      </div>

      {/* Subscription Section */}
      <section className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        <div className="flex items-center gap-2 text-accent-primary">
            <Zap className="w-5 h-5" />
            <h2 className="text-xl font-bold uppercase tracking-wider text-white">Monthly Subscriptions</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {PLANS.map((plan) => {
                const isCurrentPlan = plan.id === 'pro' ? isPro : !isPro;
                const isUpgrade = plan.id === 'pro' && !isPro;
                
                // Logic for visual state
                let cta = "Current Plan";
                let disabled = true;
                let highlight = false;

                if (isCurrentPlan) {
                    cta = "Current Plan";
                    disabled = true;
                    highlight = false; 
                    // Special case: If Pro is current, we might want to highlight it as "Active"
                    if (plan.id === 'pro') highlight = true;
                } else if (isUpgrade) {
                    cta = "Upgrade to Pro";
                    disabled = false;
                    highlight = true;
                } else {
                    // Downgrade case (Free tier when Pro)
                    cta = "Downgrade";
                    disabled = false; // Allow click to manage stripe/cancel
                    highlight = false;
                }

                return (
                    <motion.div 
                        key={plan.id}
                        whileHover={!disabled ? { y: -5 } : {}}
                        className={cn(
                            "relative p-8 rounded-3xl border flex flex-col gap-6 overflow-hidden group transition-all",
                            highlight
                                ? "bg-[#0f0f10] border-accent-primary/50 shadow-[0_0_40px_-10px_rgba(255,124,37,0.15)]" 
                                : "bg-[#0a0a0b] border-white/5",
                             isCurrentPlan && "border-accent-success/30"
                        )}
                    >
                        {highlight && isUpgrade && (
                            <div className="absolute top-0 right-0 bg-accent-primary text-black text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-bl-xl">
                                Best Value
                            </div>
                        )}

                        {isCurrentPlan && (
                             <div className="absolute top-0 right-0 bg-accent-success/20 text-accent-success text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-bl-xl flex items-center gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-accent-success animate-pulse"/>
                                Active
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

                        <div className="py-6 border-t border-b border-white/5 space-y-4">
                            <div className="flex justify-between items-center">
                                <span className="text-lg font-bold text-white flex items-center gap-2">
                                    <Sparkles className="w-4 h-4 text-accent-primary" />
                                    {plan.credits} Credits
                                </span>
                                <span className="text-xs text-text-dim bg-white/5 px-2 py-1 rounded-md">{plan.reset}</span>
                            </div>
                            <ul className="space-y-2">
                                {plan.features.map(f => (
                                    <li key={f} className="flex items-center gap-2 text-sm text-text-dim">
                                        <Check className="w-4 h-4 text-accent-success" />
                                        {f}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <button 
                            disabled={disabled}
                            className={cn(
                                "w-full py-4 rounded-xl font-bold uppercase tracking-widest text-xs transition-all flex items-center justify-center gap-2",
                                isUpgrade
                                    ? "bg-white text-black hover:scale-[1.02] shadow-lg"
                                    : disabled 
                                        ? "bg-white/5 text-white/50 cursor-default"
                                        : "bg-white/5 hover:bg-white/10 text-white"
                            )}
                        >
                            {cta}
                            {isUpgrade && <ArrowLeft className="w-4 h-4 rotate-180" />}
                            {disabled && <Check className="w-4 h-4" />}
                        </button>
                    </motion.div>
                );
            })}
        </div>
      </section>

      {/* Credit Packs Section */}
      <section className="space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        <div className="flex items-center gap-2 text-accent-secondary">
            <Box className="w-5 h-5" />
            <h2 className="text-xl font-bold uppercase tracking-wider text-white">One-Time Packs</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {PACKS.map((pack) => (
                <motion.div 
                    key={pack.id}
                    whileHover={{ scale: 1.01 }}
                    className="p-6 rounded-2xl bg-[#0a0a0b] border border-white/5 flex items-center justify-between hover:border-white/10 transition-all group"
                >
                    <div className="space-y-1">
                        <div className="flex items-center gap-2">
                             <h3 className="text-lg font-bold text-white">{pack.name}</h3>
                             <span className="text-[10px] bg-accent-secondary/10 text-accent-secondary px-2 py-0.5 rounded-full font-bold uppercase">{pack.idealFor}</span>
                        </div>
                        <div className="text-sm text-text-dim">{pack.credits} Credits • <span className="text-accent-success">{pack.reset}</span></div>
                    </div>
                    
                    <div className="flex items-center gap-4">
                        <span className="text-xl font-bold text-white">{pack.price}</span>
                        <button className="px-5 py-2 rounded-lg bg-white/5 hover:bg-white text-white hover:text-black font-bold uppercase text-[10px] tracking-widest transition-all">
                            {pack.cta}
                        </button>
                    </div>
                </motion.div>
            ))}
        </div>
      </section>

      {/* Meta Links & Footer */}
      <section className="pt-12 border-t border-white/5 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
         <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="space-y-4">
                <h4 className="text-sm font-bold uppercase tracking-widest text-text-dim">Resources</h4>
                <ul className="space-y-2">
                    <li><Link href="#" className="flex items-center gap-2 text-sm text-white hover:text-accent-primary transition-colors"><HelpCircle className="w-4 h-4" /> Documentation</Link></li>
                    <li><Link href="#" className="flex items-center gap-2 text-sm text-white hover:text-accent-primary transition-colors"><ExternalLink className="w-4 h-4" /> Tutorials</Link></li>
                </ul>
            </div>
            
            <div className="space-y-4">
                <h4 className="text-sm font-bold uppercase tracking-widest text-text-dim">Legal</h4>
                <ul className="space-y-2">
                    <li><Link href="#" className="flex items-center gap-2 text-sm text-white hover:text-accent-primary transition-colors"><Shield className="w-4 h-4" /> Privacy Policy</Link></li>
                    <li><Link href="#" className="flex items-center gap-2 text-sm text-white hover:text-accent-primary transition-colors"><Shield className="w-4 h-4" /> Terms of Service</Link></li>
                </ul>
            </div>

            <div className="flex items-end justify-end">
                 <Link href="/">
                    <button className="px-6 py-3 rounded-xl border border-white/10 hover:border-white/30 text-text-dim hover:text-white transition-all text-xs font-bold uppercase tracking-widest flex items-center gap-2">
                        Back to Website <ExternalLink className="w-3 h-3" />
                    </button>
                 </Link>
            </div>
         </div>
         
         <div className="mt-4 text-center">
            <p className="text-[10px] text-white/40 font-bold uppercase tracking-[0.2em]">
                ADG Builder v5.4 • Engine Online
            </p>
         </div>
      </section>

    </div>
  );
}
