"use client";

import { motion } from "framer-motion";

const devices = [
  "Operator", "Wavetable", "Analog", "Echo", "Hybrid Reverb", "Drum Bus", "Corpus", "Vocoder", "Shifter", "Overdrive", "Saturator", "EQ Eight", "Glue Compressor"
];

export function SocialProof() {
  return (
    <section className="py-10 border-y border-white/5 bg-white/2 overflow-hidden">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center gap-8 px-6">
          
          <div className="text-xs font-bold uppercase tracking-widest text-[#71717a] whitespace-nowrap">
              Compatible with Live 11/12 Suite
          </div>

          <div className="flex-1 overflow-hidden relative mask-gradient-x w-full">
              <div className="flex gap-8 w-max animate-ticker">
                  {[...devices, ...devices].map((d, i) => (
                      <span key={i} className="text-sm font-medium text-white/40">
                          {d}
                      </span>
                  ))}
              </div>
              <div className="absolute inset-y-0 left-0 w-20 bg-gradient-to-r from-[#0A0A0B] to-transparent" />
              <div className="absolute inset-y-0 right-0 w-20 bg-gradient-to-l from-[#0A0A0B] to-transparent" />
          </div>

      </div>
    </section>
  );
}
