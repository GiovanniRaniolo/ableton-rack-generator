"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Download, MoreHorizontal, FileAudio, Disc, Mic, Zap, Music, Speaker, Sparkles, Cpu, Layers, Settings2, X, Info, Lightbulb, Activity, Trash2, Plus, Heart, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils"; 
import { MacroGrid } from "./MacroGrid"; 
import { deleteGeneration, toggleFavorite } from "@/app/actions";
import { useRouter } from "next/navigation";
import { CollectionSelector } from "../library/CollectionSelector";

interface RackCardProps {
  id: string;
  name: string;
  type: string; 
  date: string;
  tags: readonly string[] | string[];
  file_url?: string;
  rack_data?: any; 
  prompt?: string; // Added prompt prop
  onDelete?: (id: string) => void;
  isFavoriteInitial?: boolean;
  onToggleFavorite?: (id: string, isFav: boolean) => void;
  onToggleCollection?: (id: string, collectionId: string, isActive: boolean) => void;
  onRemoveFromCollection?: (id: string) => void;
}

const getRackTypeStyle = (type: string) => {
    const t = type.toLowerCase();
    if (t.includes("bass")) return { color: "text-orange-500", bg: "bg-orange-500/10", border: "border-orange-500/20", icon: Speaker, gradient: "from-orange-500/20", stripe: "from-orange-500" };
    if (t.includes("drum") || t.includes("perc")) return { color: "text-red-500", bg: "bg-red-500/10", border: "border-red-500/20", icon: Disc, gradient: "from-red-500/20", stripe: "from-red-500" };
    if (t.includes("synth") || t.includes("pad")) return { color: "text-cyan-400", bg: "bg-cyan-400/10", border: "border-cyan-400/20", icon: Music, gradient: "from-cyan-400/20", stripe: "from-cyan-400" };
    if (t.includes("vocal")) return { color: "text-pink-500", bg: "bg-pink-500/10", border: "border-pink-500/20", icon: Mic, gradient: "from-pink-500/20", stripe: "from-pink-500" };
    if (t.includes("fx")) return { color: "text-yellow-400", bg: "bg-yellow-400/10", border: "border-yellow-400/20", icon: Zap, gradient: "from-yellow-400/20", stripe: "from-yellow-400" };
    return { color: "text-text-dim", bg: "bg-white/5", border: "border-white/10", icon: FileAudio, gradient: "from-white/10", stripe: "from-white/20" };
};

