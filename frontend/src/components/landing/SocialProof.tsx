"use client";

import { motion } from "framer-motion";

const devices = [
  "Amp", "Auto Filter", "Auto Pan", "Beat Repeat", "Cabinet", 
  "Channel EQ", "Chorus-Ensemble", "Compressor", "Corpus", "Delay", 
  "Drum Buss", "Dynamic Tube", "Echo", "EQ Eight", "EQ Three", 
  "Erosion", "Filter Delay", "Flanger", "Frequency Shifter", "Gate", 
  "Glue Compressor", "Grain Delay", "Hybrid Reverb", "Limiter", "Looper", 
  "Multiband Dynamics", "Overdrive", "Pedal", "Phaser-Flanger", "Redux", 
  "Resonators", "Reverb", "Roar", "Saturator", "Shifter", 
  "Spectral Resonator", "Spectral Time", "Tuner", "Utility", 
  "Vinyl Distortion", "Vocoder"
];

export function SocialProof() {
  return (
    <section className="py-10 border-y border-white/5 bg-white/2 overflow-hidden relative z-20">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center gap-12 px-6">
          
          <div className="text-xs font-bold uppercase tracking-widest text-[#71717a] whitespace-nowrap shrink-0">
              Compatible with Live 12.2+ Suite
          </div>

          <div className="flex-1 overflow-hidden relative mask-gradient-x w-full">
              <motion.div 
                className="flex gap-12 w-max"
                animate={{ x: "-50%" }}
                transition={{ 
                    duration: 60, 
                    ease: "linear", 
                    repeat: Infinity 
                }}
              >
                  {[...devices, ...devices].map((d, i) => (
                      <span key={i} className="text-sm font-medium text-white/30 whitespace-nowrap hover:text-white/60 transition-colors cursor-default">
                          {d}
                      </span>
                  ))}
              </motion.div>
              <div className="absolute inset-y-0 left-0 w-24 bg-gradient-to-r from-[#0A0A0B] to-transparent z-10" />
              <div className="absolute inset-y-0 right-0 w-24 bg-gradient-to-l from-[#0A0A0B] to-transparent z-10" />
          </div>

      </div>
    </section>
  );
}
