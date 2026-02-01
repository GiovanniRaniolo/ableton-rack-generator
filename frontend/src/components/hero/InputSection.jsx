import { RefreshCw, Sparkles, Music, Zap, Box } from 'lucide-react';

const TEMPLATES = [
  { id: 'vocal', icon: <Music className="w-4 h-4" />, name: 'Vocal Prime', prompt: 'Elite vocal chain with compressor, de-esser, EQ Eight and hybrid reverb' },
  { id: 'drums', icon: <Zap className="w-4 h-4" />, name: 'Punchy Drums', prompt: 'Aggressive drum buss with roar, saturator and glue compressor' },
  { id: 'master', icon: <Sparkles className="w-4 h-4" />, name: 'Master AI', prompt: 'Clean mastering chain with mid-side EQ, limiter and saturator' },
  { id: 'space', icon: <Box className="w-4 h-4" />, name: 'Deep Space', prompt: 'Atmospheric rack with spectral time, echo and phaser-flanger' },
];

export function InputSection({ prompt, setPrompt, handleGenerate, isGenerating, error }) {
  return (
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
            <div className="bg-black/40 rounded-xl p-2 relative overflow-hidden border border-white/5 transition-all duration-300 focus-within:border-accent-primary/50 focus-within:bg-black/60 focus-within:shadow-[0_0_30px_rgba(255,124,37,0.15)]">
               <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe a sound... e.g. 'Crushed lo-fi drums with spatial echo'"
                className="w-full h-32 bg-transparent border-none focus:ring-0 outline-none text-2xl font-medium placeholder:text-white/20 text-white p-6 resize-none"
              />
              <div className="flex justify-between items-center px-4 pb-2">
                 <div className="flex gap-2">
                    {TEMPLATES.slice(0,3).map(t => (
                      <button key={t.id} onClick={() => setPrompt(t.prompt)} className="px-3 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-[10px] font-bold uppercase tracking-widest transition-colors border border-white/5 flex items-center gap-2">
                        {t.icon}
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
  );
}
