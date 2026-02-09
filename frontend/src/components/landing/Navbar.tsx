"use client";

import Link from "next/link";
import { SignInButton, SignedIn, SignedOut } from "@clerk/nextjs";
import { Logo } from "@/components/ui/Logo";
import { motion, useScroll, useTransform } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

export function Navbar() {
  const { scrollY } = useScroll();
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    return scrollY.onChange((latest) => {
      setIsScrolled(latest > 50);
    });
  }, [scrollY]);

  return (
    <motion.nav 
        className={cn(
            "fixed top-0 inset-x-0 z-50 px-6 py-4 transition-all duration-300",
            isScrolled ? "bg-[#0a0a0b]/80 backdrop-blur-md border-b border-white/5" : "bg-transparent"
        )}
    >
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link href="/" className="flex items-center gap-2 group">
             <Logo className="w-8 h-8 group-hover:rotate-90 transition-transform duration-700" showText={false} />
             <span className="font-bold tracking-tight text-white hidden md:block">ADG<span className="text-brand-primary">BUILDER</span></span>
        </Link>
        
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-text-dim">
            <Link href="#how-it-works" className="hover:text-white transition-colors">How it works</Link>
            <Link href="#features" className="hover:text-white transition-colors">Features</Link>
            <Link href="/pricing" className="hover:text-white transition-colors">Pricing</Link>
        </div>

        <div className="flex items-center gap-4">
            <SignedOut>
                <SignInButton mode="modal">
                    <button className="px-4 py-2 text-text-dim hover:text-white text-sm font-medium transition-colors">
                        Login
                    </button>
                </SignInButton>
                <SignInButton mode="modal">
                     <button className="group relative px-5 py-2 rounded-full bg-brand-primary text-black text-xs font-black uppercase tracking-widest overflow-hidden transition-all hover:scale-105">
                        <div className="absolute inset-0 bg-white/40 group-hover:translate-x-full transition-transform duration-500 skew-x-12 -translate-x-full" />
                        Get Started
                     </button>
                </SignInButton>
            </SignedOut>
            <SignedIn>
                <Link href="/dashboard" className="px-5 py-2 rounded-full bg-white/10 hover:bg-white/20 border border-white/10 text-white text-xs font-bold uppercase tracking-widest transition-all flex items-center gap-2">
                    Dashboard <ArrowRight className="w-3 h-3" />
                </Link>
            </SignedIn>
        </div>
      </div>
    </motion.nav>
  );
}
