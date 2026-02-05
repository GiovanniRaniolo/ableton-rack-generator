import { Database } from 'lucide-react';
import { Logo } from '../ui/Logo';

interface NavbarProps {
  deviceCount: number;
}

export function Navbar({ deviceCount }: NavbarProps) {
  return (
    <nav className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none">
        <div className="glass-panel px-6 py-3 flex items-center gap-6 pointer-events-auto shadow-2xl animate-float-slow">
            <Logo className="w-10 h-10" />
            <div className="w-px h-4 bg-white/10"></div>
            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-text-dim">
              <Database className="w-3 h-3 text-accent-secondary" />
              <span>{deviceCount} Modules Online</span>
            </div>
        </div>
    </nav>
  );
}
