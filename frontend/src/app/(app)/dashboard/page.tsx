"use client";

import { useState, useEffect } from 'react';
import { api, GenerateResponse } from '@/lib/api';
import { Navbar } from '@/components/layout/Navbar';
import { InputSection } from '@/components/hero/InputSection';
import { ResultCard } from '@/components/result/ResultCard';
import { UserButton, useUser } from "@clerk/nextjs";
import { syncUserProfile, generateRackAction } from '@/app/actions';

export default function DashboardPage() {
  const { user } = useUser();
  const [prompt, setPrompt] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [deviceCount, setDeviceCount] = useState<number>(0);
  const [credits, setCredits] = useState<number | null>(null);

  useEffect(() => {
    // 1. Sync User with Supabase
    syncUserProfile().then(res => {
        if (res.success) setCredits(res.credits ?? 0);
    });

    // 2. Load device count
    api.getDevices().then(data => {
      setDeviceCount(Object.keys(data || {}).length);
    }).catch(console.error);
  }, []);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setError('');
    setResult(null);

    try {
      // Use Server Action instead of direct API call
      const res = await generateRackAction(prompt);
      
      if (!res.success) {
        throw new Error(res.error);
      }
      
      setResult(res.data);
      if (res.remainingCredits !== undefined) {
        setCredits(res.remainingCredits);
      }
      
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || 'Failed to generate rack. Our AI engine is currently busy or the prompt was invalid.');
      } else {
        setError('An unexpected error occurred.');
      }
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col noise-bg bg-bg-deep font-sans selection:bg-accent-primary/30 text-white">
      
      {/* Navbar with User Profile */}
      <nav className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none">
        <div className="glass-panel px-6 py-3 flex items-center gap-6 pointer-events-auto shadow-2xl animate-float-slow">
            <Navbar deviceCount={deviceCount} credits={credits} />
            <div className="w-px h-4 bg-white/10"></div>
            <UserButton afterSignOutUrl="/" />
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 py-32 flex flex-col justify-center min-h-screen">
        
        {/* Welcome Message */}
        {!result && user && (
           <div className="text-center mb-8 animate-in fade-in slide-in-from-top-4">
              <p className="text-text-dim text-sm uppercase tracking-widest font-bold">Welcome back</p>
              <p className="text-white text-lg font-medium">{user.firstName || user.username}</p>
           </div>
        )}

        {/* Input Section - Only show when no result */}
        {!result && (
          <InputSection 
             prompt={prompt}
             setPrompt={setPrompt}
             handleGenerate={handleGenerate}
             isGenerating={isGenerating}
             error={error}
          />
        )}

        {/* RESULT CARD */}
        {result && (
          <ResultCard 
             result={result} 
             onReset={() => setResult(null)} 
          />
        )}

      </main>
    </div>
  );
}
