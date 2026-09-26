import { useState, useEffect, useCallback } from 'react';
import { useLanguage } from '../../hooks/useLanguage';
import BookingSearchWidget from './BookingSearchWidget';

const HERO_SLIDES = [
  {
    image: '/images/hero/hero_exterior.jpg',
    captionUz: "Mehmonxona fasadi va xususiy avtoturargoh",
    captionRu: "Фасад отеля и охраняемая парковка",
    captionEn: "Hotel facade & private parking",
  },
  {
    image: '/images/hero/hero_lobby.jpg',
    captionUz: "Hashamatli mehmonlar zali va qulay dam olish burchagi",
    captionRu: "Уютный лаундж отеля с мягкой мебелью",
    captionEn: "Grand lobby and relaxation lounge",
  },
  {
    image: '/images/hero/hero_reception.jpg',
    captionUz: "24/7 Qabulxona va konsyerj xizmati",
    captionRu: "Круглосуточная стойка регистрации 24/7",
    captionEn: "24/7 Front desk and concierge service",
  },
];

export default function HeroSlider({ hotelInfo }) {
  const { language, t } = useLanguage();
  const [current, setCurrent] = useState(0);
  const [isPaused, setIsPaused] = useState(false);

  const nextSlide = useCallback(() => {
    setCurrent((prev) => (prev + 1) % HERO_SLIDES.length);
  }, []);

  const prevSlide = useCallback(() => {
    setCurrent((prev) => (prev - 1 + HERO_SLIDES.length) % HERO_SLIDES.length);
  }, []);

  useEffect(() => {
    if (isPaused) return;
    const interval = setInterval(nextSlide, 6000);
    return () => clearInterval(interval);
  }, [isPaused, nextSlide]);

  const locationText = language === 'ru' ? 'Ташкент' : language === 'uz' ? 'Toshkent' : 'Tashkent';
  const heroSubtitle =
    language === 'ru'
      ? 'Тихий уголок в сердце города'
      : language === 'uz'
      ? 'Shahar markazidagi sokin maskan'
      : 'An intimate sanctuary in the heart of the city';

  return (
    <section
      className="relative w-full min-h-[660px] sm:min-h-[740px] lg:min-h-[820px] flex items-center justify-center overflow-hidden bg-stone-950"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      aria-label="Hotel showcase slider"
    >
      {/* Background Slides */}
      {HERO_SLIDES.map((slide, index) => {
        const isActive = index === current;
        return (
          <div
            key={slide.image}
            className={`absolute inset-0 transition-all duration-1000 ease-in-out ${
              isActive ? 'opacity-100 scale-100 z-0' : 'opacity-0 scale-105 pointer-events-none'
            }`}
          >
            <img
              src={slide.image}
              alt={slide.captionEn}
              className="w-full h-full object-cover object-center"
              loading={index === 0 ? 'eager' : 'lazy'}
            />
          </div>
        );
      })}

      {/* Dark Vignette Overlay for Text Contrast */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/45 to-black/75 z-10" />

      {/* Hero Content */}
      <div className="relative z-20 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 text-center flex flex-col items-center">
        {/* Clickable Location Badge (Opens Yandex Maps) */}
        <a
          href={hotelInfo?.map_url || "https://yandex.uz/maps/-/CPwOM2O3"}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-black/60 hover:bg-black/90 backdrop-blur-md border border-amber-400/60 hover:border-amber-400 text-amber-300 hover:text-amber-200 text-xs sm:text-sm font-semibold tracking-wider uppercase mb-5 shadow-xl transition-all cursor-pointer group"
          title={language === 'ru' ? 'Открыть локацию в Яндекс.Картах' : language === 'uz' ? 'Lokatsiyani xaritada ochish (Yandex Maps)' : 'Open location in Maps'}
        >
          <svg className="w-4 h-4 text-amber-400 group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
              clipRule="evenodd"
            />
          </svg>
          <span>📍 {locationText}, Bog‘ibuston 156</span>
          <span className="text-amber-400 font-bold group-hover:translate-x-0.5 transition-transform">↗</span>
        </a>

        {/* Brand Main Title */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl lg:text-8xl font-serif font-bold text-white tracking-[0.08em] uppercase drop-shadow-2xl">
          {hotelInfo?.name || 'COCO HOTEL'}
        </h1>

        {/* Gold Accent Divider */}
        <div className="flex items-center justify-center gap-3 my-4">
          <span className="w-12 h-px bg-amber-400/80" />
          <span className="w-2 h-2 rotate-45 bg-amber-400" />
          <span className="w-12 h-px bg-amber-400/80" />
        </div>

        {/* Subtitle */}
        <p className="text-base sm:text-xl md:text-2xl text-white/90 font-medium tracking-wide max-w-2xl drop-shadow mb-8 sm:mb-12">
          {heroSubtitle}
        </p>

        {/* Booking Search Widget (Frosted Glass) */}
        <div className="w-full max-w-4xl">
          <BookingSearchWidget glass={true} />
        </div>

        {/* Slider Indicator Dots */}
        <div className="flex items-center gap-2.5 mt-8 sm:mt-10" role="tablist" aria-label="Slide controls">
          {HERO_SLIDES.map((_, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => setCurrent(idx)}
              className={`h-2.5 rounded-full transition-all duration-300 focus:outline-none cursor-pointer ${
                idx === current ? 'w-8 bg-amber-400 shadow-md' : 'w-2.5 bg-white/40 hover:bg-white/70'
              }`}
              aria-label={`Slide ${idx + 1}`}
              aria-selected={idx === current}
            />
          ))}
        </div>
      </div>

      {/* Prev / Next Controls */}
      <button
        type="button"
        onClick={prevSlide}
        className="hidden sm:flex absolute left-4 lg:left-8 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full items-center justify-center bg-black/35 hover:bg-black/60 border border-white/20 text-white backdrop-blur-md transition-all cursor-pointer shadow-lg"
        aria-label="Previous slide"
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth="2.5" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
        </svg>
      </button>
      <button
        type="button"
        onClick={nextSlide}
        className="hidden sm:flex absolute right-4 lg:right-8 top-1/2 -translate-y-1/2 z-20 w-11 h-11 rounded-full items-center justify-center bg-black/35 hover:bg-black/60 border border-white/20 text-white backdrop-blur-md transition-all cursor-pointer shadow-lg"
        aria-label="Next slide"
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth="2.5" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
        </svg>
      </button>
    </section>
  );
}
