"use client";

import { motion } from "framer-motion";
import { ArrowRight, Terminal, Zap, Cpu } from "lucide-react";
import Link from "next/link";
import { SignInButton, SignedOut, SignedIn } from "@clerk/nextjs";

export function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex flex-col items-center justify-center pt-32 pb-20 px-6 overflow-hidden">
      
      {/* Background Ambience */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-accent-primary/5 blur-[120px] rounded-full animate-pulse-glow" />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-accent-secondary/5 blur-[120px] rounded-full animate-pulse-glow delay-1000" />
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>

      <div className="relative z-10 container max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        
        {/* Left: Copy */}
        <div className="space-y-8 text-center lg:text-left">
           <motion.div 
             initial={{ opacity: 0, y: 20 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.6 }}
             className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-bold uppercase tracking-widest text-accent-primary"
           >
              <Zap className="w-3 h-3 fill-accent-primary" />
              Surgical NLP Engine v5.4
           </motion.div>

           <motion.h1 
             initial={{ opacity: 0, y: 20 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.6, delay: 0.1 }}
             className="text-6xl md:text-7xl lg:text-8xl font-black text-white tracking-tighter leading-[0.9]"
           >
             Native FX Racks.<br />
             <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-primary to-accent-secondary">Generated from Text.</span>
           </motion.h1>

           <motion.p 
             initial={{ opacity: 0, y: 20 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.6, delay: 0.2 }}
             className="text-xl text-text-dim max-w-xl mx-auto lg:mx-0 leading-relaxed"
           >
             Type "Lo-Fi Tape Saturation Chain" and get a fully mapped <strong>.adg file</strong> instantly.
             <span className="block mt-4 text-white/80 text-sm border-l-2 border-accent-primary pl-4 space-y-1">
                <span className="block">✅ 100% Stock Ableton Devices</span>
                <span className="block">✅ 8 Performance-Ready Macros</span>
                <span className="block">✅ Fully Editable Signal Chain</span>
             </span>
           </motion.p>

           <motion.div 
             initial={{ opacity: 0, y: 20 }}
             animate={{ opacity: 1, y: 0 }}
             transition={{ duration: 0.6, delay: 0.3 }}
             className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start"
           >
              <SignedOut>
                <SignInButton mode="modal">
                     <button className="px-8 py-4 rounded-xl bg-accent-primary text-black font-black uppercase tracking-widest hover:scale-105 transition-transform flex items-center gap-3 shadow-[0_0_30px_rgba(255,124,37,0.3)]">
                        Start Building <ArrowRight className="w-5 h-5" />
                     </button>
                </SignInButton>
              </SignedOut>
              <SignedIn>
                 <Link href="/dashboard">
                     <button className="px-8 py-4 rounded-xl bg-accent-primary text-black font-black uppercase tracking-widest hover:scale-105 transition-transform flex items-center gap-3 shadow-[0_0_30px_rgba(255,124,37,0.3)]">
                        Go to Dashboard <ArrowRight className="w-5 h-5" />
                     </button>
                 </Link>
              </SignedIn>

              <div className="flex -space-x-3">
                 {[1,2,3].map(i => (
                    <div key={i} className="w-10 h-10 rounded-full border-2 border-[#0a0a0b] bg-white/10 backdrop-blur-md flex items-center justify-center text-[10px] font-bold">
                        U{i}
                    </div>
                 ))}
                 <div className="pl-4 flex items-center text-xs font-bold text-text-dim">
                    +2k Producers
                 </div>
              </div>
           </motion.div>
        </div>

        {/* Right: Code Simulation */}
        <motion.div 
             initial={{ opacity: 0, scale: 0.95 }}
             animate={{ opacity: 1, scale: 1 }}
             transition={{ duration: 0.8, delay: 0.4 }}
             className="relative"
        >
            <div className="absolute -inset-1 bg-gradient-to-br from-accent-primary/20 to-accent-secondary/20 rounded-2xl blur-xl" />
            <div className="relative bg-[#0F0F10] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                
                {/* Window Controls */}
                <div className="px-4 py-3 border-b border-white/5 flex items-center gap-2 bg-white/2">
                    <div className="w-3 h-3 rounded-full bg-red-500/20" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/20" />
                    <div className="w-3 h-3 rounded-full bg-green-500/20" />
                    <span className="ml-2 text-[10px] font-mono text-white/30">engine_v5.4.py</span>
                </div>

                {/* Simulated Terminal */}
                <div className="p-6 font-mono text-sm h-[400px] flex flex-col justify-between relative">
                    <div className="space-y-2">
                        <div className="flex items-center gap-2 text-accent-success/80">
                            <span className="text-white/50">$</span>
                            <span>gen_rack "Lo-Fi Texture Rack"</span>
                        </div>
                        
                        <div className="space-y-1 text-white/50 pl-4 border-l border-white/10 ml-1 py-2">
                            <motion.div 
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 }}
                                className="flex items-center gap-2"
                            >
                                <Cpu className="w-3 h-3" /> Parsing Intent: <span className="text-white">"Vintage + Saturation"</span>
                            </motion.div>
                             <motion.div 
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1.8 }}
                                className="flex items-center gap-2"
                            >
                                <Terminal className="w-3 h-3" /> Mapping Macros: <span className="text-accent-secondary">Wobble, Dust, Crunch</span>
                            </motion.div>
                            <motion.div 
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 2.6 }}
                                className="flex items-center gap-2"
                            >
                                <Zap className="w-3 h-3" /> Adding Devices: <span className="text-accent-primary">Vinyl Distortion, Echo, EQ8</span>
                            </motion.div>
                        </div>

                        <motion.div 
                             initial={{ opacity: 0, height: 0 }} 
                             animate={{ opacity: 1, height: "auto" }} 
                             transition={{ delay: 3.5 }}
                             className="mt-4 p-4 rounded-lg bg-white/5 border border-white/10 border-l-4 border-l-accent-success"
                        >
                            <div className="text-[10px] uppercase tracking-widest text-accent-success font-bold mb-2">Build Complete</div>
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 bg-white/10 rounded flex items-center justify-center">
                                    <Zap className="w-6 h-6 text-white" />
                                </div>
                                <div>
                                    <div className="font-bold text-white">Lo-Fi Textures.adg</div>
                                    <div className="text-xs text-white/50">12kb • Ready for Drop</div>
                                </div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Infinite Type Cursor */}
                    <div className="absolute bottom-6 left-6 flex items-center gap-2 text-white/30">
                        <span>&gt;_</span>
                        <motion.span 
                            animate={{ opacity: [0, 1, 0] }}
                            transition={{ repeat: Infinity, duration: 0.8 }}
                            className="w-2 h-4 bg-accent-primary"
                        />
                    </div>
                </div>

            </div>
        </motion.div>
      </div>
    </section>
  );
}
