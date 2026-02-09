"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Download, ChevronDown, ChevronUp, Sparkles, Layers, Settings2, Cpu, Zap, Maximize2, Minimize2, Disc, Speaker, Music, X } from "lucide-react";
import { cn } from "@/lib/utils";

// Real Generation Data
const showcaseData = [
  {
    id: "techno-rumble",
    title: "Techno Core: Industrial Rumble",
    filename: "Techno_Rumble.adg",
    type: "Drums",
    prompt: "Create a dark, industrial Techno Rumble kick processor. Split the low end at 150Hz and keep it mono and compressed. On the high band, add a large Reverb with 5s decay, followed by a saturator driving 12dB to crush the tail, and an Auto Filter cutting at 300Hz to remove mud...",
    desc: "Creates a dark, industrial techno rumble effect, emphasizing the kick drum's presence while adding a gritty reverb tail.",
    devices: ["EQ Eight", "Utility", "Multiband Dynamics", "Hybrid Reverb", "Saturator", "Auto Filter"],
    macros: ["Rumble Size", "Dirt", "Mud Cut", "Kick Punch", "Sub Focus", "Decay Tail", "Drive", "Filter Freq"],
    tips: ["Automate 'Rumble Size' for massive drops.", "Use 'Mud Cut' to clean up the mix during busy sections."],
    intent: "Dark, Industrial, Gritty",
    explanation: "Splits the kick into lows (mono, compressed) and highs (reverb, saturation, filter). Sets long Reverb decay to create the rumble.",
    color: "text-orange-500",
    bg: "bg-orange-500/10",
    border: "border-orange-500/20",
    glow: "shadow-[0_0_30px_-5px_rgba(249,115,22,0.3)]",
    primaryAccent: "bg-orange-500"
  },
  {
    id: "vhs-pad",
    title: "Haunted VHS Pad",
    filename: "VHS_Pad.adg",
    type: "Synth",
    prompt: "Build a vintage tape wobble effect for nostalgic pads. Use a fast LFO modulating a Delay time for pitch instability (wow and flutter). Add a Vinyl Distortion for mechanical crackle, a Redux for 12-bit artifacts...",
    desc: "Vintage, degraded, and ethereal pad with tape warble and artifacts. Uses Grain Delay for spectral texture.",
    devices: ["Delay", "Vinyl Distortion", "Redux", "Grain Delay", "Utility"],
    macros: ["VHS Age", "Tape Warble", "Memory Loss", "Crackle Vol", "Downsample", "Spray Amount", "Pitch Mod", "Output Gain"],
    tips: ["Automate the 'Tape Warble' Macro for dramatic changes.", "Combine with a high-pass filter for a lo-fi aesthetic."],
    intent: "Vintage, Degraded, Ethereal",
    explanation: "Delay and Grain Delay are used to create pitch and timing instability, Vinyl Distortion adds mechanical sounds, and Redux introduces downsampling artifacts.",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    border: "border-amber-500/20",
    glow: "shadow-[0_0_30px_-5px_rgba(251,191,36,0.3)]",
    primaryAccent: "bg-amber-500"
  },
  {
    id: "neuro-bass",
    title: "NeuroSplitter Bass",
    filename: "Neuro_Bass.adg",
    type: "Bass",
    prompt: "Generate a Neurofunk Reesebass splitter rack. Split the signal into 3 bands: Low (Clean Sine), Mids (processed with Corpus set to 'Tube' for metallic resonance), Highs (Stereo Widened Chorus). Add an Overdrive on the mids...",
    desc: "Aggressive Neurofunk Bass. Signal is split into three bands to surgically process them and create a modern reese sound.",
    devices: ["Multiband Dynamics", "EQ Eight", "Corpus", "Overdrive", "Chorus-Ensemble", "Auto Filter"],
    macros: ["Reese Speed", "Metal Resonance", "Stereo Width", "Band Split", "Tube Drive", "Filter Cutoff", "Chorus Mix", "Sub Gain"],
    tips: ["Automate the Metal Resonance macro for wild variations.", "Adjust the input gain on the Multiband Dynamics for different clipping characteristics."],
    intent: "Aggressive, Focus Midrange, Wide Highs",
    explanation: "Signal is split into three bands to surgically process them. Corpus adds metallic resonance to the mids, while Chorus widens the highs.",
    color: "text-purple-500",
    bg: "bg-purple-500/10",
    border: "border-purple-500/20",
    glow: "shadow-[0_0_30px_-5px_rgba(168,85,247,0.3)]",
    primaryAccent: "bg-purple-500"
  },
  {
    id: "dub-techno",
    title: "Echospace Cathedral",
    filename: "Dub_Techno.adg",
    type: "Ambience",
    prompt: "Deep Dub Techno texture generator. Process incoming stabs with a Ping Pong Delay set to 3/16 timing and 95% feedback. Feed it into a large Hybrid Reverb with 'Freeze' capability. Use an Auto Filter with an LFO...",
    desc: "Deep, atmospheric dub techno space with rhythmic echo and filter sweeps. Cathedrals of Sound.",
    devices: ["Ping Pong Delay", "Hybrid Reverb", "Auto Filter", "Echo", "Utility"],
    macros: ["Space", "Freeze", "Filter Movement", "Dub Feedback", "Delay Time", "Verb Mix", "LFO Rate", "Width"],
    tips: ["Automate Space and Filter Movement macros for transitions.", "Experiment with different LFO shapes in Auto Filter for variations."],
    intent: "Deep, Atmospheric, Rhythmic",
    explanation: "Sets a foundation with 3/16 delay, creates an immense space with the reverb and a rhythmic base using the LFO on the Auto Filter.",
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
    border: "border-cyan-500/20",
    glow: "shadow-[0_0_30px_-5px_rgba(34,211,238,0.3)]",
    primaryAccent: "bg-cyan-500"
  }
];

