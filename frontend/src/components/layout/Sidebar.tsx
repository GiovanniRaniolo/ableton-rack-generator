"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserButton } from "@clerk/nextjs";
import { History, Zap, CreditCard } from "lucide-react";
import { Logo } from "../ui/Logo";

const navItems = [
  { icon: Zap, label: "Generator", href: "/dashboard" },
  { icon: History, label: "Archive", href: "/dashboard/history" },
  { icon: CreditCard, label: "Plans", href: "/dashboard/settings" },
];

import { useEffect, useState } from "react";
import { syncUserProfile } from "@/app/actions";

export function Sidebar() {
  const pathname = usePathname();
  const [credits, setCredits] = useState<number | null>(null);
  const [isPro, setIsPro] = useState(false);

  useEffect(() => {
    async function fetchCredits() {
        try {
            const res = await syncUserProfile();
            if (res.success && res.credits !== undefined) {
                setCredits(res.credits);
                if (res.is_pro !== undefined) setIsPro(res.is_pro);
            }
        } catch (e) {
            console.error("Failed to fetch credits", e);
        }
    }
    fetchCredits();
  }, []);

  return (
    <aside className="w-64 h-screen fixed left-0 top-0 border-r border-white/5 bg-bg-surface/30 backdrop-blur-xl flex flex-col z-50">
      {/* Logo Section */}
      <Link href="/dashboard?new=true" className="flex items-center justify-center py-6 border-b border-white/5 cursor-pointer hover:bg-white/5 transition-colors group">
        <Logo className="w-12 h-12" showText={true} />
      </Link>

      {/* Navigation */}
      <nav className="flex-1 py-8 px-4 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href && item.href !== '/dashboard'; // Strict check for subpages
          const isHomeActive = pathname === '/dashboard' && item.href === '/dashboard';
          
          return (
            <Link
              key={item.href}
              href={item.href === '/dashboard' ? '/dashboard?new=true' : item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group
                ${isActive || isHomeActive
                  ? "bg-accent-primary/10 text-accent-primary shadow-[0_0_20px_-5px_rgba(255,124,37,0.3)]" 
                  : "text-text-dim hover:text-white hover:bg-white/5"
                }`}
            >
              <item.icon className={`w-5 h-5 ${isActive ? "text-accent-primary" : "text-text-dim group-hover:text-white"}`} />
              <span className="font-medium text-sm tracking-wide">{item.label}</span>
              
              {isActive && (
                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-accent-primary shadow-[0_0_8px_rgba(255,124,37,0.8)]" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Section */}
      <div className="p-4 m-4 rounded-2xl bg-[#0a0a0b] border border-white/5 flex items-center gap-4 relative overflow-hidden group">
        {/* Glow Effect */}
        <div className="absolute -bottom-10 -right-10 w-24 h-24 bg-accent-primary/5 blur-3xl rounded-full group-hover:bg-accent-primary/10 transition-colors" />

        <div className="relative">
            <div className="border border-white/10 rounded-full w-10 h-10 flex items-center justify-center overflow-hidden">
                 <UserButton 
                    appearance={{
                        elements: {
                            userButtonAvatarBox: "w-10 h-10",
                            userButtonTrigger: "focus:shadow-none focus:outline-none"
                        }
                    }}
                />
            </div>
            {/* Absolute Online Badge */}
            <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 bg-[#0a0a0b] rounded-full flex items-center justify-center">
                <div className="w-2 h-2 rounded-full bg-accent-success shadow-[0_0_8px_rgba(62,240,139,0.8)] animate-pulse" />
            </div>
        </div>

        <div className="flex flex-col z-10">
            <span className="text-[10px] uppercase tracking-wider font-bold text-text-dim mb-0.5">
                {isPro ? "Pro Plan" : "Free Plan"}
            </span>
            <div className="flex items-baseline gap-1.5">
                <span className="font-mono text-xl font-bold text-white tracking-tighter">
                    {credits !== null ? credits : '-'}
                </span>
                <span className="text-[10px] text-accent-primary font-bold uppercase tracking-wider">Credits</span>
            </div>
        </div>
      </div>
    </aside>
  );
}
