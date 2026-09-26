import HotelImage from '../components/common/HotelImage';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useLanguage } from '../hooks/useLanguage';
import { getGallery } from '../api/hotel';
import Container from '../components/common/Container';
import SectionTitle from '../components/common/SectionTitle';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function GalleryPage() {
  const { t, language } = useLanguage();
  usePageMeta({
    title: t('meta.galleryTitle'),
    description: t('meta.galleryDesc'),
    canonicalPath: '/gallery',
  });

  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeImage, setActiveImage] = useState(null);
  useEffect(() => {
    if (!activeImage) return;
    const previousFocus = document.activeElement;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const close = document.querySelector('[data-gallery-close]');
    close?.focus();
    const onKey = (event) => {
      if (event.key === 'Escape') setActiveImage(null);
      if (event.key === 'Tab') {
        const nodes = [...document.querySelectorAll('[data-gallery-dialog] button, [data-gallery-dialog] a')];
        const first = nodes[0], last = nodes[nodes.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
      }
    };
    document.addEventListener('keydown', onKey);
    return () => { document.body.style.overflow = previousOverflow; document.removeEventListener('keydown', onKey); previousFocus?.focus(); };
  }, [activeImage]);

  const handleRetry = () => {
    setLoading(true);
    setError(false);
    getGallery()
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setError(false);
            setImages(data);
        } else {
          setImages([]);
        }
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setImages([]);
        setLoading(false);
      });
  };

  useEffect(() => {
    let isMounted = true;
    getGallery()
      .then((data) => {
        if (isMounted) {
          if (Array.isArray(data) && data.length > 0) {
            setError(false);
            setImages(data);
          } else {
            setImages([]);
          }
          setLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setError(true);
          setImages([]);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [language]);

  const categories = [
    { key: 'all', label: language === 'uz' ? 'Barchasi' : language === 'ru' ? 'Все фото' : 'All Views' },
    { key: 'rooms', label: language === 'uz' ? 'Xonalar' : language === 'ru' ? 'Номера' : 'Rooms & Suites' },
    { key: 'interior', label: language === 'uz' ? 'Interyer' : language === 'ru' ? 'Интерьер' : 'Interior & Lobby' },
    { key: 'dining', label: language === 'uz' ? 'Restoran' : language === 'ru' ? 'Ресторан' : 'Dining' },
    { key: 'exterior', label: language === 'uz' ? 'Eksteryer' : language === 'ru' ? 'Экстерьер' : 'Exterior' },
  ];

  const filteredImages = images.filter((item) => {
    if (activeCategory === 'all') return true;
    const itemCat = item.category;
    return itemCat === activeCategory;
  });

  return (
    <div className="flex flex-col bg-theme-main transition-colors duration-200">
      {/* 1. HERO HEADER */}
      <section
        aria-label="Gallery Header"
        className="relative bg-theme-secondary text-theme-main py-20 sm:py-28 border-b border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern opacity={0.14} />
        <Container className="relative z-10 text-center">
          <RevealOnScroll variant="up">
            <span className="inline-block px-3.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-[0.25em] text-[#fae28e] bg-[#dfba56]/15 border border-[#dfba56]/30 mb-4">
              {t('gallery.subtitle')}
            </span>
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mb-4">
              {t('gallery.title')}
            </h1>
            <p className="text-base sm:text-lg text-theme-muted font-light max-w-2xl mx-auto leading-relaxed">
              {t('gallery.intro')}
            </p>

            {/* Filter Pills */}
            <div className="flex flex-wrap items-center justify-center gap-2 mt-8">
              {categories.map((cat) => {
                const isActive = activeCategory === cat.key;
                return (
                  <button
                    key={cat.key}
                    type="button"
                    onClick={() => setActiveCategory(cat.key)}
                    className={`px-5 py-2 rounded-full text-xs font-semibold tracking-wider uppercase transition-all duration-300 cursor-pointer ${
                      isActive
                        ? 'bg-gold-metallic text-stone-950 shadow-md shadow-[#dfba56]/20'
                        : 'bg-theme-surface text-theme-muted border border-theme hover:border-[#dfba56]/50 hover:text-theme-main'
                    }`}
                  >
                    {cat.label}
                  </button>
                );
              })}
            </div>
          </RevealOnScroll>
        </Container>
      </section>

      {/* 2. GALLERY GRID */}
      <section aria-label="Hotel Photographs" className="relative py-16 sm:py-24 bg-theme-main">
        <GoldWavePattern opacity={0.06} />
        <Container className="relative z-10">
          {loading ? (
            <LoadingState />
          ) : error ? (
            <ErrorState onRetry={handleRetry} />
          ) : filteredImages.length === 0 ? (
            <div className="text-center py-16 px-6 bg-theme-surface border border-theme rounded-2xl max-w-xl mx-auto shadow-xl">
              <h2 className="font-serif text-xl font-bold text-theme-main mb-2">
                {t('gallery.empty')}
              </h2>
              <p className="text-sm text-theme-muted mb-6 leading-relaxed font-light">
                {t('rooms.updatingDesc')}
              </p>
              <button
                type="button"
                onClick={() => setActiveCategory('all')}
                className="inline-flex items-center px-6 py-2.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic text-stone-950 rounded-xl hover:shadow-lg transition-all"
              >
                {language === 'uz' ? 'Barcha fotosuratlarni ko‘rish' : language === 'ru' ? 'Показать все фото' : 'Show All Photos'}
              </button>
            </div>
          ) : (
            <div className="space-y-12">
              <RevealOnScroll variant="up">
                <SectionTitle
                  subtitle={t('gallery.momentsSubtitle')}
                  title={t('gallery.momentsTitle')}
                />
              </RevealOnScroll>

              {/* Luxury Masonry Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
                {filteredImages.map((item, idx) => (
                  <RevealOnScroll key={item.id || idx} variant="up" delay={idx * 50}>
                    <figure
                      role="button"
                      tabIndex={0}
                      onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); setActiveImage(item); } }}
                      onClick={() => setActiveImage(item)}
                      className={`group relative overflow-hidden bg-theme-elevated rounded-2xl border border-theme hover:border-[#dfba56]/70 flex flex-col justify-end transition-all duration-500 shadow-xl hover:shadow-2xl cursor-pointer ${
                        idx === 0 ? 'sm:col-span-2 sm:aspect-16/9 aspect-4/3' : 'aspect-4/3'
                      }`}
                    >
                      <HotelImage
                        src={item.image}
                        alt={item.alt_text || item.title || 'Coco Hotel sanctuary'}
                        loading="lazy"
                        decoding="async"
                        className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
                      />

                      {/* Golden Shimmer Glow Overlay on Hover */}
                      <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-transparent opacity-80 group-hover:opacity-95 transition-opacity duration-300" />

                      {/* Caption */}
                      <figcaption className="relative z-10 p-6 text-stone-100 flex items-end justify-between">
                        <div>
                          <p className="text-[11px] font-bold tracking-[0.2em] uppercase text-[#fae28e] mb-1">
                            Coco Hotel
                          </p>
                          <h3 className="font-serif text-base sm:text-lg font-semibold text-white">
                            {item.title || item.alt_text || 'Sanctuary View'}
                          </h3>
                        </div>
                        <span className="w-9 h-9 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-[#fae28e] group-hover:scale-110 group-hover:bg-[#dfba56] group-hover:text-stone-950 transition-all duration-300 shrink-0">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m3-3H7" />
                          </svg>
                        </span>
                      </figcaption>
                    </figure>
                  </RevealOnScroll>
                ))}
              </div>

              {/* Bottom CTA */}
              <RevealOnScroll variant="up" delay={150}>
                <div className="pt-12 text-center border-t border-theme">
                  <p className="text-sm text-theme-muted mb-6 font-light">
                    {t('gallery.experienceInPerson')}
                  </p>
                  <div className="flex flex-wrap items-center justify-center gap-4">
                    <Link
                      to="/rooms"
                      className="inline-flex items-center justify-center px-7 py-3.5 text-xs font-semibold uppercase tracking-widest border border-[#dfba56] text-[#dfba56] hover:bg-[#dfba56]/10 rounded-xl transition-all"
                    >
                      {t('gallery.exploreRooms')}
                    </Link>
                    <Link
                      to="/booking"
                      className="inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic text-stone-950 rounded-xl hover:shadow-lg hover:shadow-[#dfba56]/25 active:scale-95 transition-all"
                    >
                      {t('gallery.requestReservation')}
                    </Link>
                  </div>
                </div>
              </RevealOnScroll>
            </div>
          )}
        </Container>
      </section>

      {/* Lightbox Modal */}
      {activeImage && (
        <div
          role="dialog"
          data-gallery-dialog
          aria-modal="true"
          className="fixed inset-0 z-50 bg-black/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
          aria-label={t('gallery.title')} onClick={() => setActiveImage(null)}
        >
          <div
            className="relative max-w-5xl w-full max-h-[90vh] bg-stone-950 rounded-2xl border border-white/20 overflow-hidden shadow-2xl flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              type="button"
              data-gallery-close aria-label={t('common.close')} onClick={() => setActiveImage(null)}
              className="absolute top-4 right-4 z-20 w-10 h-10 rounded-full bg-black/70 text-white hover:text-[#fae28e] border border-white/20 flex items-center justify-center text-lg transition-colors cursor-pointer"
            >
              &times;
            </button>
            <div className="relative flex-1 overflow-hidden bg-black flex items-center justify-center">
              <HotelImage
                src={activeImage.image}
                alt={activeImage.title || 'Coco Hotel'}
                className="max-h-[75vh] w-auto max-w-full object-contain"
              />
            </div>
            <div className="p-6 bg-stone-950 border-t border-white/10 flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-widest text-[#fae28e] font-semibold">{t('gallery.title')}</p>
                <h4 className="text-lg font-serif text-white font-bold">{activeImage.title || 'Coco Hotel'}</h4>
              </div>
              <Link
                to="/booking"
                className="px-5 py-2.5 rounded-xl bg-gold-metallic text-stone-950 text-xs font-bold uppercase tracking-wider hover:shadow-lg transition-all"
              >
                {t('home.heroBook')}
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