export function Showcase() {
    const [expandedId, setExpandedId] = useState<string | null>(null);
    const selectedItem = showcaseData.find(item => item.id === expandedId);

    return (
        <section className="py-32 relative overflow-hidden bg-[#0A0A0B]">
            {/* Background Ambience */}
            <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
            <div className="absolute top-1/4 -left-[10%] w-[800px] h-[800px] bg-brand-primary/5 blur-[150px] rounded-full pointer-events-none" />
            
            <div className="max-w-7xl mx-auto px-6 relative z-10 space-y-24">
                
                {/* Section Header */}
                <div className="text-center space-y-6 max-w-4xl mx-auto">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-md">
                        <Zap className="w-4 h-4 text-brand-primary animate-pulse" />
                        <span className="text-xs font-black uppercase tracking-[0.2em] text-white">Live Evidence</span>
                    </div>
                    <h2 className="text-5xl md:text-7xl font-black text-white tracking-tighter leading-[0.9]">
                        Real Results.<br/>
                        <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-white/40">
                             Zero Mockups.
                        </span>
                    </h2>
                    <p className="text-xl text-text-dim max-w-2xl mx-auto leading-relaxed">
                        These racks were generated by our engine in <span className="text-white font-bold">seconds</span>. 
                        Click to explode the DNA, or download the <strong>.adg</strong> to test it in Ableton Live.
                    </p>
                </div>

                {/* 2-Column Grid Layout */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {showcaseData.map((item) => (
                        <ShowcaseCard 
                            key={item.id} 
                            data={item} 
                            onClick={() => setExpandedId(item.id)}
                        />
                    ))}
                </div>

            </div>

            {/* MODAL EXPANSION */}
            <AnimatePresence>
                {expandedId && selectedItem && (
                    <ShowcaseModal 
                        data={selectedItem} 
                        onClose={() => setExpandedId(null)} 
                    />
                )}
            </AnimatePresence>
        </section>
    );
}

function ShowcaseCard({ data, onClick }: { data: any, onClick: () => void }) {
    return (
        <motion.div 
            layoutId={`card-${data.id}`}
            onClick={onClick}
            className="group relative cursor-pointer h-full"
            whileHover={{ y: -5 }}
            transition={{ duration: 0.3 }}
        >
            {/* Glass Panel Container */}
            <div className="relative glass-panel p-1 border-gradient overflow-hidden rounded-[2rem] h-full">
                {/* Hover Glow */}
                <div className={`absolute -top-40 -right-40 w-80 h-80 ${data.bg} blur-[120px] opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none`}></div>
                
                <div className="bg-[#0e0e10] rounded-[1.8rem] overflow-hidden relative z-10 w-full h-full flex flex-col justify-between p-8 border border-white/5 group-hover:border-white/10 transition-colors">
                    
                    <div className="space-y-6">
                        {/* Header: Type Badge */}
                        <div className="flex justify-between items-start">
                            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full bg-black/40 border border-white/5 text-[10px] font-black uppercase tracking-widest ${data.color}`}>
                                {data.type === "Drums" && <Disc className="w-3 h-3" />}
                                {data.type === "Bass" && <Speaker className="w-3 h-3" />}
                                {data.type === "Synth" && <Music className="w-3 h-3" />}
                                {data.type === "Ambience" && <Sparkles className="w-3 h-3" />}
                                <span>{data.type} Rack</span>
                            </div>
                            <Maximize2 className="w-5 h-5 text-white/20 group-hover:text-white transition-colors" />
                        </div>

                        {/* Title */}
                        <div>
                             <motion.h3 
                                layoutId={`title-${data.id}`}
                                className="text-2xl font-black text-white tracking-tighter leading-tight group-hover:text-brand-primary transition-colors duration-300"
                            >
                                {data.title}
                            </motion.h3>
                            <div className="mt-2 text-xs font-mono text-text-dim flex items-center gap-2">
                                <span>{data.filename}</span>
                                <span className="w-1 h-1 rounded-full bg-white/20"></span>
                                <span>{data.devices.length} Devices</span>
                            </div>
                        </div>
                        
                        {/* Prompt Snippet */}
                        <div className="bg-black/40 rounded-xl p-4 border border-white/5 font-mono text-[11px] text-text-dim leading-relaxed relative overflow-hidden group/prompt">
                            <div className={`absolute left-0 top-0 bottom-0 w-1 ${data.primaryAccent} opacity-50`}></div>
                            <span className={data.color}>$ &gt; </span>
                            <span className="text-white/60 line-clamp-3">{data.prompt}</span>
                        </div>
                    </div>

                    <div className="mt-8 pt-6 border-t border-white/5 flex items-center justify-between">
                         <button className={`text-xs font-bold uppercase tracking-widest text-white/50 group-hover:text-white transition-colors flex items-center gap-2`}>
                            Inspect DNA 
                        </button>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}

function ShowcaseModal({ data, onClose }: { data: any, onClose: () => void }) {
    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 md:p-8">
            <motion.div 
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }} 
                exit={{ opacity: 0 }}
                onClick={onClose}
                className="absolute inset-0 bg-black/90 backdrop-blur-md"
            />
            
            <motion.div
                layoutId={`card-${data.id}`}
                className="relative w-full max-w-6xl max-h-[90vh] bg-[#0a0a0b] border border-white/10 rounded-3xl shadow-2xl overflow-hidden flex flex-col z-10"
            >
                {/* Modal Header */}
                <div className="relative p-8 md:p-10 border-b border-white/5 bg-[#121214] flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                        <button 
                        onClick={(e) => { e.stopPropagation(); onClose(); }}
                        className="absolute top-4 right-4 p-2 rounded-full bg-white/5 hover:bg-white/10 text-text-dim hover:text-white transition-colors z-50"
                    >
                        <X className="w-6 h-6" />
                    </button>

                    <div className="flex items-center gap-6">
                        <div className={`w-16 h-16 rounded-3xl flex items-center justify-center border ${data.bg} ${data.border} ${data.color}`}>
                            {data.type === "Drums" && <Disc className="w-8 h-8" />}
                            {data.type === "Bass" && <Speaker className="w-8 h-8" />}
                            {data.type === "Synth" && <Music className="w-8 h-8" />}
                            {data.type === "Ambience" && <Sparkles className="w-8 h-8" />}
                        </div>
                        <div>
                            <motion.h2 
                                layoutId={`title-${data.id}`}
                                className="text-3xl md:text-5xl font-black text-white tracking-tight text-glow mb-2"
                            >
                                {data.title}
                            </motion.h2>
                            <div className="flex items-center gap-3">
                                <span className={`text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full border ${data.color} ${data.bg} ${data.border}`}>
                                    {data.type} Rack
                                </span>
                                <span className="text-sm text-white/50 font-mono tracking-tight">{data.filename}</span>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-3 pr-12 md:pr-0">
                            <a 
                            href={`/showcase/${data.filename}`} 
                            download
                            className={`px-6 py-3 bg-brand-primary text-black font-black uppercase tracking-widest text-xs rounded-xl hover:scale-105 transition-transform flex items-center gap-2 shadow-[0_0_20px_rgba(0,255,194,0.3)]`}
                            onClick={(e) => e.stopPropagation()}
                        >
                            <Download className="w-4 h-4" />
                            Download
                        </a>
                    </div>
                </div>

                {/* Modal Content Scroll */}
                <div className="flex-1 overflow-y-auto p-8 md:p-10 custom-scrollbar">
                     <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                        {/* Left: Logic & Topology */}
                        <div className="space-y-10">
                            
                            {/* Sonic Signature & Strategy */}
                            <div className="space-y-6">
                                <h4 className={`text-xs font-black text-text-dim uppercase tracking-[0.3em] flex items-center gap-2`}>
                                    <Sparkles className={`w-4 h-4 ${data.color}`} /> Sonic Signature
                                </h4>
                                <p className="text-xl font-medium text-white italic opacity-90 leading-relaxed">
                                    "{data.intent}"
                                </p>
                                
                                <div className="space-y-3 pt-4">
                                    <h4 className={`text-xs font-black text-text-dim uppercase tracking-[0.3em] flex items-center gap-2`}>
                                        <Cpu className={`w-4 h-4 ${data.color}`} /> Design Strategy
                                    </h4>
                                    <div className="p-5 bg-white/5 rounded-xl border border-white/5 font-mono text-sm text-text-dim leading-relaxed">
                                        {data.explanation}
                                    </div>
                                </div>
                            </div>

                            {/* Prompt */}
                            <div className="space-y-4">
                                <h4 className={`text-xs font-black text-text-dim uppercase tracking-[0.3em] flex items-center gap-2`}>
                                    <Zap className={`w-4 h-4 ${data.color}`} /> Generation Prompt
                                </h4>
                                <div className="bg-black/40 rounded-xl p-6 border border-white/5 font-mono text-xs text-text-dim leading-relaxed relative overflow-hidden">
                                     <div className={`absolute left-0 top-0 bottom-0 w-1 ${data.primaryAccent} opacity-50`}></div>
                                     <span className={data.color}>$ &gt; </span>
                                     <span className="text-white/90">{data.prompt}</span>
                                </div>
                            </div>

                            {/* Signal Chain */}
                            <div className="space-y-4">
                                <h4 className={`text-xs font-black text-text-dim uppercase tracking-[0.3em] flex items-center gap-2`}>
                                    <Layers className={`w-4 h-4 ${data.color}`} /> Signal Chain
                                </h4>
                                <div className="flex flex-wrap items-center gap-3">
                                    {data.devices.map((dev: string, i: number) => (
                                        <div key={i} className="flex items-center gap-2 group/dev">
                                            <div className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg hover:border-white/30 transition-colors">
                                                <span className="text-[10px] font-black text-text-dim/50">{i + 1}</span>
                                                <span className="text-xs font-bold text-white uppercase tracking-wide group-hover/dev:text-brand-primary transition-colors">
                                                    {dev}
                                                </span>
                                            </div>
                                            {/* Arrow Connector */}
                                            {i !== data.devices.length - 1 && (
                                                <div className="text-white/10">
                                                    <ChevronDown className="w-4 h-4 -rotate-90" />
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Right: Macros & Tips */}
                        <div className="space-y-10">
                            <div>
                                <h4 className={`text-xs font-black text-text-dim uppercase tracking-[0.3em] flex items-center gap-2 mb-8`}>
                                    <Settings2 className={`w-4 h-4 ${data.color}`} /> Macro Controls
                                </h4>
                                <div className="grid grid-cols-2 gap-4">
                                    {data.macros.map((macro: string, i: number) => (
                                        <div key={i} className="bg-bg-deep border border-white/5 rounded-xl p-4 flex items-center gap-4 hover:border-white/20 transition-all group/macro cursor-pointer">
                                            {/* Knob Container: Rotates on Hover */}
                                            <div className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center transition-all duration-700 ease-out group-hover/macro:rotate-[135deg] group-hover/macro:border-white/30 relative bg-[#1A1A1C]">
                                                {/* Indicator Pointer */}
                                                <div className={`w-1 h-3 ${data.primaryAccent} rounded-full absolute top-1`}></div>
                                            </div>
                                            
                                            <div className="overflow-hidden">
                                                <div className={`text-[10px] font-black uppercase tracking-wider ${data.color} mb-1`}>Knob {i + 1}</div>
                                                <div className="text-sm font-bold text-white truncate">{macro}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {data.tips && (
                                <div className="pt-8 border-t border-white/5">
                                    <h4 className="text-[10px] font-black text-text-dim uppercase tracking-[0.3em] mb-4">Pro Tips</h4>
                                    <div className="grid grid-cols-1 gap-3">
                                        {data.tips.map((tip: string, idx: number) => (
                                            <div key={idx} className="bg-bg-deep border border-white/5 rounded-xl p-4 flex gap-4 hover:border-white/20 transition-all group/tip">
                                                <div className={`mt-1.5 flex-shrink-0 w-1.5 h-1.5 rounded-full ${data.primaryAccent} group-hover/tip:scale-125 transition-transform`} />
                                                <p className="text-sm text-text-dim group-hover/tip:text-white transition-colors leading-relaxed">
                                                    {tip}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                     </div>
                </div>
            </motion.div>
        </div>
    );
}
