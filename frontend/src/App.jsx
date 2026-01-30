import { useState, useEffect } from 'react';
import { 
  Wand2, Download, Box, Layers, Play, RefreshCw, 
  Cpu, Database, Sparkles, ChevronRight, Zap,
  Music, Settings2, Share2, HelpCircle
} from 'lucide-react';
import { api } from './api/client';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/** Utility for tailwind class merging */
function cn(...inputs) {
  return twMerge(clsx(inputs));
}

const TEMPLATES = [
  { id: 'vocal', icon: <Music className="w-4 h-4" />, name: 'Vocal Prime', prompt: 'Elite vocal chain with compressor, de-esser, EQ Eight and hybrid reverb' },
  { id: 'drums', icon: <Zap className="w-4 h-4" />, name: 'Punchy Drums', prompt: 'Aggressive drum buss with roar, saturator and glue compressor' },
  { id: 'master', icon: <Sparkles className="w-4 h-4" />, name: 'Master AI', prompt: 'Clean mastering chain with mid-side EQ, limiter and saturator' },
  { id: 'space', icon: <Box className="w-4 h-4" />, name: 'Deep Space', prompt: 'Atmospheric rack with spectral time, echo and phaser-flanger' },
];

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
      {/* Top Navbar - Minimal & Floating */}
      <nav className="fixed top-6 left-0 right-0 z-50 flex justify-center pointer-events-none">
        <div className="glass-panel px-6 py-3 flex items-center gap-6 pointer-events-auto shadow-2xl animate-float-slow">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-accent-primary blur-md opacity-40 animate-pulse-slow"></div>
                <Zap className="text-accent-primary w-5 h-5 relative z-10 fill-current" />
              </div>
              <span className="text-sm font-black tracking-[0.3em] text-white">ADG GEN</span>
            </div>
            <div className="w-px h-4 bg-white/10"></div>
            <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-text-dim">
              <Database className="w-3 h-3 text-accent-secondary" />
              <span>{deviceCount} Modules Online</span>
            </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 py-32 flex flex-col justify-center min-h-screen">
        
        {/* Input Section - Only show when no result or explicitly reset (not implemented yet, but for now just hide if result exists? No, keep it top) */}
        {!result && (
          <section className="space-y-12 text-center animate-in fade-in zoom-in duration-700">
            <div className="space-y-6">
               <h1 className="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-white/40 tracking-tighter leading-[0.9]">
                 AUDIO<br/>ALCHEMY
               </h1>
               <p className="text-xl text-text-dim font-medium max-w-2xl mx-auto leading-relaxed">
                 Generate studio-grade Ableton Effect Racks using an AI trained on professional sound design techniques.
               </p>
            </div>

            <div className="max-w-3xl mx-auto relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-accent-primary to-accent-secondary rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
              <div className="relative glass-panel p-2">
                <div className="bg-black/40 rounded-xl p-2 relative overflow-hidden">
                   <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe a sound... e.g. 'Crushed lo-fi drums with spatial echo'"
                    className="w-full h-32 bg-transparent border-none focus:ring-0 text-2xl font-medium placeholder:text-white/20 text-white p-6 resize-none"
                  />
                  <div className="flex justify-between items-center px-4 pb-2">
                     <div className="flex gap-2">
                        {TEMPLATES.slice(0,3).map(t => (
                          <button key={t.id} onClick={() => setPrompt(t.prompt)} className="px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-[10px] font-bold uppercase tracking-widest transition-colors border border-white/5">
                            {t.name}
                           </button>
                        ))}
                     </div>
                     <button
                      onClick={handleGenerate}
                      disabled={isGenerating || !prompt.trim()}
                      className="px-8 py-3 bg-white text-black font-black uppercase tracking-widest text-xs rounded-lg hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none flex items-center gap-2 shadow-[0_0_20px_rgba(255,255,255,0.3)]"
                     >
                       {isGenerating ? <RefreshCw className="animate-spin w-4 h-4"/> : <Sparkles className="w-4 h-4"/>}
                       Generate
                     </button>
                  </div>
                </div>
              </div>
            </div>
            {error && <p className="text-red-400 font-mono text-xs bg-red-500/10 inline-block px-4 py-2 rounded-lg border border-red-500/20">{error}</p>}
          </section>
        )}

        {/* RESULT CARD - THE "ALLUCINANTE" PART */}
        {result && (
          <div className="animate-in fade-in slide-in-from-bottom-24 duration-1000">
             <div className="relative glass-panel p-1 border-gradient overflow-hidden group">
                {/* Background Glows */}
                <div className="absolute -top-40 -right-40 w-96 h-96 bg-accent-primary/20 blur-[150px] pointer-events-none animate-pulse-slow"></div>
                <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-accent-secondary/20 blur-[150px] pointer-events-none animate-pulse-slow" style={{animationDelay: '1s'}}></div>

                <div className="bg-[#0a0a0b]/80 rounded-[1.8rem] overflow-hidden relative z-10">
                   
                   {/* HEADER ROW */}
                   <header className="p-10 md:p-14 border-b border-white/5 flex flex-col md:flex-row justify-between items-start md:items-center gap-8 relative overflow-hidden">
                      <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
                      
                      <div className="space-y-4 relative z-10">
                         <div className="inline-flex items-center gap-3 px-3 py-1 rounded-full bg-accent-primary/10 border border-accent-primary/20 text-accent-primary text-[10px] font-black uppercase tracking-[0.2em]">
                            <span className="relative flex h-2 w-2">
                              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-primary opacity-75"></span>
                              <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-primary"></span>
                            </span>
                            ADG Generated
                         </div>
                         <h2 className="text-5xl md:text-7xl font-black text-white tracking-tighter leading-none text-glow">
                           {result.creative_name}
                         </h2>
                         <p className="font-mono text-text-dim text-sm">{result.filename}</p>
                      </div>

                      <div className="flex flex-col gap-3 relative z-10">
                        <button 
                          onClick={() => api.downloadRack(result.filename)}
                          className="px-8 py-4 bg-accent-primary hover:bg-[#ff904d] text-black font-black uppercase tracking-[0.2em] text-xs rounded-full shadow-[0_0_30px_-5px_rgba(255,124,37,0.4)] hover:shadow-[0_0_50px_-10px_rgba(255,124,37,0.6)] hover:scale-105 transition-all active:scale-95 flex items-center gap-3"
                        >
                          <Download className="w-4 h-4" />
                          Download .adg
                        </button>
                        <button 
                          onClick={() => setResult(null)}
                          className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/10 text-white font-bold uppercase tracking-[0.2em] text-xs rounded-full transition-all flex items-center justify-center gap-3 backdrop-blur-md"
                        >
                          <RefreshCw className="w-4 h-4" />
                          New Rack
                        </button>
                      </div>
                   </header>

                   {/* CORE GRID */}
                   <div className="grid grid-cols-1 lg:grid-cols-2">
                      
                      {/* LEFT: INTENT & DEVICES */}
                      <div className="p-10 md:p-14 border-b lg:border-b-0 lg:border-r border-white/5 space-y-12">
                         <div className="space-y-6">
                            <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                               <Sparkles className="w-4 h-4 text-accent-secondary" />
                               Sonic Signature
                            </h3>
                            {/* Decreased from text-2xl/3xl to xl/2xl */}
                            <p className="text-xl md:text-2xl font-medium text-white leading-relaxed italic opacity-90">
                              "{result.sound_intent}"
                            </p>
                            <div className="p-6 bg-white/5 rounded-2xl border border-white/5 backdrop-blur-sm">
                              <p className="text-sm text-text-main font-mono leading-relaxed">
                                {result.explanation}
                              </p>
                            </div>
                         </div>

                         <div className="space-y-8">
                             <div className="flex items-center justify-between">
                                <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                                  <Layers className="w-4 h-4 text-accent-primary" />
                                  Signal Topology
                                </h3>
                                {result.parallel_logic && <span className="text-[10px] font-mono text-accent-primary bg-accent-primary/10 px-2 py-1 rounded">PARALLEL</span>}
                             </div>

                             <div className="space-y-4">
                               {result.devices.map((dev, i) => (
                                 <div key={i} className="group flex items-center gap-4 relative">
                                    {i !== result.devices.length - 1 && (
                                       <div className="absolute left-[19px] top-10 w-0.5 h-6 bg-white/10 group-hover:bg-accent-primary/50 transition-colors"></div>
                                    )}
                                    <div className="w-10 h-10 rounded-xl bg-bg-deep border border-white/10 flex items-center justify-center text-text-dim font-black text-sm group-hover:border-accent-primary group-hover:text-accent-primary group-hover:shadow-[0_0_15px_rgba(255,124,37,0.2)] transition-all z-10">
                                      {i + 1}
                                    </div>
                                    <div className="flex-1 h-12 bg-white/[0.02] border border-white/[0.05] rounded-xl flex items-center px-6 text-sm font-bold tracking-wider text-text-bright uppercase group-hover:bg-white/[0.05] transition-all">
                                      {dev}
                                    </div>
                                 </div>
                               ))}
                             </div>
                         </div>
                      </div>

                      {/* RIGHT: MACRO ENGINEERING */}
                      <div className="p-10 md:p-14 bg-black/20">
                         <div className="flex items-center justify-between mb-10">
                            <h3 className="text-xs font-black text-text-dim uppercase tracking-[0.5em] flex items-center gap-3">
                               <Settings2 className="w-4 h-4 text-accent-success" />
                               Macro Matrix
                            </h3>
                            <div className="flex gap-1">
                               <div className="w-1 h-1 rounded-full bg-accent-success animate-pulse"></div>
                               <div className="w-1 h-1 rounded-full bg-accent-success animate-pulse delay-75"></div>
                               <div className="w-1 h-1 rounded-full bg-accent-success animate-pulse delay-150"></div>
                            </div>
                         </div>

                         <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {(result.macro_details && result.macro_details.length > 0 ? result.macro_details : Array.from({length: 8}, (_,i) => ({macro: i+1, name: `Macro ${i+1}`, description: 'Parameter'}))).map((m, i) => (
                              <div key={i} className="bg-bg-deep border border-white/5 rounded-2xl p-5 hover:border-accent-success/30 transition-all group hover:-translate-y-1 relative overflow-hidden">
                                 <div className="absolute inset-0 bg-accent-success/5 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                 <div className="flex justify-between items-start mb-2 relative z-10">
                                    {/* Increased from text-[10px] to text-xs */}
                                    <span className="text-xs font-black text-accent-success uppercase tracking-widest">Knob {m.macro}</span>
                                    <div className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center group-hover:border-accent-success/50 group-hover:rotate-90 transition-all duration-500">
                                       <div className="w-0.5 h-3 bg-white/20 mb-3 rounded-full group-hover:bg-accent-success"></div>
                                    </div>
                                 </div>
                                 {/* Increased from text-sm to text-base */}
                                 <p className="text-base font-black text-white uppercase tracking-wider mb-1 truncate relative z-10">{m.name}</p>
                                 {/* Increased from text-[10px] to text-xs */}
                                 {/* Description - NO TRUNCATION */}
                                 <p className="text-xs text-text-dim leading-relaxed relative z-10 mb-4 border-b border-white/5 pb-2">
                                    {m.description}
                                 </p>
                                 
                                 {/* Technical Mapping Truth - HIGH VISIBILITY */}
                                 <div className="bg-black/40 rounded-lg p-3 relative z-10">
                                     <div className="flex items-center gap-2 mb-2">
                                        <div className={`w-1.5 h-1.5 rounded-full ${m.target_device ? 'bg-accent-success shadow-[0_0_8px_rgba(74,222,128,0.5)]' : 'bg-yellow-500'}`}></div>
                                        <span className="text-[10px] font-black uppercase tracking-widest text-text-dim">
                                            {m.target_device ? 'AI Connection' : 'Auto-Mapping'}
                                        </span>
                                     </div>
                                     
                                     {m.target_device ? (
                                         <div className="space-y-1">
                                             <div className="flex justify-between items-center text-[10px] uppercase tracking-wider font-mono">
                                                 <span className="text-text-dim">Device</span>
                                                 <span className="text-accent-success font-bold">{m.target_device}</span>
                                             </div>
                                             <div className="flex justify-between items-center text-[10px] uppercase tracking-wider font-mono">
                                                  <span className="text-text-dim">Param</span>
                                                  <span className="text-white font-bold">{m.target_parameter}</span>
                                             </div>
                                         </div>
                                     ) : (
                                         <div className="text-[10px] text-text-dim italic text-center py-1">
                                             System determined best parameter logic
                                         </div>
                                     )}
                                 </div>
                              </div>
                            ))}
                         </div>
                         
                         {result.tips && result.tips.length > 0 && (
                            <div className="mt-12 pt-8 border-t border-white/5">
                               <p className="text-[10px] font-black text-text-dim uppercase tracking-[0.2em] mb-4">Pro Tips</p>
                               <div className="space-y-3">
                                  {result.tips.slice(0, 2).map((tip, idx) => (
                                     /* Increased from text-xs to text-sm */
                                     <div key={idx} className="flex gap-3 text-sm text-text-main leading-relaxed opacity-60 hover:opacity-100 transition-opacity">
                                        <span className="text-accent-secondary">•</span>
                                        {tip}
                                     </div>
                                  ))}
                               </div>
                            </div>
                         )}
                      </div>
                   </div>
                </div>
             </div>
          </div>
        )}

      </main>
    </div>
  );
}

export default App;
