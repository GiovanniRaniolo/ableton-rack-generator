"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence, Reorder, useDragControls } from "framer-motion";
import { Library, Heart, Search, ChevronRight, Folder, FolderHeart, ArrowLeft, Plus, Loader2, Music, Disc, Edit3, Check, X, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { getUserCollections, getCollectionGenerations, removeFromCollection, updateCollection, deleteCollection, reorderCollectionItems } from "@/app/actions";
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
    
    // Advanced Management States
    const [isEditingName, setIsEditingName] = useState(false);
    const [editNameValue, setEditNameValue] = useState("");
    const [isUpdatingName, setIsUpdatingName] = useState(false);
    const [confirmDeleteColl, setConfirmDeleteColl] = useState(false);
    const [isDeletingColl, setIsDeletingColl] = useState(false);

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
        setEditNameValue(collection.name);
        setRacksLoading(true);
        const racks = await getCollectionGenerations(collection.id);
        setCollectionRacks(racks);
        setRacksLoading(false);
    };

    const handleUpdateName = async () => {
        if (!selectedCollection || !editNameValue.trim() || editNameValue === selectedCollection.name) {
            setIsEditingName(false);
            return;
        }

        setIsUpdatingName(true);
        const res = await updateCollection(selectedCollection.id, editNameValue);
        if (res.success) {
            setSelectedCollection({ ...selectedCollection, name: editNameValue });
            setCollections(prev => prev.map(c => c.id === selectedCollection.id ? { ...c, name: editNameValue } : c));
            setIsEditingName(false);
        } else {
            alert("Failed to update name: " + res.error);
        }
        setIsUpdatingName(false);
    };

    const handleDeleteCollection = async () => {
        if (!selectedCollection) return;
        
        if (!confirmDeleteColl) {
            setConfirmDeleteColl(true);
            setTimeout(() => setConfirmDeleteColl(false), 3000);
            return;
        }

        setIsDeletingColl(true);
        const res = await deleteCollection(selectedCollection.id);
        if (res.success) {
            setCollections(prev => prev.filter(c => c.id !== selectedCollection.id));
            handleBack();
        } else {
            alert("Failed to delete collection: " + res.error);
        }
        setIsDeletingColl(false);
    };

    const handleReorder = async (newOrder: any[]) => {
        setCollectionRacks(newOrder);
        if (selectedCollection) {
            await reorderCollectionItems(selectedCollection.id, newOrder.map(r => r.id));
        }
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
                                    <div className="flex items-center gap-4 mb-2">
                                        {isEditingName ? (
                                            <div className="flex items-center gap-3">
                                                <input 
                                                    autoFocus
                                                    type="text"
                                                    value={editNameValue}
                                                    onChange={(e) => setEditNameValue(e.target.value)}
                                                    onKeyDown={(e) => {
                                                        if (e.key === 'Enter') handleUpdateName();
                                                        if (e.key === 'Escape') setIsEditingName(false);
                                                    }}
                                                    className="bg-white/5 border border-brand-primary/30 rounded-xl px-4 py-2 text-2xl md:text-4xl font-black text-white focus:outline-none focus:border-brand-primary transition-all w-full max-w-md"
                                                />
                                                <button 
                                                    onClick={handleUpdateName}
                                                    disabled={isUpdatingName}
                                                    className="w-12 h-12 rounded-2xl bg-brand-primary text-black flex items-center justify-center hover:scale-105 transition-all shadow-[0_0_20px_rgba(0,255,194,0.3)]"
                                                >
                                                    {isUpdatingName ? <Loader2 className="w-5 h-5 animate-spin" /> : <Check className="w-6 h-6" />}
                                                </button>
                                                <button 
                                                    onClick={() => setIsEditingName(false)}
                                                    className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 text-white flex items-center justify-center hover:bg-white/10 transition-all"
                                                >
                                                    <X className="w-5 h-5" />
                                                </button>
                                            </div>
                                        ) : (
                                            <div className="flex items-center gap-4">
                                                <h1 className="text-3xl md:text-5xl font-black text-white tracking-tight">{selectedCollection.name}</h1>
                                                {!selectedCollection.is_favorite && (
                                                    <div className="flex items-center gap-2">
                                                        <button 
                                                            onClick={() => setIsEditingName(true)}
                                                            className="p-2 rounded-xl bg-white/5 border border-white/10 text-text-dim hover:text-white hover:bg-white/10 transition-all"
                                                            title="Edit Name"
                                                        >
                                                            <Edit3 className="w-4 h-4" />
                                                        </button>
                                                        <button 
                                                            onClick={handleDeleteCollection}
                                                            disabled={isDeletingColl}
                                                            className={cn(
                                                                "p-2 rounded-xl border transition-all flex items-center gap-2",
                                                                confirmDeleteColl 
                                                                    ? "bg-red-500 text-white border-red-500 shadow-[0_0_15px_rgba(239,68,68,0.3)]" 
                                                                    : "bg-white/5 border-white/10 text-text-dim hover:text-red-500 hover:bg-red-500/10 hover:border-red-500/20"
                                                            )}
                                                            title="Delete Collection"
                                                        >
                                                            {isDeletingColl ? (
                                                                <Loader2 className="w-4 h-4 animate-spin" />
                                                            ) : (
                                                                <Trash2 className="w-4 h-4" />
                                                            )}
                                                            {confirmDeleteColl && <span className="text-[10px] font-black uppercase tracking-widest">Delete?</span>}
                                                        </button>
                                                    </div>
                                                )}
                                                {selectedCollection.is_favorite && <Heart className="w-8 h-8 text-red-500 fill-current" />}
                                            </div>
                                        )}
                                    </div>
                                    <div className="flex items-center gap-3">
                                        <span className="text-[10px] font-black uppercase tracking-[0.2em] text-brand-primary">Collection Items</span>
                                        <span className="w-1 h-1 rounded-full bg-white/20" />
                                        <span className="text-sm font-mono text-text-dim">{collectionRacks.length} Racks</span>
                                        {!selectedCollection.is_favorite && collectionRacks.length > 1 && (
                                            <>
                                                <span className="w-1 h-1 rounded-full bg-white/20" />
                                                <span className="text-[9px] font-bold text-brand-primary/60 uppercase tracking-widest">Drag cards to reorder</span>
                                            </>
                                        )}
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
                            <Reorder.Group 
                                axis="y" // Reorder only supports one axis easily for grids, but we can use values
                                values={collectionRacks} 
                                onReorder={handleReorder}
                                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
                            >
                                {collectionRacks.map((rack) => (
                                    <DraggableRackCard 
                                        key={rack.id}
                                        rack={rack}
                                        isFavorite={selectedCollection.is_favorite}
                                        collectionId={selectedCollection.id}
                                        setCollectionRacks={setCollectionRacks}
                                    />
                                ))}
                            </Reorder.Group>
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

function DraggableRackCard({ 
    rack, 
    isFavorite, 
    collectionId, 
    setCollectionRacks 
}: { 
    rack: any, 
    isFavorite: boolean, 
    collectionId: string, 
    setCollectionRacks: React.Dispatch<React.SetStateAction<any[]>> 
}) {
    const dragControls = useDragControls();
    
    return (
        <Reorder.Item 
            key={rack.id} 
            value={rack}
            dragListener={false}
            dragControls={dragControls}
            className="relative"
            whileDrag={{ 
                scale: 1.05, 
                zIndex: 100,
                boxShadow: "0 20px 40px rgba(0,0,0,0.4)"
            }}
            layout
        >
            <RackCard 
                id={rack.id}
                name={rack.creative_name}
                type={rack.rack_data?.type || 'FX'}
                date={new Date(rack.created_at).toLocaleDateString()}
                tags={[]} 
                file_url={rack.file_url}
                rack_data={rack.rack_data}
                prompt={rack.prompt}
                isFavoriteInitial={isFavorite}
                dragControls={!isFavorite ? dragControls : undefined}
                onToggleFavorite={(rackId, isFav) => {
                    if (isFavorite && !isFav) {
                        setCollectionRacks(prev => prev.filter(r => r.id !== rackId));
                    }
                } }
                onToggleCollection={(rackId, collId, isActive) => {
                    if (collectionId === collId && !isActive) {
                        setCollectionRacks(prev => prev.filter(r => r.id !== rackId));
                    }
                }}
                onRemoveFromCollection={async (rackId) => {
                    if (!isFavorite) {
                        const res = await removeFromCollection(rackId, collectionId);
                        if (res.success) {
                            setCollectionRacks(prev => prev.filter(r => r.id !== rackId));
                        }
                    }
                }}
                onDelete={() => {
                    setCollectionRacks(prev => prev.filter(r => r.id !== rack.id));
                }}
            />
        </Reorder.Item>
    );
}
