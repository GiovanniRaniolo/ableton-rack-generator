"use client";

import { useEffect, useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { Loader2, Music, Search } from 'lucide-react';
import Link from 'next/link';
import { getUserLibrary } from '@/app/actions';
import { RackCard } from '@/components/result/RackCard'; // New Card

interface Generation {
  id: string;
  creative_name: string;
  prompt: string;
  filename: string;
  file_url: string;
  created_at: string;
  rack_data: any;
}

export default function ArchivePage() {
  const { user, isLoaded } = useUser();
  const [generations, setGenerations] = useState<Generation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isLoaded || !user) return;
    async function fetchHistory() {
      setLoading(true);
      const data = await getUserLibrary();
      setGenerations(data || []);
      setLoading(false);
    }
    fetchHistory();
  }, [user, isLoaded]);

  return (
    <div className="min-h-screen text-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-end border-b border-white/5 pb-8">
            <div className="space-y-2">
                <h1 className="text-4xl md:text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-white/50 tracking-tighter">
                    ARCHIVE
                </h1>
                <p className="text-text-dim text-lg">Your generated sonic history.</p>
            </div>
            
            <div className="flex items-center gap-2 px-4 py-2 bg-white/5 rounded-full border border-white/5 text-xs text-text-dim font-mono">
                <Search className="w-4 h-4" />
                <span>{generations.length} RACKS STORED</span>
            </div>
        </div>

        {loading ? (
            <div className="flex justify-center py-32">
                <Loader2 className="w-10 h-10 animate-spin text-brand-primary" />
            </div>
        ) : generations.length === 0 ? (
            <div className="text-center py-32 border border-white/5 rounded-3xl bg-white/[0.02] flex flex-col items-center">
                <Music className="w-16 h-16 text-white/5 mb-6" />
                <h3 className="text-2xl font-bold text-white mb-2">Archive Empty</h3>
                <p className="text-text-dim mb-8">Start generating to build your collection.</p>
                <Link href="/dashboard">
                    <button className="px-8 py-3 bg-white text-black font-black uppercase tracking-widest text-xs rounded-xl hover:scale-105 transition-transform">
                        Go to Generator
                    </button>
                </Link>
            </div>
        ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 auto-rows-max">
                {generations.map((gen) => {
                    // Infer type from prompt or name if possible, default to "FX"
                    let type = "FX";
                    const promptLower = gen.prompt.toLowerCase();
                    if (promptLower.includes("bass")) type = "Bass";
                    else if (promptLower.includes("drum") || promptLower.includes("kick") || promptLower.includes("snare")) type = "Drums";
                    else if (promptLower.includes("pad") || promptLower.includes("synth") || promptLower.includes("lead")) type = "Synth";
                    else if (promptLower.includes("vocal") || promptLower.includes("voice")) type = "Vocals";

                    // Extract some tags from prompt logic (simplified)
                    const tags = gen.prompt.split(' ').filter(w => w.length > 4).slice(0, 3);

                    return (
                        <RackCard 
                            key={gen.id}
                            id={gen.id}
                            name={gen.creative_name || gen.filename.replace('.adg', '')}
                            type={type}
                            date={new Date(gen.created_at).toLocaleDateString()}
                            tags={tags}
                            file_url={gen.file_url}
                            rack_data={gen.rack_data}
                            prompt={gen.prompt}
                        />
                    );
                })}
            </div>
        )}
      </div>
    </div>
  );
}
