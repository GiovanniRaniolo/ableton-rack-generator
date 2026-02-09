"use client";

import { motion } from "framer-motion";
import { Brain, Database, FileCode, CheckCircle2, ShieldCheck, Zap } from "lucide-react";

const specs = [
  {
    icon: Brain,
    title: "Surgical NLP v7",
    subtitle: "Semantic DSP Translation",
    metrics: ["Context-Aware Parsing", "Psychoacoustic Mapping", "Genre-Specific Logic"],
    desc: "Our engine bridges the gap between language and sound. It translates abstract adjectives like 'warmth' or 'punch' into precise, floating-point DSP values.",
    color: "text-purple-400",
    bg: "bg-purple-500/10",
    border: "border-purple-500/20"
  },
  {
    icon: Database,
    title: "Acoustic Neural Grid",
    subtitle: "1,500+ Mapped Nodes",
    metrics: ["60+ Device Architectures", "Dynamic Signal Flow", "Parametric Constraints"],
    desc: "A vast topology of mapped parameters ensures every knob turn is musical. We don't just randomise values; we model the relationship between devices.",
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
    border: "border-cyan-500/20"
  },
  {
    icon: FileCode,
    title: "Native Core Engine",
    subtitle: "Pure .adg Architecture",
    metrics: ["Zero CPU Overhead", "Native DSP Code", "Latency-Free Execution"],
    desc: "We generate native code that runs directly on Live's internal engine. No VST wrappers, no external plugins—just pure, optimized native performance.",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/20"
  }
];

export function TechSpecs() {
  return (
    <section className="py-24 relative overflow-hidden bg-[#0A0A0B]">
      
      {/* Background Grid */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-to-b from-[#0A0A0B] via-transparent to-[#0A0A0B] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        
        {/* Section Header */}
        <div className="text-center mb-20">
            <motion.div 
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-mono text-brand-primary mb-6"
            >
                <Zap className="w-3 h-3" />
                <span>ENGINE ARCHITECTURE</span>
            </motion.div>
            
            <motion.h2 
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 }}
                className="text-4xl md:text-5xl font-black text-white mb-6 tracking-tight"
            >
                Not a Randomizer.<br/>
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-white/50">Scientific Precision.</span>
            </motion.h2>

            <motion.p 
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.2 }}
                className="text-lg text-text-dim max-w-2xl mx-auto"
            >
                Most AI tools hallucinate parameters. We built a deterministic engine that bridges the gap between <span className="text-white">Natural Language</span> and <span className="text-white">DSP Code</span>.
            </motion.p>
        </div>

        {/* Blueprint Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {specs.map((item, i) => (
                <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.2 }}
                    className={`group relative p-8 rounded-2xl bg-[#111] border border-white/5 hover:border-white/10 transition-all duration-500 hover:shadow-2xl overflow-hidden`}
                >
                    {/* Hover Glow */}
                    <div className={`absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-b from-transparent to-${item.color.split('-')[1]}-500/5`} />

                    {/* Header */}
                    <div className="relative z-10 flex flex-col items-start gap-6">
                        <div className={`p-4 rounded-xl ${item.bg} ${item.border} border`}>
                            <item.icon className={`w-8 h-8 ${item.color}`} />
                        </div>
                        
                        <div>
                            <h3 className="text-2xl font-bold text-white mb-1 group-hover:text-brand-primary transition-colors">
                                {item.title}
                            </h3>
                            <div className={`text-xs font-mono font-bold uppercase tracking-widest ${item.color} opacity-80`}>
                                {item.subtitle}
                            </div>
                        </div>

                        <p className="text-text-dim leading-relaxed text-sm">
                            {item.desc}
                        </p>

                        {/* Metrics List */}
                        <div className="w-full space-y-3 pt-6 border-t border-white/5">
                            {item.metrics.map((m, j) => (
                                <div key={j} className="flex items-center gap-3 text-sm text-white/70">
                                    <CheckCircle2 className={`w-4 h-4 ${item.color} shrink-0`} />
                                    <span>{m}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </motion.div>
            ))}
        </div>

      </div>
    </section>
  );
}