export function RackCard({ id, name, type, date, tags, file_url, rack_data, prompt, onDelete, isFavoriteInitial, onToggleFavorite, onToggleCollection, onRemoveFromCollection }: RackCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [showCollections, setShowCollections] = useState(false);
  const [isFavorite, setIsFavorite] = useState(isFavoriteInitial || false);
  const [isTogglingFav, setIsTogglingFav] = useState(false);
  const [confirmRemove, setConfirmRemove] = useState(false);
  const [isRemoving, setIsRemoving] = useState(false);
  const router = useRouter();
  const style = getRackTypeStyle(type);
  const TypeIcon = style.icon;

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirmDelete) {
        setConfirmDelete(true);
        return;
    }

    setIsDeleting(true);
    const res = await deleteGeneration(id);
    if (res.success) {
        if (onDelete) {
            onDelete(id);
        } else {
            router.refresh();
        }
        setIsExpanded(false);
    } else {
        alert("Failed to delete: " + res.error);
    }
    setIsDeleting(false);
  };

  const handleToggleFav = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsTogglingFav(true);
    const res = await toggleFavorite(id);
    if (res.success) {
        const newFav = res.action === 'added';
        setIsFavorite(newFav);
        if (onToggleFavorite) onToggleFavorite(id, newFav);
    }
    setIsTogglingFav(false);
  };

  const handleRemoveFromCollection = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirmRemove) {
        setConfirmRemove(true);
        // Reset confirmation after 3 seconds
        setTimeout(() => setConfirmRemove(false), 3000);
        return;
    }

    if (onRemoveFromCollection) {
        setIsRemoving(true);
        await Promise.resolve(onRemoveFromCollection(id));
        setIsRemoving(false);
        setConfirmRemove(false);
    }
  };

  return (
    <>
    {/* COLLAPSED CARD */}
    <motion.div
      layoutId={`card-container-${id}`}
      onClick={() => setIsExpanded(true)}
      className={cn(
        "relative rounded-3xl border border-white/5 bg-[#121214] hover:bg-[#18181b] hover:border-white/10 cursor-pointer group transition-all duration-500 min-h-[220px] flex flex-col justify-between",
        !showCollections && "overflow-hidden"
      )}
      whileHover={{ y: -5 }}
    >
      {/* Top Gradient Stripe */}
      <div className={cn("absolute top-0 inset-x-0 h-1 bg-gradient-to-r", style.stripe, "to-transparent opacity-80")} />
      
      {/* Content */}
      <div className="p-6">
        <div className="flex justify-between items-start mb-6">
             <div className={cn(
                "w-12 h-12 rounded-2xl flex items-center justify-center border transition-all duration-300",
                style.bg, style.border, style.color
            )}>
              <TypeIcon className="w-6 h-6" />
            </div>
            
            <div className="flex flex-col items-end gap-2">
                <span className="text-xs font-medium font-mono text-white/60 bg-white/5 px-2 py-1 rounded-md border border-white/5">{date}</span>
                
                <div className="flex items-center gap-1.5 opacity-40 group-hover:opacity-100 transition-opacity">
                    <button 
                        onClick={handleToggleFav}
                        disabled={isTogglingFav}
                        className={cn(
                            "p-2 rounded-lg transition-all border border-white/5 bg-white/5",
                            isFavorite 
                                ? "text-red-500 bg-red-500/10 border-red-500/20" 
                                : "text-text-dim hover:text-white hover:bg-white/10"
                        )}
                    >
                        {isTogglingFav ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            <Heart className={cn("w-4 h-4", isFavorite && "fill-current")} />
                        )}
                    </button>

                    <button 
                        onClick={(e) => { e.stopPropagation(); setShowCollections(!showCollections); }}
                        className={cn(
                            "p-2 rounded-lg transition-all border border-white/5 bg-white/5 text-text-dim hover:text-white hover:bg-white/10 hover:border-white/10",
                            showCollections && "bg-brand-primary/10 text-brand-primary border-brand-primary/20 opacity-100"
                        )}
                    >
                        <Plus className="w-4 h-4" />
                    </button>

                    {onRemoveFromCollection && (
                        <button 
                            onClick={handleRemoveFromCollection}
                            disabled={isRemoving}
                            className={cn(
                                "h-8 px-2 rounded-lg transition-all duration-300 border flex items-center gap-2 overflow-hidden",
                                confirmRemove 
                                    ? "bg-brand-primary text-black border-brand-primary/50 w-auto px-3 shadow-[0_0_15px_rgba(0,255,194,0.3)]" 
                                    : "bg-white/5 text-text-dim hover:text-white hover:bg-white/10 border-white/5"
                            )}
                        >
                            {isRemoving ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                            ) : (
                                <X className="w-4 h-4 shrink-0" />
                            )}
                            {confirmRemove && !isRemoving && (
                                <span className="text-[10px] font-black uppercase tracking-tighter whitespace-nowrap">
                                    REMOVE?
                                </span>
                            )}
                        </button>
                    )}
                    {/* ... (delete button continues) */}

                    <button 
                        onClick={handleDelete}
                        disabled={isDeleting}
                        className={cn(
                            "h-8 px-2 rounded-lg transition-all duration-300 border flex items-center gap-2 overflow-hidden",
                            confirmDelete 
                                ? "bg-red-600 text-white border-red-400 w-auto px-3 shadow-[0_0_15px_rgba(239,68,68,0.4)]" 
                                : "bg-white/5 text-red-500 hover:text-red-400 hover:bg-red-500/10 border-white/5"
                        )}
                    >
                        {isDeleting ? (
                            <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <Trash2 className="w-4 h-4 shrink-0" />
                        )}
                        {confirmDelete && !isDeleting && (
                            <span className="text-[10px] font-black uppercase tracking-tighter whitespace-nowrap">
                                CONFIRM?
                            </span>
                        )}
                    </button>
                </div>

                {/* Collection Selector Popover & Overlay */}
                <AnimatePresence>
                    {showCollections && (
                        <>
                            {/* Subtle Overlay Backdrop */}
                            <motion.div 
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                onClick={(e) => { e.stopPropagation(); setShowCollections(false); }}
                                className="fixed inset-0 z-[115] bg-black/20 backdrop-blur-[2px]"
                            />
                            <CollectionSelector 
                                generationId={id} 
                                onClose={() => setShowCollections(false)} 
                                onToggleFavorite={(isFav) => {
                                    setIsFavorite(isFav);
                                    if (onToggleFavorite) onToggleFavorite(id, isFav);
                                }}
                                onToggleCollection={(collId, isActive) => {
                                    if (onToggleCollection) onToggleCollection(id, collId, isActive);
                                }}
                            />
                        </>
                    )}
                </AnimatePresence>
            </div>
        </div>

        <motion.h3 
            layoutId={`title-${id}`}
            className="font-display font-bold text-xl text-white leading-tight mb-2 line-clamp-2 group-hover:text-brand-primary transition-colors"
        >
            {name}
        </motion.h3>
        
        <div className="flex items-center gap-2 mb-4">
             <span className={cn("text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full border", style.color, style.bg, style.border)}>
                 {type}
             </span>
        </div>
      </div>

       {/* Footer: Devices Used (Fixed Height for Alignment) */}
      <div className="px-5 py-4 border-t border-white/5 bg-black/20 h-[72px] flex items-center">
         <div className="grid grid-cols-2 gap-2 w-full">
            {(rack_data?.devices || []).slice(0, 3).map((dev: string, i: number) => (
                <div key={i} className="flex items-center gap-1.5 px-2 py-1 rounded bg-[#1f1f23] border border-white/5 overflow-hidden">
                    <div className="w-1 h-1 rounded-full bg-accent-secondary/80 shadow-[0_0_5px_rgba(0,210,255,0.5)] shrink-0" />
                    <span className="text-[10px] font-medium text-text-main truncate leading-none">{dev}</span>
                </div>
            ))}
            
            {/* 4th Slot: Either the 4th device OR the counter */}
            {(rack_data?.devices || []).length === 4 && (
                 <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-[#1f1f23] border border-white/5 overflow-hidden">
                    <div className="w-1 h-1 rounded-full bg-accent-secondary/80 shadow-[0_0_5px_rgba(0,210,255,0.5)] shrink-0" />
                    <span className="text-[10px] font-medium text-text-main truncate leading-none">{(rack_data?.devices || [])[3]}</span>
                </div>
            )}
            
            {(rack_data?.devices || []).length > 4 && (
                 <div className="flex items-center justify-center gap-1 px-2 py-1 rounded bg-white/5 border border-white/10">
                    <span className="text-[10px] font-bold text-text-dim leading-none">
                        +{(rack_data?.devices || []).length - 3} more
                    </span>
                </div>
            )}

            {/* Empty State / Less than 4 items filler to keep grid stable? No, grid handles it. */}
            {(!rack_data?.devices || rack_data.devices.length === 0) && (
                <div className="col-span-2 flex items-center justify-center gap-2 text-[10px] text-text-dim italic opacity-50">
                    <Activity className="w-3 h-3" />
                    No effects data
                </div>
            )}
         </div>
      </div>
    </motion.div>

    {/* EXPANDED MODAL OVERLAY */}
    <AnimatePresence>
        {isExpanded && (
            <div className="fixed top-0 right-0 bottom-0 left-0 md:left-64 z-[100] flex items-center justify-center p-4 md:p-8">
                <motion.div 
                    initial={{ opacity: 0 }} 
                    animate={{ opacity: 1 }} 
                    exit={{ opacity: 0 }}
                    onClick={() => { setIsExpanded(false); setConfirmDelete(false); }}
                    className="absolute inset-0 bg-black/80 backdrop-blur-md"
                />
                
                <motion.div
                    layoutId={`card-container-${id}`}
                    className={cn(
                        "relative w-full max-w-6xl max-h-[90vh] bg-[#0a0a0b] border border-white/10 rounded-3xl shadow-2xl flex flex-col transition-all duration-300",
                        !showCollections && "overflow-hidden"
                    )}
                >
                    {/* Header */}
                    <div className="relative p-8 md:p-10 border-b border-white/5 bg-[#121214] flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                         <button 
                            onClick={(e) => { e.stopPropagation(); setIsExpanded(false); setConfirmDelete(false); }}
                            className="absolute top-4 right-4 p-2 rounded-full bg-white/5 hover:bg-white/10 text-text-dim hover:text-white transition-colors z-50"
                        >
                            <X className="w-6 h-6" />
                        </button>

                         <div className="flex items-center gap-6">
                            <div className={cn(
                                "w-16 h-16 rounded-3xl flex items-center justify-center border",
                                style.bg, style.border, style.color
                            )}>
                                <TypeIcon className="w-8 h-8" />
                            </div>
                            <div>
                                <motion.h2 
                                    layoutId={`title-${id}`}
                                    className="text-3xl md:text-5xl font-black text-white tracking-tight text-glow mb-2"
                                >
                                    {name}
                                </motion.h2>
                                <div className="flex items-center gap-3">
                                    <span className={cn("text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full border", style.color, style.bg, style.border)}>
                                        {type} Rack
                                    </span>
                                    <span className="text-sm text-white/50 font-mono tracking-tight">{date}</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-3 items-center">
                             <button 
                                onClick={handleToggleFav}
                                disabled={isTogglingFav}
                                className={cn(
                                    "p-3 rounded-xl transition-all border border-white/5 bg-white/5",
                                    isFavorite 
                                        ? "text-red-500 bg-red-500/10 border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.2)]" 
                                        : "text-text-dim hover:text-white hover:bg-white/10"
                                )}
                            >
                                {isTogglingFav ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    <Heart className={cn("w-5 h-5", isFavorite && "fill-current")} />
                                )}
                            </button>

                             <div className="relative">
                                <button 
                                    onClick={(e) => { e.stopPropagation(); setShowCollections(!showCollections); }}
                                    className={cn(
                                        "p-3 rounded-xl transition-all border border-white/5 bg-white/5 text-text-dim hover:text-white hover:bg-white/10 hover:border-white/10",
                                        showCollections && "bg-brand-primary/10 text-brand-primary border-brand-primary/20"
                                    )}
                                >
                                    <Plus className="w-5 h-5" />
                                </button>
                                <AnimatePresence>
                                    {showCollections && (
                                        <CollectionSelector 
                                            generationId={id} 
                                            onClose={() => setShowCollections(false)} 
                                        />
                                    )}
                                </AnimatePresence>
                             </div>

                             <button 
                                onClick={handleDelete}
                                disabled={isDeleting}
                                className={cn(
                                    "px-6 py-3 font-black uppercase tracking-widest text-xs rounded-xl transition-all flex items-center gap-2 border",
                                    confirmDelete 
                                        ? "bg-red-600 text-white border-red-400 shadow-[0_0_20px_rgba(239,68,68,0.5)]" 
                                        : "bg-white/5 text-red-500 hover:bg-red-500/10 hover:text-red-400 border-white/5"
                                )}
                            >
                                {isDeleting ? (
                                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                ) : (
                                    <Trash2 className="w-4 h-4" />
                                )}
                                {confirmDelete ? "CONFIRM DELETE?" : "DELETE RACK"}
                            </button>

                             {file_url ? (
                                <a 
                                    href={file_url} 
                                    target="_blank" 
                                    rel="noopener noreferrer" 
                                    className="px-6 py-3 bg-brand-primary text-black font-black uppercase tracking-widest text-xs rounded-xl hover:scale-105 transition-transform flex items-center gap-2 shadow-[0_0_20px_rgba(0,255,194,0.3)]"
                                >
                                    <Download className="w-4 h-4" />
                                    Download
                                </a>
                            ) : null}
                        </div>
                    </div>

                    {/* Scrollable Content */}
                    <div className="flex-1 overflow-y-auto p-8 md:p-10 custom-scrollbar">
                         <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
                            
                            {/* LEFT COLUMN: INTENT & DEVICES (4 Cols) */}
                            <div className="lg:col-span-4 space-y-10">
                                
                                {/* Prompt Display (NEW) */}
                                {prompt && (
                                    <div className="space-y-4">
                                        <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.2em] flex items-center gap-2">
                                            <Info className="w-4 h-4 text-brand-primary" />
                                            User Prompt
                                        </h3>
                                        <div className="p-4 bg-white/5 rounded-2xl border border-white/5 text-sm text-text-bright italic leading-relaxed">
                                            "{prompt}"
                                        </div>
                                    </div>
                                )}

                                {/* Sonic Signature */}
                                <div className="space-y-4">
                                    <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.2em] flex items-center gap-2">
                                        <Sparkles className="w-4 h-4 text-accent-secondary" />
                                        Sonic Signature
                                    </h3>
                                    <p className="text-xl font-medium text-white leading-relaxed italic opacity-90">
                                        "{rack_data?.sound_intent || 'Processing intent optimized for ' + type}"
                                    </p>
                                </div>

                                 {/* Design Strategy (NEW) */}
                                 {rack_data?.explanation && (
                                     <div className="space-y-4">
                                        <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.2em] flex items-center gap-2">
                                            <Info className="w-4 h-4 text-brand-primary" />
                                            Design Strategy
                                        </h3>
                                        <div className="p-4 bg-white/5 rounded-2xl border border-white/5 text-sm text-text-main leading-relaxed">
                                            {rack_data.explanation}
                                        </div>
                                     </div>
                                 )}

                                {/* Signal Chain */}
                                <div className="space-y-4">
                                    <div className="flex items-center justify-between">
                                        <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.2em] flex items-center gap-2">
                                            <Layers className="w-4 h-4 text-brand-primary" />
                                            Signal Chain
                                        </h3>
                                        {rack_data?.parallel_logic && <span className="text-[10px] font-mono text-brand-primary bg-brand-primary/10 px-2 py-1 rounded">PARALLEL</span>}
                                    </div>
                                    <div className="space-y-2">
                                        {(rack_data?.devices || []).map((dev: string, i: number) => (
                                            <div key={i} className="flex items-center gap-3 p-3 bg-[#121214] rounded-lg border border-white/5">
                                                <div className="w-6 h-6 rounded bg-black flex items-center justify-center text-[10px] text-text-dim font-mono border border-white/10">
                                                    {i + 1}
                                                </div>
                                                <div className="text-sm font-bold text-text-bright">{dev}</div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* RIGHT COLUMN: MACROS (8 Cols) */}
                            <div className="lg:col-span-8 space-y-10">
                                <div className="bg-[#121214] rounded-3xl p-8 border border-white/5 shadow-inner">
                                    <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.2em] flex items-center gap-2 mb-8">
                                        <Settings2 className="w-4 h-4 text-accent-success" />
                                        Macro Matrix
                                    </h3>
                                    {rack_data?.macro_details ? (
                                        <MacroGrid macroDetails={rack_data.macro_details} />
                                    ) : (
                                        <div className="text-center py-10 text-text-dim">Macro data unavailable</div>
                                    )}
                                </div>

                                {/* Pro Tips (NEW) */}
                                {rack_data?.tips && rack_data.tips.length > 0 && (
                                    <div>
                                        <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.2em] flex items-center gap-2 mb-4">
                                            <Lightbulb className="w-4 h-4 text-yellow-400" />
                                            Pro Tips
                                        </h3>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            {rack_data.tips.map((tip: string, idx: number) => (
                                                <div key={idx} className="flex gap-3 text-sm text-text-main leading-relaxed bg-white/5 p-4 rounded-xl border border-white/5">
                                                    <span className="text-accent-secondary text-lg">•</span>
                                                    {tip}
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
        )}
    </AnimatePresence>
    </>
  );
}
