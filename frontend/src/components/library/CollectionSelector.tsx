"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Heart, Plus, Search, Check, FolderPlus, X, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { 
    getUserCollections, 
    createCollection, 
    toggleFavorite, 
    addToCollection, 
    removeFromCollection, 
    getGenerationCollections 
} from "@/app/actions";

interface Collection {
    id: string;
    name: string;
    is_favorite: boolean;
}

interface CollectionSelectorProps {
    generationId: string;
    onClose: () => void;
    onToggleFavorite?: (isFav: boolean) => void;
    onToggleCollection?: (collectionId: string, isActive: boolean) => void;
}

export function CollectionSelector({ generationId, onClose, onToggleFavorite, onToggleCollection }: CollectionSelectorProps) {
    const [collections, setCollections] = useState<Collection[]>([]);
    const [activeCollectionIds, setActiveCollectionIds] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");
    const [isCreating, setIsCreating] = useState(false);
    const [newCollectionName, setNewCollectionName] = useState("");
    const [isProcessing, setIsProcessing] = useState<string | null>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === "Escape") onClose();
        };

        const handleClickOutside = (e: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
                onClose();
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        window.addEventListener("mousedown", handleClickOutside);
        return () => {
            window.removeEventListener("keydown", handleKeyDown);
            window.removeEventListener("mousedown", handleClickOutside);
        };
    }, [onClose]);

    useEffect(() => {
        async function loadData() {
            setLoading(true);
            const [allColls, activeIds] = await Promise.all([
                getUserCollections(),
                getGenerationCollections(generationId)
            ]);
            setCollections(allColls);
            setActiveCollectionIds(activeIds);
            setLoading(false);
        }
        loadData();
    }, [generationId]);

    const handleToggleFavorite = async () => {
        setIsProcessing('favorite');
        const res = await toggleFavorite(generationId);
        if (res.success) {
            const favColl = collections.find(c => c.is_favorite);
            const newFav = res.action === 'added';
            if (onToggleFavorite) onToggleFavorite(newFav);
            if (favColl) {
                if (newFav) {
                    setActiveCollectionIds(prev => [...prev, favColl.id]);
                } else {
                    setActiveCollectionIds(prev => prev.filter(id => id !== favColl.id));
                }
            }
        }
        setIsProcessing(null);
    };

    const handleToggleCollection = async (collectionId: string) => {
        const isActive = activeCollectionIds.includes(collectionId);
        setIsProcessing(collectionId);
        
        if (isActive) {
            const res = await removeFromCollection(generationId, collectionId);
            if (res.success) {
                setActiveCollectionIds(prev => prev.filter(id => id !== collectionId));
                if (onToggleCollection) onToggleCollection(collectionId, false);
            }
        } else {
            const res = await addToCollection(generationId, collectionId);
            if (res.success) {
                setActiveCollectionIds(prev => [...prev, collectionId]);
                if (onToggleCollection) onToggleCollection(collectionId, true);
            }
        }
        setIsProcessing(null);
    };

    const handleCreateCollection = async () => {
        if (!newCollectionName.trim()) return;
        setIsProcessing('create');
        const res = await createCollection(newCollectionName);
        if (res.success && res.data) {
            setCollections(prev => [...prev, res.data]);
            setNewCollectionName("");
            setIsCreating(false);
            // Auto add to the newly created collection
            await handleToggleCollection(res.data.id);
        }
        setIsProcessing(null);
    };

    const filteredCollections = collections.filter(c => 
        !c.is_favorite && c.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const isFavorite = collections.find(c => c.is_favorite && activeCollectionIds.includes(c.id));

    return (
        <motion.div 
            ref={containerRef}
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            className="absolute right-0 top-12 w-72 z-[120] bg-[#121214]/95 backdrop-blur-2xl border border-white/10 rounded-2xl shadow-2xl overflow-hidden flex flex-col"
            onClick={(e) => e.stopPropagation()}
        >
            {/* Header / Quick Fav */}
            <div className="p-4 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
                <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-text-dim">Add to Collection</h3>
                <button 
                    onClick={handleToggleFavorite}
                    className={cn(
                        "flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[10px] font-bold transition-all uppercase tracking-wider",
                        isFavorite 
                            ? "bg-red-500/20 text-red-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]" 
                            : "bg-white/5 text-text-dim hover:text-white hover:bg-white/10"
                    )}
                >
                    {isProcessing === 'favorite' ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    ) : (
                        <Heart className={cn("w-3.5 h-3.5", isFavorite && "fill-current")} />
                    )}
                    {isFavorite ? 'Favorited' : 'Favorite'}
                </button>
            </div>

            {/* Search */}
            <div className="p-3 border-b border-white/5">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-white/30" />
                    <input 
                        type="text"
                        placeholder="Search collections..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-black/40 border border-white/5 rounded-xl py-2 pl-9 pr-4 text-xs text-white placeholder:text-white/20 focus:outline-none focus:border-brand-primary/50 transition-colors"
                    />
                </div>
            </div>

            {/* List */}
            <div className="max-h-56 overflow-y-auto custom-scrollbar py-2">
                {loading ? (
                    <div className="flex justify-center py-8">
                        <Loader2 className="w-6 h-6 animate-spin text-brand-primary/50" />
                    </div>
                ) : collections.length === 0 && !isCreating ? (
                    <div className="text-center py-8 px-4">
                        <p className="text-[10px] text-text-dim uppercase tracking-wider mb-4 leading-relaxed">No collections found. Create your first one below.</p>
                    </div>
                ) : (
                    <div className="space-y-0.5 px-2">
                        {filteredCollections.map((coll) => (
                            <button
                                key={coll.id}
                                onClick={() => handleToggleCollection(coll.id)}
                                className={cn(
                                    "w-full flex items-center justify-between p-2.5 rounded-xl transition-all group",
                                    activeCollectionIds.includes(coll.id) 
                                        ? "bg-brand-primary/10 text-brand-primary" 
                                        : "hover:bg-white/5 text-text-main hover:text-white"
                                )}
                            >
                                <div className="flex items-center gap-3 overflow-hidden">
                                     <div className={cn(
                                        "w-2 h-2 rounded-full shrink-0 transition-all",
                                        activeCollectionIds.includes(coll.id) ? "bg-brand-primary" : "bg-white/10 group-hover:bg-white/20"
                                     )} />
                                     <span className="text-xs font-medium truncate">{coll.name}</span>
                                </div>
                                {isProcessing === coll.id ? (
                                    <Loader2 className="w-3.5 h-3.5 animate-spin opacity-50" />
                                ) : activeCollectionIds.includes(coll.id) ? (
                                    <Check className="w-3.5 h-3.5" />
                                ) : null}
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {/* Actions / Create */}
            <div className="p-3 border-t border-white/5 bg-black/40 mt-auto">
                <AnimatePresence mode="wait">
                    {!isCreating ? (
                        <motion.button
                            key="add-btn"
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -5 }}
                            onClick={() => setIsCreating(true)}
                            className="w-full flex items-center justify-center gap-2 p-2.5 rounded-xl border border-dashed border-white/10 text-text-dim hover:text-white hover:border-white/20 hover:bg-white/5 transition-all text-xs font-bold"
                        >
                            <Plus className="w-4 h-4" />
                            Create Collection
                        </motion.button>
                    ) : (
                        <motion.div
                            key="create-form"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="space-y-3"
                        >
                            <div className="flex items-center justify-between mb-1">
                                <span className="text-[9px] font-black uppercase tracking-[0.2em] text-brand-primary">New Collection</span>
                                <button onClick={() => setIsCreating(false)} className="text-text-dim hover:text-white">
                                    <X className="w-3 h-3" />
                                </button>
                            </div>
                            <input 
                                autoFocus
                                type="text"
                                placeholder="Summer Vibes, Dark Techno..."
                                value={newCollectionName}
                                onChange={(e) => setNewCollectionName(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') handleCreateCollection();
                                    if (e.key === 'Escape') setIsCreating(false);
                                }}
                                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white placeholder:text-white/20 focus:outline-none focus:border-brand-primary/50 transition-colors"
                            />
                            <button
                                onClick={handleCreateCollection}
                                disabled={!newCollectionName.trim() || isProcessing === 'create'}
                                className="w-full bg-brand-primary hover:bg-brand-primary/90 text-black font-black uppercase tracking-widest text-[10px] py-2.5 rounded-xl transition-all shadow-[0_0_15px_rgba(0,255,194,0.3)] disabled:opacity-50 disabled:shadow-none flex items-center justify-center gap-2"
                            >
                                {isProcessing === 'create' ? <Loader2 className="w-4 h-4 animate-spin" /> : <FolderPlus className="w-4 h-4" />}
                                Confirm Create
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </motion.div>
    );
}
