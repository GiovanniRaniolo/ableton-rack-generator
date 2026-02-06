"use client";

import { Download, RefreshCw, Sparkles, Layers, Settings2, Cpu } from 'lucide-react';
import { api, GenerateResponse } from '@/lib/api';
import { MacroGrid } from './MacroGrid';
import { cn } from '@/lib/utils';

interface ResultCardProps {
    result: GenerateResponse;
    onReset: () => void;
}

export function ResultCard({ result, onReset }: ResultCardProps) {
  if (!result) return null;

  return (
    <div className="animate-in fade-in slide-in-from-bottom-24 duration-1000">
        <div className="relative glass-panel p-1 border-gradient overflow-hidden group">
        {/* Background Glows */}
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-accent-primary/20 blur-[150px] pointer-events-none animate-pulse-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-accent-secondary/20 blur-[150px] pointer-events-none animate-pulse-slow" style={{animationDelay: '1s'}}></div>

        <div className="bg-[#0a0a0b]/80 rounded-[1.8rem] overflow-hidden relative z-10">
            
            {/* HEADER ROW */}
            <header className="p-10 md:p-14 border-b border-white/5 flex flex-col md:flex-row justify-between items-start md:items-center gap-8 relative overflow-hidden">
                <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
                
                <div className="space-y-4 relative z-10">
                    <div className="inline-flex items-center gap-3 px-3 py-1 rounded-full bg-accent-primary/10 border border-accent-primary/20 text-accent-primary text-[10px] font-black uppercase tracking-[0.2em]">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-primary opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-primary"></span>
                    </span>
                    ADG Generated
                    </div>
                    <h2 className="text-5xl md:text-7xl font-black text-white tracking-tighter leading-none text-glow">
                    {result.creative_name}
                    </h2>
                    <p className="font-mono text-text-dim text-sm">{result.filename}</p>
                </div>

                <div className="flex flex-col gap-3 relative z-10">
                <button 
                    onClick={() => {
                        if (result.file_url) {
                            window.open(result.file_url, '_blank');
                        } else {
                            api.downloadRack(result.filename);
                        }
                    }}
                    className="px-8 py-4 bg-accent-primary hover:bg-[#ff904d] text-black font-black uppercase tracking-[0.2em] text-xs rounded-full shadow-[0_0_30px_-5px_rgba(255,124,37,0.4)] hover:shadow-[0_0_50px_-10px_rgba(255,124,37,0.6)] hover:scale-105 transition-all active:scale-95 flex items-center gap-3 cursor-pointer"
                >
                    <Download className="w-4 h-4" />
                    Download .adg
                </button>
                <button 
                    onClick={onReset}
                    className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 text-white font-bold uppercase tracking-[0.2em] text-xs rounded-full transition-all flex items-center justify-center gap-3 backdrop-blur-md cursor-pointer"
                >
                    <RefreshCw className="w-4 h-4" />
                    New Rack
                </button>
                </div>
            </header>

            {/* CORE GRID */}
            <div className="grid grid-cols-1 lg:grid-cols-2">
                
                {/* LEFT: INTENT & DEVICES */}
                <div className="p-10 md:p-14 border-b lg:border-b-0 lg:border-r border-white/5 space-y-12">
                    <div className="space-y-6">
                    <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                        <Sparkles className="w-4 h-4 text-accent-secondary" />
                        Sonic Signature
                    </h3>
                    <p className="text-xl md:text-2xl font-medium text-white leading-relaxed italic opacity-90">
                        "{result.sound_intent}"
                    </p>
                    <div className="space-y-4">
                        <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                           <Cpu className="w-4 h-4 text-accent-primary" />
                           Design Strategy
                        </h3>
                        <div className="p-6 bg-white/5 rounded-2xl border border-white/5 backdrop-blur-sm">
                            <p className="text-sm text-text-main font-mono leading-relaxed">
                            {result.explanation}
                            </p>
                        </div>
                    </div>
                    </div>

                    <div className="space-y-8">
                        <div className="flex items-center justify-between">
                        <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                            <Layers className="w-4 h-4 text-accent-primary" />
                            Signal Topology
                        </h3>
                        {result.parallel_logic && <span className="text-[10px] font-mono text-accent-primary bg-accent-primary/10 px-2 py-1 rounded">PARALLEL</span>}
                        </div>

                        <div className="space-y-4">
                        {result.devices.map((dev, i) => (
                            <div key={i} className="group flex items-center gap-4 relative">
                            {i !== result.devices.length - 1 && (
                                <div className="absolute left-[19px] top-10 w-0.5 h-6 bg-white/10 group-hover:bg-accent-primary/50 transition-colors"></div>
                            )}
                            <div className="w-10 h-10 rounded-xl bg-bg-deep border border-white/10 flex items-center justify-center text-text-dim font-black text-sm group-hover:border-accent-primary group-hover:text-accent-primary group-hover:shadow-[0_0_15px_rgba(255,124,37,0.2)] transition-all z-10">
                                {i + 1}
                            </div>
                            <div className="flex-1 h-12 bg-white/[0.02] border border-white/[0.05] rounded-xl flex items-center px-6 text-sm font-bold tracking-wider text-text-bright uppercase group-hover:bg-white/[0.05] transition-all">
                                {dev}
                            </div>
                            </div>
                        ))}
                        </div>
                    </div>
                </div>

                {/* RIGHT: MACRO ENGINEERING */}
                <div className="p-10 md:p-14 bg-black/20">
                    <div className="flex items-center justify-between mb-10">
                    <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                        <Settings2 className="w-4 h-4 text-accent-success" />
                        Macro Matrix
                    </h3>
                    <div className="flex gap-1">
                        <div className="w-1 h-1 rounded-full bg-accent-success animate-pulse"></div>
                        <div className="w-1 h-1 rounded-full bg-accent-success animate-pulse delay-75"></div>
                        <div className="w-1 h-1 rounded-full bg-accent-success animate-pulse delay-150"></div>
                    </div>
                    </div>

                    <MacroGrid macroDetails={result.macro_details} />
                    
                    {result.tips && result.tips.length > 0 && (
                    <div className="mt-12 pt-8 border-t border-white/5">
                        <p className="text-[10px] font-black text-text-dim uppercase tracking-[0.2em] mb-4">Pro Tips</p>
                        <div className="space-y-3">
                            {result.tips.slice(0, 2).map((tip, idx) => (
                                <div key={idx} className="flex gap-3 text-sm text-text-main leading-relaxed opacity-60 hover:opacity-100 transition-opacity">
                                <span className="text-accent-secondary">•</span>
                                {tip}
                                </div>
                            ))}
                        </div>
                    </div>
                    )}
                </div>
            </div>
        </div>
        </div>
    </div>
  );
}
