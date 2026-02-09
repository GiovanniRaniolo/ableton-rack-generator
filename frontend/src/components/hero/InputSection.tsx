"use client";



import { useState, useEffect } from 'react';
import { RefreshCw, Sparkles, Music, Zap, Box, Wind, Waves, Radio, Activity } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Logo } from '../ui/Logo';
import { motion, AnimatePresence } from 'framer-motion';

const ALL_TEMPLATES = [
  { id: 'lofi', icon: <Radio className="w-4 h-4" />, name: 'Lo-Fi Cassette', prompt: 'Vintage tape saturation with wow/flutter, erosion and heavy compression' },
  { id: 'space', icon: <Box className="w-4 h-4" />, name: 'Deep Space', prompt: 'Atmospheric reverb with shimmer, grain delay and spectral time' },
  { id: 'vocal', icon: <Music className="w-4 h-4" />, name: 'Vocal Air', prompt: 'Clean vocal chain with OTT, de-esser, EQ Eight high-shelf and plate reverb' },
  { id: 'dub', icon: <Waves className="w-4 h-4" />, name: 'Dub Echoes', prompt: 'Rhythmic tape delay with filter modulation and spring reverb tail' },
  { id: 'glitch', icon: <Activity className="w-4 h-4" />, name: 'Glitch Stutter', prompt: 'Beat repeat chaos with redux, frequency shifter and gate' },
  { id: 'crunch', icon: <Zap className="w-4 h-4" />, name: 'Drum Crunch', prompt: 'Aggressive parallel compression with drum buss, roar and limiter' },
  { id: 'texture', icon: <Wind className="w-4 h-4" />, name: 'Texture Pad', prompt: 'Evolving granular texture with resonator, chorus and auto-pan' },
  { id: 'master', icon: <Sparkles className="w-4 h-4" />, name: 'Mix Polish', prompt: 'Subtle mastering chain with glue compressor, mid-side EQ and saturator' },
];

interface InputSectionProps {
    prompt: string;
    setPrompt: (value: string) => void;
    handleGenerate: () => void;
    isGenerating: boolean;
    error: string;
    userName?: string;
}

export function InputSection({ prompt, setPrompt, handleGenerate, isGenerating, error, userName = "Creator" }: InputSectionProps) {
  // Carousel State
  const [visibleIndices, setVisibleIndices] = useState([0, 1, 2]);
  const [greeting, setGreeting] = useState("Hello");

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) setGreeting("Good morning");
    else if (hour >= 12 && hour < 18) setGreeting("Good afternoon");
    else setGreeting("Good evening");
  }, []);

  // Smoother rotation: rotate ONE card at a time every 4 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setVisibleIndices(prev => {
        const next = [...prev];
        // Rotate the first item to the end of the list relative to the current set
        // Actually, let's just shift the window by 1
        const lastIndex = prev[prev.length - 1];
        const newIndex = (lastIndex + 1) % ALL_TEMPLATES.length;
        return [prev[1], prev[2], newIndex];
      });
    }, 4000); // Slower interval
    return () => clearInterval(interval);
  }, []);

  return (
      <section className="w-full max-w-4xl mx-auto space-y-8 animate-in fade-in zoom-in duration-700 flex flex-col items-center">
        
        {/* AI Greeting Header */}
        <div className="text-center space-y-2">
            <h2 className="text-3xl md:text-4xl font-semibold text-white tracking-tight">
                {greeting}, <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-primary to-accent-secondary">{userName}</span>
            </h2>
            <p className="text-text-dim text-lg">What sound are we designing today?</p>
        </div>

        {/* Main Input Area */}
        <div className="relative group w-full">
          <div className="absolute -inset-0.5 bg-gradient-to-r from-brand-primary via-accent-secondary to-brand-primary rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000 animate-pulse-slow"></div>
          <div className="relative bg-[#0a0a0b] p-1.5 rounded-2xl border border-white/10 shadow-2xl">
            <div className="bg-[#121214] rounded-xl p-1 relative overflow-hidden transition-all duration-300 focus-within:bg-[#18181b]">
               <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the sound you want... (e.g., 'Dubstep bass with growl')"
                className="w-full h-32 bg-transparent border-none focus:ring-0 outline-none text-xl font-medium placeholder:text-white/10 text-white p-6 resize-none leading-relaxed"
                autoFocus
              />
              
              {/* Generate Button Wrapper */}
              <div className="flex justify-end px-4 pb-4">
                 <button
                  onClick={handleGenerate}
                  disabled={isGenerating || !prompt.trim()}
                  className="px-6 py-2.5 bg-white text-black font-black uppercase tracking-widest text-xs rounded-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center gap-2 shadow-[0_0_20px_rgba(255,255,255,0.15)] hover:shadow-[0_0_30px_rgba(255,255,255,0.3)]"
                 >
                   {isGenerating ? <RefreshCw className="animate-spin w-4 h-4"/> : <Sparkles className="w-4 h-4"/>}
                   Generate Rack
                 </button>
              </div>
            </div>
          </div>
        </div>

        {/* Animated Suggested Prompts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 w-full">
             <AnimatePresence mode='popLayout'>
                {visibleIndices.map((idx) => {
                    const t = ALL_TEMPLATES[idx];
                    return (
                        <motion.button 
                            key={t.id} 
                            layout
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            transition={{ duration: 0.4 }}
                            onClick={() => setPrompt(t.prompt)}
                            className="text-left group relative p-4 rounded-xl bg-white/5 border border-white/5 hover:border-white/20 transition-all duration-300 hover:bg-white/10 overflow-hidden h-28 flex flex-col justify-between"
                        >
                            <div className="absolute inset-0 bg-gradient-to-br from-transparent to-black/50 opacity-0 group-hover:opacity-100 transition-opacity" />
                            
                            <div className="relative z-10 flex items-center gap-3">
                                <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center text-brand-primary group-hover:text-white group-hover:bg-brand-primary transition-all duration-300 shadow-inner">
                                    {t.icon}
                                </div>
                                <h3 className="text-base font-bold text-white group-hover:text-brand-primary transition-colors">{t.name}</h3>
                            </div>
                            
                            <p className="relative z-10 text-xs text-white/80 line-clamp-2 leading-relaxed group-hover:text-white pl-1">{t.prompt}</p>
                        </motion.button>
                    );
                })}
            </AnimatePresence>
        </div>

        {error && (
            <div className="flex justify-center">
                <p className="text-red-400 font-mono text-xs bg-red-500/10 px-5 py-2.5 rounded-lg border border-red-500/20 flex items-center gap-2">
                    <div className="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse" />
                    {error}
                </p>
            </div>
        )}
      </section>
  );
}
