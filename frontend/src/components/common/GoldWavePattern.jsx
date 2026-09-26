export default function GoldWavePattern({
  variant = 'hero', // 'hero' | 'top-right' | 'subtle'
  opacity,
  className = '',
}) {
  const customStyle = opacity !== undefined ? { opacity } : undefined;

  if (variant === 'hero') {
    return (
      <div
        className={`absolute inset-0 overflow-hidden pointer-events-none z-0 select-none ${className}`}
        style={customStyle}
        aria-hidden="true"
      >
        <svg
          className="absolute -top-12 -left-20 w-[120%] h-[120%] opacity-25 dark:opacity-35"
          viewBox="0 0 1440 900"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="none"
        >
          <defs>
            <linearGradient id="goldWaveGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#fae28e" stopOpacity="0.8" />
              <stop offset="50%" stopColor="#dfba56" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#b88a28" stopOpacity="0" />
            </linearGradient>
            <linearGradient id="goldWaveGrad2" x1="100%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stopColor="#fae28e" stopOpacity="0.7" />
              <stop offset="40%" stopColor="#dfba56" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#b88a28" stopOpacity="0" />
            </linearGradient>
          </defs>

          {/* Flowing Ribbon 1 */}
          <path
            d="M-100 250 C 250 80, 500 480, 850 280 C 1100 120, 1350 350, 1600 200"
            stroke="url(#goldWaveGrad1)"
            strokeWidth="1.6"
            fill="none"
          />
          <path
            d="M-100 270 C 250 100, 500 500, 850 300 C 1100 140, 1350 370, 1600 220"
            stroke="url(#goldWaveGrad1)"
            strokeWidth="1.4"
            fill="none"
          />
          <path
            d="M-100 290 C 250 120, 500 520, 850 320 C 1100 160, 1350 390, 1600 240"
            stroke="url(#goldWaveGrad1)"
            strokeWidth="1.2"
            fill="none"
          />
          <path
            d="M-100 310 C 250 140, 500 540, 850 340 C 1100 180, 1350 410, 1600 260"
            stroke="url(#goldWaveGrad1)"
            strokeWidth="1"
            fill="none"
          />
          <path
            d="M-100 330 C 250 160, 500 560, 850 360 C 1100 200, 1350 430, 1600 280"
            stroke="url(#goldWaveGrad1)"
            strokeWidth="0.8"
            fill="none"
          />

          {/* Flowing Ribbon 2 (Counter-wave in lower half) */}
          <path
            d="M-80 650 C 300 450, 600 800, 1050 550 C 1300 400, 1500 620, 1650 500"
            stroke="url(#goldWaveGrad2)"
            strokeWidth="1.8"
            fill="none"
          />
          <path
            d="M-80 670 C 300 470, 600 820, 1050 570 C 1300 420, 1500 640, 1650 520"
            stroke="url(#goldWaveGrad2)"
            strokeWidth="1.5"
            fill="none"
          />
          <path
            d="M-80 690 C 300 490, 600 840, 1050 590 C 1300 440, 1500 660, 1650 540"
            stroke="url(#goldWaveGrad2)"
            strokeWidth="1.2"
            fill="none"
          />
          <path
            d="M-80 710 C 300 510, 600 860, 1050 610 C 1300 460, 1500 680, 1650 560"
            stroke="url(#goldWaveGrad2)"
            strokeWidth="0.9"
            fill="none"
          />
        </svg>
      </div>
    );
  }

  if (variant === 'top-right') {
    return (
      <div
        className={`absolute top-0 right-0 w-96 h-96 overflow-hidden pointer-events-none z-0 select-none opacity-20 dark:opacity-30 ${className}`}
        style={customStyle}
        aria-hidden="true"
      >
        <svg viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
          <path d="M50 0 C 120 180, 260 220, 400 120" stroke="#dfba56" strokeWidth="1.2" fill="none" opacity="0.6" />
          <path d="M80 0 C 150 190, 280 230, 400 140" stroke="#dfba56" strokeWidth="1.2" fill="none" opacity="0.5" />
          <path d="M110 0 C 180 200, 300 240, 400 160" stroke="#dfba56" strokeWidth="1" fill="none" opacity="0.4" />
          <path d="M140 0 C 210 210, 320 250, 400 180" stroke="#dfba56" strokeWidth="0.8" fill="none" opacity="0.3" />
        </svg>
      </div>
    );
  }

  // Generic subtle wave background
  return (
    <div
      className={`absolute inset-0 overflow-hidden pointer-events-none z-0 select-none opacity-15 dark:opacity-20 ${className}`}
      style={customStyle}
      aria-hidden="true"
    >
      <svg
        className="w-full h-full object-cover"
        viewBox="0 0 1000 600"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
      >
        <path d="M-50 150 Q 250 50 550 220 T 1100 180" stroke="#dfba56" strokeWidth="1.2" fill="none" />
        <path d="M-50 175 Q 250 75 550 245 T 1100 205" stroke="#dfba56" strokeWidth="1" fill="none" opacity="0.8" />
        <path d="M-50 200 Q 250 100 550 270 T 1100 230" stroke="#dfba56" strokeWidth="0.8" fill="none" opacity="0.6" />
      </svg>
    </div>
  );
}
