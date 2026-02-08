"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowRight, Terminal, Loader2, Sparkles, Lock, Zap } from "lucide-react";
import { SignInButton, SignedOut, SignedIn } from "@clerk/nextjs";
import Link from "next/link";

export function Simulation() {
  const [prompt, setPrompt] = useState("");
  const [isSimulating, setIsSimulating] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [showResult, setShowResult] = useState(false);

  const handleSimulate = () => {
    if (!prompt) return;
    setIsSimulating(true);
    setLogs([]);
    setShowResult(false);

    const sequence = [
      "Initializing NLP Engine...",
      `Parsing intent: "${prompt}"...`,
      "Identifying devices: [Saturator, Chorus, EQ8]...",
      "Mapping macros: [Tone, Width, Drive]...",
      "Optimizing CPU load...",
      "Generating .adg file...",
      "Done."
    ];

    let delay = 0;
    sequence.forEach((log, i) => {
      delay += Math.random() * 800 + 400; // Random delay between 400-1200ms
      setTimeout(() => {
        setLogs(prev => [...prev, log]);
        if (i === sequence.length - 1) {
            setIsSimulating(false);
            setShowResult(true);
        }
      }, delay);
    });
  };

  return (
    <section id="simulation" className="py-24 px-6 bg-[#0A0A0B] relative overflow-hidden">
        
        {/* Background Glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-accent-primary/5 blur-[120px] rounded-full pointer-events-none" />

        <div className="max-w-4xl mx-auto relative z-10">
            
            <div className="text-center mb-12">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-bold uppercase tracking-widest text-accent-secondary mb-4">
                    <Sparkles className="w-3 h-3" />
                    Interactive Demo
                </div>
                <h2 className="text-4xl md:text-5xl font-black text-white tracking-tighter mb-4">
                    Test the <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-primary to-accent-secondary">Builder.</span>
                </h2>
                <p className="text-text-dim">
                    Type a desired FX Chain. Watch the engine construct it.
                </p>
            </div>

            <div className="glass-panel p-2 rounded-2xl border border-white/10 shadow-2xl bg-[#0F0F10]">
                
                {/* Input Area */}
                <div className="flex gap-2 p-2 relative">
                    <input 
                        type="text" 
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="e.g. Parallel Saturation with filtered delays..."
                        className="w-full bg-white/5 border border-white/5 rounded-xl px-6 py-4 text-white placeholder-white/20 focus:outline-none focus:ring-1 focus:ring-accent-primary/50 font-mono text-sm"
                        onKeyDown={(e) => e.key === "Enter" && handleSimulate()}
                    />
                    <button 
                        onClick={handleSimulate}
                        disabled={isSimulating || !prompt}
                        className="absolute right-4 top-1/2 -translate-y-1/2 px-6 py-2 bg-accent-primary text-black font-bold uppercase tracking-widest text-xs rounded-lg hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center gap-2"
                    >
                        {isSimulating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4" />}
                        Build .adg
                    </button>
                </div>

                {/* Console Output */}
                <div className="h-64 bg-black/50 rounded-xl mt-2 p-6 font-mono text-xs text-green-400 overflow-y-auto custom-scrollbar flex flex-col-reverse relative">
                    
                    {/* Placeholder Text */}
                    {!isSimulating && logs.length === 0 && !showResult && (
                        <div className="absolute inset-0 flex items-center justify-center text-white/20 pointer-events-none">
                            Waiting for request...
                        </div>
                    )}

                    <div className="space-y-1">
                        {logs.map((log, i) => (
                            <motion.div 
                                key={i}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="flex items-center gap-2"
                            >
                                <span className="text-white/30">{">"}</span>
                                {log}
                            </motion.div>
                        ))}
                    </div>
                </div>

                {/* The Trap (Result) */}
                <AnimatePresence>
                    {showResult && (
                        <motion.div 
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 20 }}
                            className="absolute inset-0 z-20 bg-[#0F0F10]/95 backdrop-blur-xl flex flex-col items-center justify-center text-center p-8 rounded-2xl"
                        >
                            <div className="w-16 h-16 bg-accent-primary/10 rounded-2xl flex items-center justify-center mb-6 animate-pulse-glow">
                                <Lock className="w-8 h-8 text-accent-primary" />
                            </div>
                            <h3 className="text-2xl font-bold text-white mb-2">Rack Compiled Successfully</h3>
                            <p className="text-text-dim max-w-sm mb-8">
                                The file <strong>"{prompt}.adg"</strong> is ready for Ableton Live 11/12.
                            </p>
                            
                            <div className="flex gap-4">
                                <SignedOut>
                                    <SignInButton mode="modal">
                                        <button className="px-8 py-3 bg-white text-black font-bold uppercase tracking-widest text-xs rounded-xl hover:scale-105 transition-transform flex items-center gap-2">
                                            Create Account to Download
                                            <ArrowRight className="w-4 h-4" />
                                        </button>
                                    </SignInButton>
                                </SignedOut>
                                <SignedIn>
                                    <Link href="/dashboard">
                                        <button className="px-8 py-3 bg-accent-primary text-black font-bold uppercase tracking-widest text-xs rounded-xl hover:scale-105 transition-transform flex items-center gap-2">
                                            Go to Dashboard
                                            <ArrowRight className="w-4 h-4" />
                                        </button>
                                    </Link>
                                </SignedIn>
                            </div>
                            <p className="mt-4 text-[10px] text-white/30 uppercase tracking-widest">
                                3 Generazioni Gratuite Incluse
                            </p>
                        </motion.div>
                    )}
                </AnimatePresence>

            </div>
        </div>
    </section>
  );
}
