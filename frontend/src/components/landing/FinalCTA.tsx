"use client";

import { SignInButton, SignedOut, SignedIn } from "@clerk/nextjs";
import Link from "next/link";
import { Check, Activity, Zap, Download, Cpu, Sparkles } from "lucide-react";

const trustSignals = [
    { icon: Zap, text: "10 Free Generations" },
    { icon: Download, text: "Instant .adg Download" },
    { icon: Cpu, text: "43 Audio Effects" },
    { icon: Sparkles, text: "Surgical NLP Engine" }
];

export function FinalCTA() {
    return (
        <section className="relative py-32 overflow-hidden">
            {/* Ambient Background */}
            <div className="absolute inset-0 bg-gradient-to-b from-bg-main via-accent-primary/5 to-bg-main" />
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent-primary/10 blur-[150px] rounded-full animate-pulse-slow" />
            </div>

            {/* Content Container */}
            <div className="max-w-4xl mx-auto px-6 text-center relative z-10">
                
                {/* Social Proof Micro-Element */}
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-xs text-accent-primary mb-8">
                    <Activity className="w-3 h-3 animate-pulse" />
                    <span className="font-bold">127 racks generated today</span>
                </div>

                {/* Headline */}
                <h2 className="text-4xl md:text-5xl lg:text-6xl font-black text-white mb-6 tracking-tight leading-tight">
                    Ready to Build Your<br />First Rack?
                </h2>

                {/* Subheadline */}
                <p className="text-lg md:text-xl text-text-dim mb-10 max-w-2xl mx-auto leading-relaxed">
                    Generate production-ready Ableton racks in seconds.{" "}
                    <strong className="text-white font-bold">No credit card required.</strong>
                </p>

                {/* CTA Buttons */}
                <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
                    <SignedOut>
                        <SignInButton mode="modal">
                            <button className="group px-10 py-5 bg-accent-primary hover:bg-[#ff904d] text-black font-black uppercase tracking-[0.2em] text-sm rounded-full shadow-[0_0_40px_rgba(255,124,37,0.4)] hover:shadow-[0_0_60px_rgba(255,124,37,0.6)] hover:scale-105 transition-all active:scale-95 cursor-pointer flex items-center justify-center gap-3">
                                <Zap className="w-5 h-5" />
                                Start Creating Free
                            </button>
                        </SignInButton>
                    </SignedOut>
                    
                    <SignedIn>
                        <Link href="/dashboard">
                            <button className="group px-10 py-5 bg-accent-primary hover:bg-[#ff904d] text-black font-black uppercase tracking-[0.2em] text-sm rounded-full shadow-[0_0_40px_rgba(255,124,37,0.4)] hover:shadow-[0_0_60px_rgba(255,124,37,0.6)] hover:scale-105 transition-all active:scale-95 cursor-pointer flex items-center justify-center gap-3">
                                <Zap className="w-5 h-5" />
                                Go to Dashboard
                            </button>
                        </Link>
                    </SignedIn>

                    <Link href="/pricing">
                        <button className="px-10 py-5 bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 text-white font-bold uppercase tracking-[0.2em] text-sm rounded-full transition-all cursor-pointer flex items-center justify-center gap-2">
                            View Pricing
                            <span className="text-accent-primary">→</span>
                        </button>
                    </Link>
                </div>

                {/* Trust Signals Grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
                    {trustSignals.map((signal, idx) => {
                        const Icon = signal.icon;
                        return (
                            <div key={idx} className="flex flex-col items-center gap-3 group">
                                <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center group-hover:border-accent-primary/50 transition-colors">
                                    <Icon className="w-5 h-5 text-accent-primary" />
                                </div>
                                <span className="text-sm text-text-dim font-medium group-hover:text-white transition-colors">
                                    {signal.text}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>
        </section>
    );
}
