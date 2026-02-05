"use client";

import { useState, useEffect } from 'react';
import { api, GenerateResponse } from '@/lib/api';
import { Navbar } from '@/components/layout/Navbar';
import { InputSection } from '@/components/hero/InputSection';
import { ResultCard } from '@/components/result/ResultCard';

export default function Home() {
  const [prompt, setPrompt] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [deviceCount, setDeviceCount] = useState<number>(0);

  useEffect(() => {
    // Load device count
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
      const data = await api.generateRack(prompt);
      setResult(data);
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
      
      <Navbar deviceCount={deviceCount} />

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 py-32 flex flex-col justify-center min-h-screen">
        
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
