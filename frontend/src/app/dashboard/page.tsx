"use client";

import { useState, useEffect } from "react";
import { InputSection } from "@/components/hero/InputSection";
import { ResultCard } from "@/components/result/ResultCard";
import { generateRackAction, syncUserProfile } from "@/app/actions";
import { GenerateResponse, api } from "@/lib/api";
import { Navbar } from "@/components/layout/Navbar";
import { UserButton, useUser } from "@clerk/nextjs";

export default function DashboardPage() {
  const { user } = useUser();
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState("");
  const [deviceCount, setDeviceCount] = useState(0);
  const [credits, setCredits] = useState<number | null>(null);

  useEffect(() => {
    syncUserProfile().then(res => {
        if (res.success) setCredits(res.credits ?? 0);
    });
    api.getDevices().then(data => {
      setDeviceCount(Object.keys(data || {}).length);
    }).catch(console.error);
  }, []);

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

  return (
    <div className="min-h-screen flex flex-col justify-center relative">
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
    </div>
  );
}
