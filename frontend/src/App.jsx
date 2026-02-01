import { useState, useEffect } from 'react';
import { api } from './api/client';
import { Navbar } from './components/layout/Navbar';
import { InputSection } from './components/hero/InputSection';
import { ResultCard } from './components/result/ResultCard';

function App() {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [deviceCount, setDeviceCount] = useState(0);

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
    } catch (err) {
      setError('Failed to generate rack. Our AI engine is currently busy or the prompt was invalid.');
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col noise-bg bg-bg-deep font-sans selection:bg-accent-primary/30">
      
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

export default App;
