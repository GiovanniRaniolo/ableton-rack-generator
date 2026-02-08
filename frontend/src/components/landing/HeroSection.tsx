"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Terminal, Cpu, Zap, Activity, Download } from "lucide-react";
import Link from "next/link";
import { SignInButton, SignedOut, SignedIn } from "@clerk/nextjs";

const examples = [
    {
        cmd: 'gen_rack "Deep Dub Techno Chord Rack with Space Echo"',
        intent: "Filtered Delays + Reverb Wash",
        devices: ["Filter Delay", "Hybrid Reverb", "Redux", "EQ Eight"],
        macros: ["Space", "Grit", "Filter Freq", "Feedback"],
        file: "Dub Chords.adg",
        color: "text-cyan-400",
        border: "border-cyan-500/50"
    },
    {
        cmd: 'gen_rack "Aggressive Neuro Bass Processing Chain"',
        intent: "Multiband Distortion + Compression",
        devices: ["Multiband Dynamics", "Saturator", "Pedal", "Limiter"],
        macros: ["Drive", "Crunch", "Squash", "Tone"],
        file: "Neuro Bass Processor.adg",
        color: "text-red-400",
        border: "border-red-500/50"
    },
    {
        cmd: 'gen_rack "Lo-Fi Hip Hop Drum Bus with Vinyl Crackle"',
        intent: "Vintage Warble + Saturation",
        devices: ["Vinyl Distortion", "Drum Buss", "Echo", "Utility"],
        macros: ["Age", "Wobble", "Boom", "Crunch"],
        file: "Lo-Fi Drum Bus.adg",
        color: "text-yellow-400",
        border: "border-yellow-500/50"
    }
];

