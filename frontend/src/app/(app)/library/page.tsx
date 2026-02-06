"use client";

import { useEffect, useState } from 'react';

import { createClient as createSupabaseClient } from '@supabase/supabase-js'; 
import { useUser } from '@clerk/nextjs';
import { Navbar } from '@/components/layout/Navbar';
import { ResultCard } from '@/components/result/ResultCard';
import { Loader2, Download, Calendar, Music, Search } from 'lucide-react';
import Link from 'next/link';
import { getUserLibrary, syncUserProfile } from '@/app/actions';

// Simple client-side supabase access since we enabled RLS
const supabase = createSupabaseClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface Generation {
  id: string;
  creative_name: string;
  prompt: string;
  filename: string;
  file_url: string;
  created_at: string;
  rack_data: any;
}

export default function LibraryPage() {
  const { user, isLoaded } = useUser();
  const [generations, setGenerations] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(true);
  const [credits, setCredits] = useState<number | null>(null);
  const [selectedRack, setSelectedRack] = useState<Generation | null>(null);

  useEffect(() => {
    // Sync credits just in case
    syncUserProfile().then(res => {
         if (res.success) setCredits(res.credits ?? 0);
    });

    if (!isLoaded || !user) return;

    async function fetchHistory() {
      setLoading(true);
      // Use Server Action instead of direct client fetch
      const data = await getUserLibrary();
      setGenerations(data || []);
      setLoading(false);
    }

    fetchHistory();
  }, [user, isLoaded]);

  return (
    <div className="min-h-screen flex flex-col noise-bg bg-bg-deep font-sans selection:bg-accent-primary/30 text-white">
      
      <div className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none">
          {/* We reuse the Stats Navbar but we need to trick it or just use the Link structure */}
           <div className="pointer-events-auto">
                <Navbar deviceCount={generations.length} credits={credits} />
           </div>
      </div>

      <main className="flex-1 w-full max-w-7xl mx-auto px-6 py-32">
        <div className="flex justify-between items-end mb-12">
            <div>
                <h1 className="text-4xl md:text-5xl font-black text-white tracking-tighter mb-4">YOUR ARCHIVE</h1>
                <p className="text-text-dim font-medium max-w-xl">Every rack you've ever generated, safely stored in the cloud.</p>
            </div>
            <div className="hidden md:flex items-center gap-2 px-4 py-2 bg-white/5 rounded-full border border-white/5 text-xs text-text-dim">
                <Search className="w-4 h-4" />
                <span>Encrypted Storage: Active</span>
            </div>
        </div>

        {loading ? (
            <div className="flex justify-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-accent-primary" />
            </div>
        ) : generations.length === 0 ? (
            <div className="text-center py-20 border border-white/5 rounded-3xl bg-white/[0.02]">
                <Music className="w-12 h-12 text-white/10 mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">No racks found</h3>
                <p className="text-text-dim mb-6">You haven't generated anything yet.</p>
                <Link href="/dashboard">
                    <button className="px-6 py-3 bg-white text-black font-black uppercase tracking-widest text-xs rounded-lg hover:scale-105 transition-transform">
                        Create your first Rack
                    </button>
                </Link>
            </div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {generations.map((gen) => (
                    <div key={gen.id} className="group relative bg-[#121212] border border-white/5 rounded-2xl p-6 hover:border-accent-primary/50 transition-all hover:-translate-y-1 flex flex-col">
                        <div className="absolute inset-x-0 bottom-0 h-1 bg-gradient-to-r from-accent-primary to-accent-secondary opacity-0 group-hover:opacity-100 transition-opacity rounded-b-2xl"></div>
                        
                        <div className="flex justify-between items-start mb-4">
                            <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-accent-primary font-black text-sm">
                                ADG
                            </div>
                            <div className="text-[10px] font-mono text-text-dim flex items-center gap-2">
                                <Calendar className="w-3 h-3" />
                                {new Date(gen.created_at).toLocaleDateString()}
                            </div>
                        </div>

                        <h3 className="text-xl font-black text-white tracking-tight mb-2 truncate group-hover:text-accent-primary transition-colors">
                            {gen.creative_name || "Untitled Rack"}
                        </h3>
                        
                        <p className="text-xs text-text-dim line-clamp-2 mb-6 h-8">
                            {gen.prompt}
                        </p>

                        <div className="flex items-center gap-3 border-t border-white/5 pt-4 mt-auto">
                            <button
                                onClick={() => setSelectedRack(gen)}
                                className="flex-1 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-xs font-bold uppercase tracking-widest text-white flex items-center justify-center gap-2 transition-colors"
                            >
                                <Search className="w-3 h-3" />
                                View Details
                            </button>
                            
                            <a 
                                href={gen.file_url} 
                                target="_blank"
                                rel="noopener noreferrer"
                                className="w-10 h-10 flex items-center justify-center bg-accent-primary/10 hover:bg-accent-primary/20 text-accent-primary rounded-lg transition-colors border border-accent-primary/20"
                                title="Download .adg"
                            >
                                <Download className="w-4 h-4" />
                            </a>
                        </div>
                    </div>
                ))}
            </div>
        )}

        {/* DETAILS MODAL */}
        {selectedRack && (
            <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
                <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-[#121212] rounded-3xl border border-white/10 shadow-2xl">
                    <button 
                        onClick={() => setSelectedRack(null)}
                        className="absolute top-4 right-4 z-50 p-2 bg-black/50 hover:bg-white/20 rounded-full text-white transition-colors"
                    >
                        <span className="sr-only">Close</span>
                        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                    
                    {/* Reuse ResultCard but inject the stored rack_data */}
                    <div className="p-8">
                        <ResultCard 
                            result={{...selectedRack.rack_data, file_url: selectedRack.file_url}} 
                            onReset={() => setSelectedRack(null)} // Close modal on reset
                        />
                    </div>
                </div>
            </div>
        )}
      </main>
    </div>
  );
}
