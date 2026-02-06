import { Database, Coins } from 'lucide-react';
import { Logo } from '../ui/Logo';

interface NavbarProps {
  deviceCount: number;
  credits?: number | null;
}

import Link from 'next/link';

export function Navbar({ deviceCount, credits }: NavbarProps) {
  return (
    <nav className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none">
        <div className="glass-panel px-6 py-3 flex items-center gap-6 pointer-events-auto shadow-2xl animate-float-slow">
            <Link href="/dashboard">
                <Logo className="w-10 h-10 hover:opacity-80 transition-opacity" />
            </Link>
            
            <div className="flex gap-4 px-2">
               <Link href="/dashboard" className="text-[10px] font-bold uppercase tracking-widest text-text-bright hover:text-accent-primary transition-colors">Generator</Link>
               <Link href="/library" className="text-[10px] font-bold uppercase tracking-widest text-text-dim hover:text-white transition-colors">Library</Link>
            </div>

            <div className="w-px h-4 bg-white/10"></div>
            
            {/* Stats Group */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-text-dim">
                <Database className="w-3 h-3 text-accent-secondary" />
                <span>{deviceCount} Modules</span>
              </div>
              
              {credits !== null && credits !== undefined && (
                <>
                  <div className="w-px h-3 bg-white/10"></div>
                  <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-text-bright">
                    <Coins className="w-3 h-3 text-accent-primary" />
                    <span className="text-accent-primary">{credits} Credits</span>
                  </div>
                </>
              )}
            </div>
        </div>
    </nav>
  );
}
