export default function CocoLogo({ className = '', emblemOnly = false, size = 'default' }) {
  // Dimensions
  const emblemSizes = {
    sm: 'w-7 h-7',
    default: 'w-9 h-9 sm:w-10 sm:h-10',
    lg: 'w-12 h-12 sm:w-14 sm:h-14',
  };

  const textSizes = {
    sm: { title: 'text-lg tracking-[0.2em]', sub: 'text-[8px] tracking-[0.3em]' },
    default: { title: 'text-xl sm:text-2xl tracking-[0.25em]', sub: 'text-[9px] sm:text-[10px] tracking-[0.35em]' },
    lg: { title: 'text-2xl sm:text-3xl tracking-[0.25em]', sub: 'text-[10px] sm:text-[11px] tracking-[0.4em]' },
  };

  return (
    <div className={`inline-flex items-center gap-2.5 sm:gap-3 group ${className}`}>
      {/* Real Coco Hotel Emblem: Interlocking luxury looped clover/infinity monogram */}
      <svg
        className={`${emblemSizes[size] || emblemSizes.default} shrink-0 text-[var(--color-gold)] transition-transform duration-300 group-hover:scale-105`}
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="cocoGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#fae28e" />
            <stop offset="50%" stopColor="#dfba56" />
            <stop offset="100%" stopColor="#b88a28" />
          </linearGradient>
          <filter id="goldGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="1" stdDeviation="1.5" floodColor="#dfba56" floodOpacity="0.4" />
          </filter>
        </defs>

        {/* Outer stylized diamond/clover petals with metallic gold stroke */}
        <g filter="url(#goldGlow)">
          {/* Top petal */}
          <path
            d="M 50 14 C 62 14 74 25 74 38 C 74 46 68 53 60 56 C 53 49 53 38 42 35 C 39 22 43 14 50 14 Z"
            stroke="url(#cocoGoldGrad)"
            strokeWidth="3.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
          {/* Bottom petal */}
          <path
            d="M 50 86 C 38 86 26 75 26 62 C 26 54 32 47 40 44 C 47 51 47 62 58 65 C 61 78 57 86 50 86 Z"
            stroke="url(#cocoGoldGrad)"
            strokeWidth="3.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
          {/* Left petal */}
          <path
            d="M 14 50 C 14 38 25 26 38 26 C 46 26 53 32 56 40 C 49 47 38 47 35 58 C 22 61 14 57 14 50 Z"
            stroke="url(#cocoGoldGrad)"
            strokeWidth="3.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
          {/* Right petal */}
          <path
            d="M 86 50 C 86 62 75 74 62 74 C 54 74 47 68 44 60 C 51 53 62 53 65 42 C 78 39 86 43 86 50 Z"
            stroke="url(#cocoGoldGrad)"
            strokeWidth="3.8"
            strokeLinecap="round"
            strokeLinejoin="round"
            fill="none"
          />
          {/* Central interlock diamond accent */}
          <circle cx="50" cy="50" r="4.5" fill="url(#cocoGoldGrad)" />
        </g>
      </svg>

      {/* Typography */}
      {!emblemOnly && (
        <div className="flex flex-col select-none">
          <span
            className={`font-serif font-bold ${
              textSizes[size]?.title || textSizes.default.title
            } text-theme-main transition-colors group-hover:text-theme-gold leading-none`}
          >
            COCO
          </span>
          <span
            className={`font-sans font-medium uppercase ${
              textSizes[size]?.sub || textSizes.default.sub
            } text-theme-gold flex items-center gap-1.5 mt-1 opacity-90`}
          >
            <span className="w-2.5 h-px bg-theme-gold inline-block opacity-60" />
            HOTEL
            <span className="w-2.5 h-px bg-theme-gold inline-block opacity-60" />
          </span>
        </div>
      )}
    </div>
  );
}
