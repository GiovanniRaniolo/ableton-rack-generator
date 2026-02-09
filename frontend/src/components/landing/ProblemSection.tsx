"use client";

import { motion } from "framer-motion";
import { MousePointer2, Repeat, LightbulbOff } from "lucide-react";

const problems = [
  {
    icon: MousePointer2,
    title: "Macro Mapping Hell",
    desc: "Stop right-clicking 'Map to Macro' 16 times per rack. We map the most important parameters automatically.",
    color: "text-red-400",
    bg: "bg-red-400/10",
    border: "border-red-400/20"
  },
  {
    icon: Repeat,
    title: "Chain Fatigue",
    desc: "Dragging the same 3 stock plugins onto every track? Let AI suggest new signal chains you wouldn't think of.",
    color: "text-yellow-400",
    bg: "bg-yellow-400/10",
    border: "border-yellow-400/20"
  },
  {
    icon: LightbulbOff,
    title: "Empty Rack Syndrome",
    desc: "Don't start from an empty device view. Get a fully routed, functional FX Rack as your starting point.",
    color: "text-blue-400",
    bg: "bg-blue-400/10",
    border: "border-blue-400/20"
  }
];

export function ProblemSection() {
  return (
    <section className="py-24 px-6 bg-[#0A0A0B] relative">
      <div className="max-w-6xl mx-auto">
        
        <div className="text-center mb-16 space-y-4">
            <h2 className="text-3xl md:text-5xl font-black text-white tracking-tighter">
                Stop building <span className="text-brand-primary">infrastructure.</span> Start mixing.
            </h2>
            <p className="text-text-dim max-w-2xl mx-auto">
                We handle the routing, mapping, and device selection. You just turn the knobs.
            </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {problems.map((p, i) => (
                <motion.div 
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.1 }}
                    className={`p-8 rounded-2xl border ${p.border} ${p.bg} hover:bg-opacity-20 transition-all group`}
                >
                    <div className={`w-12 h-12 rounded-lg ${p.bg} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                        <p.icon className={`w-6 h-6 ${p.color}`} />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-3">{p.title}</h3>
                    <p className="text-text-dim text-sm leading-relaxed">{p.desc}</p>
                </motion.div>
            ))}
        </div>

      </div>
    </section>
  );
}
