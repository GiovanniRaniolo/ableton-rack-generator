import { MacroDetail } from "@/lib/api";
import { cn } from "@/lib/utils";

interface MacroGridProps {
    macroDetails: MacroDetail[];
}

export function MacroGrid({ macroDetails }: MacroGridProps) {
    // Default 8 macros if empty
    const macros = (macroDetails && macroDetails.length > 0) 
        ? macroDetails 
        : Array.from({length: 8}, (_,i) => ({macro: i+1, name: `Macro ${i+1}`, description: 'Parameter'} as MacroDetail));

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {macros.map((m, i) => (
            <div key={i} className="bg-bg-deep border border-white/5 rounded-2xl p-5 hover:border-accent-success/30 transition-all group hover:-translate-y-1 relative overflow-hidden">
                <div className="absolute inset-0 bg-accent-success/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <div className="flex justify-between items-start mb-2 relative z-10">
                <span className="text-xs font-black text-accent-success uppercase tracking-widest">Knob {m.macro}</span>
                <div className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center group-hover:border-accent-success/50 group-hover:rotate-90 transition-all duration-500">
                    <div className="w-0.5 h-3 bg-white/20 mb-3 rounded-full group-hover:bg-accent-success"></div>
                </div>
                </div>
                <p className="text-base font-black text-white uppercase tracking-wider mb-1 truncate relative z-10">{m.name}</p>
                <p className="text-xs text-text-dim leading-relaxed relative z-10 mb-4 border-b border-white/5 pb-2">
                {m.description}
                </p>
                
                {/* Technical Mapping Truth - HIGH VISIBILITY */}
                <div className="bg-black/40 rounded-lg p-3 relative z-10">
                    <div className="flex items-center gap-2 mb-2">
                    <div className={cn("w-1.5 h-1.5 rounded-full", m.target_device ? 'bg-accent-success shadow-[0_0_8px_rgba(74,222,128,0.5)]' : 'bg-yellow-500')}></div>
                    <span className="text-[10px] font-black uppercase tracking-widest text-text-dim">
                        {m.target_device ? 'AI Connection' : 'Auto-Mapping'}
                    </span>
                    </div>
                    
                    {m.target_device ? (
                        <div className="space-y-1">
                            <div className="flex justify-between items-center text-[10px] uppercase tracking-wider font-mono">
                                <span className="text-text-dim">Device</span>
                                <span className="text-accent-success font-bold">{m.target_device}</span>
                            </div>
                            <div className="flex justify-between items-center text-[10px] uppercase tracking-wider font-mono">
                                <span className="text-text-dim">Param</span>
                                <span className="text-white font-bold">{m.target_parameter}</span>
                            </div>
                        </div>
                    ) : (
                        <div className="text-[10px] text-text-dim italic text-center py-1">
                            System determined best parameter logic
                        </div>
                    )}
                </div>
            </div>
        ))}
        </div>
    );
}
