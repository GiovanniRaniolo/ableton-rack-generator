"use client";

import { motion } from "framer-motion";
import { Check, Zap, CreditCard, Sparkles } from "lucide-react";
import Link from "next/link";
import { SignInButton, SignedOut } from "@clerk/nextjs";

export function PricingSection() {
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

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                
                {/* Free Tier */}
                <div className="p-8 rounded-3xl border border-white/5 bg-white/5 hover:border-white/10 transition-all flex flex-col">
                    <div className="mb-6">
                        <div className="text-sm font-bold uppercase tracking-widest text-text-dim mb-2">Starter</div>
                        <div className="text-4xl font-black text-white">€0<span className="text-lg text-white/30 font-medium">/mo</span></div>
                    </div>
                    <ul className="space-y-4 mb-8 flex-1">
                        <li className="flex items-center gap-3 text-sm text-text-main"><Check className="w-4 h-4 text-white/50" /> 3 Rack Builds / Month</li>
                        <li className="flex items-center gap-3 text-sm text-text-main"><Check className="w-4 h-4 text-white/50" /> Standard Device Chains</li>
                        <li className="flex items-center gap-3 text-sm text-text-main"><Check className="w-4 h-4 text-white/50" /> Native Devices Only</li>
                    </ul>
                    <SignedOut>
                        <SignInButton mode="modal">
                            <button className="w-full py-3 rounded-xl border border-white/10 hover:bg-white/5 text-xs font-bold uppercase tracking-widest transition-all">
                                Get Started Free
                            </button>
                        </SignInButton>
                    </SignedOut>
                </div>

                {/* Pro Subscription */}
                <div className="p-8 rounded-3xl border border-accent-primary/20 bg-accent-primary/5 hover:bg-accent-primary/10 transition-all relative flex flex-col transform hover:-translate-y-2 duration-300">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 py-1 bg-accent-primary text-black text-[10px] font-black uppercase tracking-widest rounded-full shadow-[0_0_20px_rgba(255,124,37,0.4)]">
                        Most Popular
                    </div>
                    <div className="mb-6">
                        <div className="text-sm font-bold uppercase tracking-widest text-accent-primary mb-2 flex items-center gap-2">
                             <Zap className="w-4 h-4" /> Pro Creator
                        </div>
                        <div className="text-4xl font-black text-white">€5.90<span className="text-lg text-white/30 font-medium">/mo</span></div>
                        <div className="text-xs text-text-dim mt-1">Cancel anytime.</div>
                    </div>
                    <ul className="space-y-4 mb-8 flex-1">
                        <li className="flex items-center gap-3 text-sm text-white font-medium"><Check className="w-4 h-4 text-accent-primary" /> Unlimited Rack Builds</li>
                        <li className="flex items-center gap-3 text-sm text-white font-medium"><Check className="w-4 h-4 text-accent-primary" /> Complex Parallel Chains</li>
                        <li className="flex items-center gap-3 text-sm text-white font-medium"><Check className="w-4 h-4 text-accent-primary" /> Intelligent Macro Mapping</li>
                        <li className="flex items-center gap-3 text-sm text-white font-medium"><Check className="w-4 h-4 text-accent-primary" /> Commercial License</li>
                    </ul>
                    <SignedOut>
                        <SignInButton mode="modal">
                             <button className="w-full py-3 rounded-xl bg-accent-primary text-black font-bold uppercase tracking-widest hover:brightness-110 shadow-[0_0_20px_rgba(255,124,37,0.2)] transition-all">
                               Start Pro Trial
                             </button>
                        </SignInButton>
                    </SignedOut>
                </div>

                {/* One-Time Packs */}
                <div className="p-8 rounded-3xl border border-accent-secondary/20 bg-accent-secondary/5 hover:bg-accent-secondary/10 transition-all flex flex-col">
                    <div className="mb-6">
                        <div className="text-sm font-bold uppercase tracking-widest text-accent-secondary mb-2 flex items-center gap-2">
                            <Sparkles className="w-4 h-4" /> Power Packs
                        </div>
                        <div className="text-4xl font-black text-white">€2.90<span className="text-lg text-white/30 font-medium">+</span></div>
                        <div className="text-xs text-text-dim mt-1">Pay as you go.</div>
                    </div>
                    <ul className="space-y-4 mb-8 flex-1">
                        <li className="flex items-center gap-3 text-sm text-text-main"><Check className="w-4 h-4 text-accent-secondary" /> 50 Credits Pack</li>
                        <li className="flex items-center gap-3 text-sm text-text-main"><Check className="w-4 h-4 text-accent-secondary" /> No Subscription</li>
                        <li className="flex items-center gap-3 text-sm text-text-main"><Check className="w-4 h-4 text-accent-secondary" /> Lifetime Validity</li>
                    </ul>
                    <SignedOut>
                        <SignInButton mode="modal">
                            <button className="w-full py-3 rounded-xl border border-accent-secondary/20 hover:bg-accent-secondary/20 text-accent-secondary text-xs font-bold uppercase tracking-widest transition-all">
                                Buy Credits
                            </button>
                        </SignInButton>
                    </SignedOut>
                </div>

            </div>
        </div>
    </section>
  );
}