export function HeroSection() {
    const [index, setIndex] = useState(0);
    const [displayedCmd, setDisplayedCmd] = useState("");
    const ex = examples[index];

    // Cycle examples every 16 seconds (Extensive pause for reading)
    useEffect(() => {
        const timer = setInterval(() => {
            setIndex((prev) => (prev + 1) % examples.length);
        }, 16000);
        return () => clearInterval(timer);
    }, []);

    // Typing Effect for Command
    useEffect(() => {
        setDisplayedCmd("");
        let i = 0;
        const typeTimer = setInterval(() => {
            if (i < ex.cmd.length) {
                setDisplayedCmd(ex.cmd.slice(0, i + 1));
                i++;
            } else {
                clearInterval(typeTimer);
            }
        }, 50); 
        return () => clearInterval(typeTimer);
    }, [index, ex.cmd]);

  return (
    <section className="relative min-h-screen flex items-center pt-20 overflow-hidden">
      
      {/* Background Ambience */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-accent-primary/5 blur-[120px] rounded-full animate-pulse-glow" />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-accent-secondary/5 blur-[120px] rounded-full animate-pulse-glow delay-1000" />
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>

      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">
           
           {/* Left Content */}
           <div className="space-y-8">
             <motion.div 
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ duration: 0.6 }}
               className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-accent-primary"
             >
               <span className="relative flex h-2 w-2">
                 <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-primary opacity-75"></span>
                 <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-primary"></span>
               </span>
               v5.3 Now Available
             </motion.div>

             <motion.h1 
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ duration: 0.6, delay: 0.1 }}
               className="font-black text-white tracking-tighter leading-[0.9]"
             >
               <span className="text-4xl md:text-5xl lg:text-6xl block mb-2">
                   Native <span className="text-white">Ableton Audio FX</span> Racks.
               </span>
               <span className="text-6xl md:text-7xl lg:text-8xl text-transparent bg-clip-text bg-gradient-to-r from-accent-primary to-accent-secondary">Generated from Text.</span>
             </motion.h1>

             <motion.p 
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ duration: 0.6, delay: 0.2 }}
               className="text-xl text-text-dim max-w-xl mx-auto lg:mx-0 leading-relaxed"
             >
               Type "Lo-Fi Tape Saturation Chain" or "Techno Rumble" and get a fully mapped <strong>.adg file</strong> for <span className="text-white">Ableton Live</span> instantly.
               <span className="block mt-6 text-white/80 text-sm border-l-2 border-accent-primary pl-4 space-y-2">
                  <span className="flex items-center gap-2">
                    <Cpu className="w-4 h-4 text-accent-primary" />
                    100% Stock Ableton Devices
                  </span>
                  <span className="flex items-center gap-2">
                    <Activity className="w-4 h-4 text-accent-primary" />
                    8 Performance-Ready Macros
                  </span>
                  <span className="flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-accent-primary" />
                    Fully Editable Signal Chain
                  </span>
               </span>
             </motion.p>
  
             <motion.div 
               initial={{ opacity: 0, y: 20 }}
               animate={{ opacity: 1, y: 0 }}
               transition={{ duration: 0.6, delay: 0.3 }}
               className="flex flex-col sm:flex-row gap-4"
             >
               <SignedOut>
                 <SignInButton mode="modal">
                   <button className="px-8 py-4 bg-accent-primary text-black font-bold text-lg rounded-full hover:scale-105 hover:shadow-[0_0_40px_rgba(255,124,37,0.3)] transition-all flex items-center justify-center gap-2">
                     Start Building Free <ArrowRight className="w-5 h-5" />
                   </button>
                 </SignInButton>
               </SignedOut>
               <SignedIn>
                 <Link href="/dashboard">
                   <button className="px-8 py-4 bg-accent-primary text-black font-bold text-lg rounded-full hover:scale-105 hover:shadow-[0_0_40px_rgba(255,124,37,0.3)] transition-all flex items-center justify-center gap-2">
                     Go to Dashboard <ArrowRight className="w-5 h-5" />
                   </button>
                 </Link>
               </SignedIn>
               <div className="flex items-center gap-[-10px] pl-4">
                  {/* TODO: Re-enable when we have real user numbers */}
                  {/* <div className="flex -space-x-2">
                      {[1,2,3].map(i => (
                          <div key={i} className="w-8 h-8 rounded-full bg-white/10 border-2 border-[#0A0A0B]" />
                      ))}
                  </div>
                  <span className="text-xs text-text-dim ml-4 font-medium">+2k Producers</span> */}
               </div>
             </motion.div>
           </div>

           {/* Right Content - Infinite Loop Terminal */}
           <div className="relative h-[480px] w-full max-w-lg mx-auto lg:ml-auto">
                <AnimatePresence mode="wait">
                    <motion.div 
                        key={index}
                        initial={{ opacity: 0, scale: 0.98 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.98 }}
                        transition={{ duration: 0.3 }}
                        className="absolute inset-0 bg-[#050505] border border-white/10 rounded-xl shadow-2xl overflow-hidden flex flex-col font-mono text-sm"
                    >
                        {/* Terminal Header */}
                        <div className="bg-[#111] px-4 py-2 border-b border-white/5 flex items-center justify-between">
                            <div className="flex gap-2">
                                <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
                                <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
                                <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
                            </div>
                            <div className="text-[10px] text-white/20 font-bold uppercase tracking-widest">
                                bash — 80x24
                            </div>
                        </div>

                        {/* Valid Terminal Content */}
                        <div className="p-6 text-xs md:text-sm text-text-dim flex-1 flex flex-col font-mono">
                            
                            {/* Command Input Line */}
                            <div className="flex flex-wrap gap-2 mb-6 min-h-[40px]">
                                <span className="text-accent-secondary shrink-0">user@adg-engine:~$</span>
                                <span className="text-white break-words">
                                    {displayedCmd}
                                    <span className="inline-block w-2 h-4 bg-white/50 align-middle ml-1 animate-pulse" />
                                </span>
                            </div>
                            
                            {/* Execution Logs - Staggered Delays */}
                            <div className="space-y-4">
                                <motion.div 
                                    initial={{ opacity: 0, x: -5 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 2.5 }}
                                    className="flex gap-3"
                                >
                                    <span className="text-emerald-500">➜</span>
                                    <span>Parsing Intent: <span className="text-white font-bold">"{ex.intent}"</span></span>
                                </motion.div>

                                <motion.div 
                                    initial={{ opacity: 0, x: -5 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 4.0 }}
                                    className="flex gap-3"
                                >
                                    <span className="text-emerald-500">➜</span>
                                    <span>Chain Config: <span className="text-white/80">{ex.devices.join(" -> ")}</span></span>
                                </motion.div>

                                <motion.div 
                                    initial={{ opacity: 0, x: -5 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 5.5 }}
                                    className="flex gap-3"
                                >
                                    <span className="text-emerald-500">➜</span>
                                    <span>Mapping Macros: <span className={`font-bold ${ex.color}`}>{ex.macros.join(", ")}</span></span>
                                </motion.div>
                            </div>

                            {/* Result Output - With Download CTA */}
                            <motion.div 
                                initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 7.0 }}
                                className={`mt-auto p-4 border-l-2 ${ex.border} bg-white/5 font-sans mb-2 group cursor-pointer hover:bg-white/10 transition-colors`}
                            >
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 bg-white/10 rounded flex items-center justify-center">
                                            <Zap className={`w-4 h-4 ${ex.color}`} />
                                        </div>
                                        <div>
                                            <div className="text-white font-bold text-sm">{ex.file}</div>
                                            <div className="text-[10px] text-white/40 uppercase tracking-widest">Ready for Ableton</div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2 px-3 py-1.5 bg-white/10 rounded-md text-xs font-bold text-white group-hover:bg-accent-primary group-hover:text-black transition-colors">
                                        <Download className="w-3 h-3" />
                                        Download .adg
                                    </div>
                                </div>
                            </motion.div>

                        </div>

                    </motion.div>
                </AnimatePresence>

                {/* Glow behind */}
                <div className="absolute -inset-4 bg-accent-primary/10 blur-3xl -z-10 rounded-full opacity-30" />
           </div>

      </div>
    </section>
  );
}
