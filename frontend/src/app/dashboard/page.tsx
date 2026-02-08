"use client";

import { useState, useEffect, Suspense } from "react";
import { InputSection } from "@/components/hero/InputSection";
import { ResultCard } from "@/components/result/ResultCard";
import { generateRackAction, syncUserProfile } from "@/app/actions";
import { GenerateResponse, api } from "@/lib/api";
import { Navbar } from "@/components/layout/Navbar";
import { UserButton, useUser } from "@clerk/nextjs";
import { useSearchParams, useRouter } from "next/navigation";

function DashboardContent() {
  const { user, isLoaded } = useUser();
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState("");
  const [deviceCount, setDeviceCount] = useState(0);
  const [credits, setCredits] = useState<number | null>(null);

  useEffect(() => {
    // Handle Reset / New Navigation
    if (searchParams.get('new')) {
        setResult(null);
        setPrompt("");
        // Clean up URL without reload
        router.replace('/dashboard', { scroll: false });
    }

    syncUserProfile().then(res => {
        if (res.success) setCredits(res.credits ?? 0);
    });
    api.getDevices().then(data => {
      setDeviceCount(Object.keys(data || {}).length);
    }).catch(console.error);
  }, [searchParams, router]);

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    setIsGenerating(true);
    setError("");
    setResult(null);

    try {
      const res = await generateRackAction(prompt);
      if (!res.success) throw new Error(res.error);
      setResult(res.data);
      if (res.remainingCredits !== undefined) setCredits(res.remainingCredits);
    } catch (err: any) {
      setError(err.message || "Generation failed.");
    } finally {
      setIsGenerating(false);
    }
  };

  if (!isLoaded) return null;

  return (
    <div className="max-w-5xl mx-auto w-full px-6 py-20 flex flex-col justify-center min-h-screen">
      {!result ? (
          <InputSection 
              prompt={prompt}
              setPrompt={setPrompt}
              handleGenerate={handleGenerate}
              isGenerating={isGenerating}
              error={error}
              userName={user?.firstName || 'Creator'}
          />
      ) : (
          <ResultCard result={result} onReset={() => setResult(null)} />
      )}
    </div>
  );
}

export default function DashboardPage() {
  return (
    <div className="min-h-screen flex flex-col justify-center relative">
        <Suspense fallback={
            <div className="flex items-center justify-center min-h-screen">
                <div className="w-8 h-8 border-2 border-accent-primary border-t-transparent rounded-full animate-spin" />
            </div>
        }>
            <DashboardContent />
        </Suspense>
    </div>
  );
}
