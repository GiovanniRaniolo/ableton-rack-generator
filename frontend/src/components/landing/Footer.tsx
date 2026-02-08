"use client";

import Link from "next/link";
import { Logo } from "@/components/ui/Logo";

export function Footer() {
  return (
    <footer className="bg-[#0A0A0B] border-t border-white/5 py-16 px-6">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-12">
            
            <div className="space-y-4">
                <div className="flex items-center gap-2">
                    <Logo className="w-6 h-6 grayscale opacity-50" showText={false} />
                    <span className="font-bold tracking-tight text-white/50 text-sm">ADG<span className="text-white/30">BUILDER</span></span>
                </div>
                <p className="text-text-dim text-xs leading-relaxed max-w-xs">
                    The first NPL-to-Rack engine. 
                    We parse your intent and map native Ableton devices for you.
                </p>
                <div className="text-[10px] text-white/20 uppercase tracking-widest">
                    &copy; 2026 Dark Studio AI.
                </div>
            </div>

            <div>
                <h4 className="font-bold text-white text-sm mb-6">Product</h4>
                <ul className="space-y-4 text-xs text-text-dim">
                    <li><Link href="#" className="hover:text-white transition-colors">Features</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Pricing</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Changelog</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Roadmap</Link></li>
                </ul>
            </div>

            <div>
                 <h4 className="font-bold text-white text-sm mb-6">Resources</h4>
                 <ul className="space-y-4 text-xs text-text-dim">
                    <li><Link href="#" className="hover:text-white transition-colors">Documentation</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">API Reference</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Community Discord</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Blog</Link></li>
                 </ul>
            </div>

            <div>
                 <h4 className="font-bold text-white text-sm mb-6">Legal</h4>
                 <ul className="space-y-4 text-xs text-text-dim">
                    <li><Link href="#" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Terms of Service</Link></li>
                    <li><Link href="#" className="hover:text-white transition-colors">Cookie Policy</Link></li>
                 </ul>
            </div>

        </div>
    </footer>
  );
}
