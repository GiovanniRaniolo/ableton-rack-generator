import Link from "next/link";
import { SignInButton, SignedIn, SignedOut } from "@clerk/nextjs";
import { ArrowRight, Lock } from "lucide-react";
import { Logo } from "@/components/ui/Logo";

export default function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col bg-bg-deep text-white font-sans selection:bg-accent-primary/30">
      
      {/* Navbar */}
      <nav className="fixed top-0 inset-x-0 z-50 px-6 py-6 flex justify-between items-center">
        <Logo className="w-8 h-8" />
        <SignedOut>
            <SignInButton mode="modal">
                <button className="px-5 py-2 rounded-full bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 text-xs font-bold uppercase tracking-widest transition-all">
                    Login
                </button>
            </SignInButton>
        </SignedOut>
        <SignedIn>
            <Link href="/dashboard" className="px-5 py-2 rounded-full bg-accent-primary/10 border border-accent-primary/20 text-accent-primary text-xs font-bold uppercase tracking-widest transition-all hover:bg-accent-primary/20">
                Dashboard
            </Link>
        </SignedIn>
      </nav>

      {/* Hero */}
      <main className="flex-1 flex flex-col items-center justify-center text-center px-6 relative overflow-hidden">
        
        {/* Background Gradients */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent-primary/10 blur-[120px] rounded-full pointer-events-none"></div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-accent-secondary/10 blur-[80px] rounded-full pointer-events-none mix-blend-screen"></div>

        <div className="relative z-10 space-y-10 max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-bold uppercase tracking-widest text-text-dim mb-4">
                <span className="w-2 h-2 rounded-full bg-accent-success animate-pulse"></span>
                v5.3 Surgical Engine Online
            </div>

            <Logo className="w-32 h-32 mx-auto" showText={false} />
            
            <h1 className="text-7xl md:text-9xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-white/40 tracking-tighter leading-[0.9]">
                ADG<br/>BUILDER
            </h1>
            
            <p className="text-xl md:text-2xl text-text-dim font-medium max-w-2xl mx-auto leading-relaxed">
                The first <span className="text-white">semantic engine</span> for Ableton Live. 
                Generate <span className="text-accent-secondary">parallel chains</span> and <span className="text-accent-primary">mapped macros</span> using standard language.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-4 pt-8">
                <SignedOut>
                    <SignInButton mode="modal" forceRedirectUrl="/dashboard">
                        <button className="px-10 py-5 bg-white text-black font-black uppercase tracking-[0.2em] text-sm rounded-xl hover:scale-105 transition-transform flex items-center gap-3 shadow-[0_0_40px_rgba(255,255,255,0.2)]">
                            Start Building
                            <ArrowRight className="w-5 h-5" />
                        </button>
                    </SignInButton>
                </SignedOut>

                <SignedIn>
                    <Link href="/dashboard">
                        <button className="px-10 py-5 bg-accent-primary text-black font-black uppercase tracking-[0.2em] text-sm rounded-xl hover:scale-105 transition-transform flex items-center gap-3 shadow-[0_0_40px_rgba(255,124,37,0.4)]">
                            Go to Dashboard
                            <ArrowRight className="w-5 h-5" />
                        </button>
                    </Link>
                </SignedIn>
                
                <div className="flex items-center gap-2 px-6 py-4 rounded-xl bg-white/5 border border-white/5 text-xs font-mono text-text-dim">
                    <Lock className="w-3 h-3" />
                    Secure Access Required
                </div>
            </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center text-[10px] uppercase tracking-widest text-text-dim opacity-50">
        &copy; 2026 ADG Builder. All systems operational.
      </footer>
    </div>
  );
}
