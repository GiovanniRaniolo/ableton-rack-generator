export function Logo({ className = "w-8 h-8", showText = true }: { className?: string, showText?: boolean }) {
  return (
    <div className="flex items-center gap-3">
      <svg 
        viewBox="0 0 100 100" 
        className={className} 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Input Lines (Cyan) */}
        <path d="M10 35 H30" stroke="#00FFC2" strokeWidth="6" strokeLinecap="round" />
        <path d="M10 65 H30" stroke="#00FFC2" strokeWidth="6" strokeLinecap="round" />
        
        {/* The Processor Box (Dark with Cyan Glow) */}
        <rect x="30" y="20" width="40" height="60" rx="8" fill="#121212" stroke="#00FFC2" strokeWidth="3" />
        
        {/* Internal Parallel Logic (Subtle) */}
        <path d="M40 35 H60" stroke="#00FFC2" strokeWidth="2" strokeOpacity="0.5" />
        <path d="M40 50 H60" stroke="#00FFC2" strokeWidth="2" strokeOpacity="0.5" />
        <path d="M40 65 H60" stroke="#00FFC2" strokeWidth="2" strokeOpacity="0.5" />

        {/* 8 Output Macro Lines (The Core Value) */}
        <path d="M70 24 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 32 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 40 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 48 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 56 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 64 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 72 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
        <path d="M70 80 H90" stroke="#00FFC2" strokeWidth="3" strokeLinecap="round" />
      </svg>
      
      {showText && (
        <span className="font-extrabold tracking-tight text-white flex flex-col leading-none">
          <span className="text-[1.1em] tracking-[0.05em]">ADG</span>
          <span className="text-[0.6em] text-[#00FFC2] tracking-[0.2em] font-mono uppercase">Builder</span>
        </span>
      )}
    </div>
  );
}
