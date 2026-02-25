"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Library, Heart, Search, ChevronRight, Folder, FolderHeart, ArrowLeft, Plus, Loader2, Music, Disc } from "lucide-react";
import { cn } from "@/lib/utils";
import { getUserCollections, getCollectionGenerations, removeFromCollection } from "@/app/actions";
import { RackCard } from "@/components/result/RackCard";

interface Collection {
    id: string;
    name: string;
    is_favorite: boolean;
    item_count?: number;
}

export default function CollectionsPage() {
    const [collections, setCollections] = useState<Collection[]>([]);
    const [selectedCollection, setSelectedCollection] = useState<Collection | null>(null);
    const [collectionRacks, setCollectionRacks] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [racksLoading, setRacksLoading] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");

    useEffect(() => {
        async function loadCollections() {
            setLoading(true);
            const data = await getUserCollections();
            setCollections(data);
            setLoading(false);
        }
        loadCollections();
    }, []);

    const handleSelectCollection = async (collection: Collection) => {
        setSelectedCollection(collection);
        setRacksLoading(true);
        const racks = await getCollectionGenerations(collection.id);
        setCollectionRacks(racks);
        setRacksLoading(false);
    };

    const handleBack = () => {
        setSelectedCollection(null);
        setCollectionRacks([]);
    };

    const filteredCollections = collections.filter(c => 
        c.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <Loader2 className="w-10 h-10 animate-spin text-brand-primary/50 mb-4" />
                <p className="text-text-dim text-sm font-medium tracking-widest uppercase">Loading your collections...</p>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <AnimatePresence mode="wait">
                {!selectedCollection ? (
                    <motion.div 
                        key="collections-grid"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="space-y-8"
                    >
                        {/* Header */}
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
                            <div>
                                <h1 className="text-4xl font-black text-white tracking-tight mb-2 flex items-center gap-3">
                                    <Library className="w-10 h-10 text-brand-primary" />
                                    Collections
                                </h1>
                                <p className="text-text-dim max-w-lg">Manage your favorite racks and organized playlists.</p>
                            </div>

                            <div className="relative w-full md:w-72">
                                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                                <input 
                                    type="text"
                                    placeholder="Find a collection..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full bg-[#121214] border border-white/5 rounded-2xl py-3 pl-11 pr-4 text-sm text-white focus:outline-none focus:border-brand-primary/50 transition-colors"
                                />
                            </div>
                        </div>

                        {/* Collections Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                            {filteredCollections.map((coll) => (
                                <motion.div
                                    key={coll.id}
                                    whileHover={{ y: -5 }}
                                    onClick={() => handleSelectCollection(coll)}
                                    className={cn(
                                        "group relative bg-[#121214] border border-white/5 rounded-3xl p-6 cursor-pointer overflow-hidden transition-all hover:bg-[#18181b] hover:border-white/10",
                                        coll.is_favorite && "border-red-500/10 hover:border-red-500/20"
                                    )}
                                >
                                    <div className="flex flex-col gap-6 relative z-10">
                                        <div className={cn(
                                            "w-14 h-14 rounded-2xl flex items-center justify-center border transition-all duration-500",
                                            coll.is_favorite 
                                                ? "bg-red-500/10 border-red-500/20 text-red-500 group-hover:scale-110 shadow-[0_0_20px_rgba(239,68,68,0.1)]" 
                                                : "bg-white/5 border-white/10 text-brand-primary group-hover:scale-110 shadow-[0_0_20px_rgba(0,255,194,0.1)]"
                                        )}>
                                            {coll.is_favorite ? <Heart className="w-7 h-7 fill-current" /> : <Folder className="w-7 h-7" />}
                                        </div>

                                        <div>
                                            <h3 className="text-xl font-bold text-white mb-1 group-hover:text-brand-primary transition-colors">{coll.name}</h3>
                                            <p className="text-[10px] font-black uppercase tracking-widest text-text-dim">Collection</p>
                                        </div>
                                    </div>

                                    {/* Decorative Icon */}
                                    <div className="absolute -bottom-4 -right-4 opacity-[0.03] group-hover:opacity-[0.07] transition-opacity duration-500">
                                        {coll.is_favorite ? <FolderHeart size={120} /> : <Library size={120} />}
                                    </div>
                                </motion.div>
                            ))}

                            {/* Empty State / Prompt */}
                            {filteredCollections.length === 0 && (
                                <div className="col-span-full py-20 text-center border border-dashed border-white/5 rounded-3xl bg-white/[0.02]">
                                    <p className="text-text-dim italic">No collections found matching your search.</p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                ) : (
                    <motion.div 
                        key="collection-detail"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className="space-y-8"
                    >
                        {/* Detail Header */}
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                            <div className="flex items-center gap-6">
                                <button 
                                    onClick={handleBack}
                                    className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-white hover:bg-white/10 transition-all hover:-translate-x-1"
                                >
                                    <ArrowLeft className="w-5 h-5" />
                                </button>
                                <div>
                                    <div className="flex items-center gap-3 mb-1">
                                        <h1 className="text-3xl md:text-5xl font-black text-white tracking-tight">{selectedCollection.name}</h1>
                                        {selectedCollection.is_favorite && <Heart className="w-8 h-8 text-red-500 fill-current" />}
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <span className="text-[10px] font-black uppercase tracking-[0.2em] text-brand-primary">Collection Items</span>
                                        <span className="w-1 h-1 rounded-full bg-white/20" />
                                        <span className="text-sm font-mono text-text-dim">{collectionRacks.length} Racks</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Detail Content */}
                        {racksLoading ? (
                             <div className="flex flex-col items-center justify-center py-20">
                                <Loader2 className="w-8 h-8 animate-spin text-brand-primary/50 mb-4" />
                            </div>
                        ) : collectionRacks.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                                {collectionRacks.map((rack) => (
                                    <RackCard 
                                        key={rack.id}
                                        id={rack.id}
                                        name={rack.creative_name}
                                        type={rack.rack_data?.type || 'FX'}
                                        date={new Date(rack.created_at).toLocaleDateString()}
                                        tags={[]} // Collections view doesn't need tags necessarily or can fetch them
                                        file_url={rack.file_url}
                                        rack_data={rack.rack_data}
                                        prompt={rack.prompt}
                                        isFavoriteInitial={selectedCollection.is_favorite}
                                        onToggleFavorite={(rackId, isFav) => {
                                            if (selectedCollection.is_favorite && !isFav) {
                                                setCollectionRacks(prev => prev.filter(r => r.id !== rackId));
                                            }
                                        } }
                                        onToggleCollection={(rackId, collId, isActive) => {
                                            if (selectedCollection.id === collId && !isActive) {
                                                setCollectionRacks(prev => prev.filter(r => r.id !== rackId));
                                            }
                                        }}
                                        onRemoveFromCollection={async (rackId) => {
                                            if (!selectedCollection.is_favorite) {
                                                const res = await removeFromCollection(rackId, selectedCollection.id);
                                                if (res.success) {
                                                    setCollectionRacks(prev => prev.filter(r => r.id !== rackId));
                                                }
                                            }
                                        }}
                                        onDelete={() => {
                                            setCollectionRacks(prev => prev.filter(r => r.id !== rack.id));
                                        }}
                                    />
                                ))}
                            </div>
                        ) : (
                            <div className="py-32 flex flex-col items-center justify-center border border-dashed border-white/5 rounded-[40px] bg-white/[0.02]">
                                <div className="w-20 h-20 rounded-3xl bg-white/5 flex items-center justify-center mb-6">
                                    <Music className="w-10 h-10 text-white/20" />
                                </div>
                                <p className="text-white/40 font-medium mb-1">This collection is empty</p>
                                <p className="text-text-dim text-sm max-w-xs text-center">Add some racks from the Generator or Archive to see them here.</p>
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
