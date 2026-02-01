import { Zap, Database } from 'lucide-react';

export function Navbar({ deviceCount }) {
  return (
    <nav className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none">
        <div className="glass-panel px-6 py-3 flex items-center gap-6 pointer-events-auto shadow-2xl animate-float-slow">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-accent-primary blur-md opacity-40 animate-pulse-slow"></div>
                <Zap className="text-accent-primary w-5 h-5 relative z-10 fill-current" />
              </div>
              <span className="text-sm font-black tracking-[0.3em] text-white">ADG GEN</span>
            </div>
            <div className="w-px h-4 bg-white/10"></div>
            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-text-dim">
              <Database className="w-3 h-3 text-accent-secondary" />
              <span>{deviceCount} Modules Online</span>
            </div>
        </div>
    </nav>
  );
}
