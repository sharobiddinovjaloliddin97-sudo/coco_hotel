import HotelImage from '../components/common/HotelImage';
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useLanguage } from '../hooks/useLanguage';
import { getPromotions } from '../api/hotel';
import Container from '../components/common/Container';
import SectionTitle from '../components/common/SectionTitle';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function PromotionsPage() {
  const { t, language } = useLanguage();
  usePageMeta({
    title: t('meta.offersTitle'),
    description: t('meta.offersDesc'),
    canonicalPath: '/promotions',
  });

  const [promotions, setPromotions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const handleRetry = () => {
    setLoading(true);
    setError(false);
    getPromotions()
      .then((data) => {
        setPromotions(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  };

  useEffect(() => {
    let isMounted = true;
    getPromotions()
      .then((data) => {
        if (isMounted) {
          setPromotions(Array.isArray(data) ? data : []);
          setLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setError(true);
          setLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [language]);



  return (
    <div className="flex flex-col bg-theme-main transition-colors duration-200">
      {/* 1. HERO HEADER */}
      <section
        aria-label="Promotions Header"
        className="relative bg-theme-secondary text-theme-main py-20 sm:py-28 border-b border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern opacity={0.14} />
        <Container className="relative z-10 text-center">
          <RevealOnScroll variant="up">
            <span className="inline-block px-3.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-[0.25em] text-[#fae28e] bg-[#dfba56]/15 border border-[#dfba56]/30 mb-4">
              {t('promotions.specialPrivileges')}
            </span>
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mb-4">
              {t('promotions.exclusiveOffers')}
            </h1>
            <p className="text-base sm:text-lg text-theme-muted font-light max-w-2xl mx-auto leading-relaxed">
              {t('promotions.intro')}
            </p>
          </RevealOnScroll>
        </Container>
      </section>

      {/* 2. PROMOTIONS LIST */}
      <section aria-label="Available Offers" className="relative py-16 sm:py-24 bg-theme-main">
        <GoldWavePattern opacity={0.06} />
        <Container className="relative z-10">
          {loading ? (
            <LoadingState />
          ) : error ? (
            <ErrorState onRetry={handleRetry} />
          ) : promotions.length === 0 ? (
            <div className="text-center py-16 px-6 bg-theme-surface border border-theme rounded-2xl max-w-xl mx-auto space-y-5 shadow-2xl">
              <span className="inline-block p-4 rounded-full bg-theme-elevated text-[#dfba56] border border-[#dfba56]/30 shadow-md">
                <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 11.25v8.25a1.5 1.5 0 01-1.5 1.5H4.5a1.5 1.5 0 01-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 109.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1114.625 7.5H12m0 0V21m-8.625-9.75h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125z" />
                </svg>
              </span>
              <h2 className="font-serif text-2xl font-bold text-theme-main">
                {t('promotions.noActiveOffers')}
              </h2>
              <p className="text-sm text-theme-muted leading-relaxed max-w-md mx-auto font-light">
                {t('promotions.noActiveDesc')}
              </p>
              <div className="pt-3 flex flex-wrap items-center justify-center gap-4">
                <Link
                  to="/rooms"
                  className="inline-flex items-center px-6 py-3 text-xs font-bold uppercase tracking-widest bg-gold-metallic text-stone-950 rounded-xl hover:shadow-lg transition-all"
                >
                  {t('rooms.browseAccommodations')}
                </Link>
                <Link
                  to="/contact"
                  className="inline-flex items-center px-6 py-3 text-xs font-semibold uppercase tracking-widest border border-[#dfba56] text-[#dfba56] hover:bg-[#dfba56]/10 rounded-xl transition-all"
                >
                  {t('rooms.contactConcierge')}
                </Link>
              </div>
            </div>
          ) : (
            <div className="space-y-12">
              <RevealOnScroll variant="up">
                <SectionTitle
                  subtitle={t('promotions.curatedStays')}
                  title={t('promotions.currentPrivileges')}
                />
              </RevealOnScroll>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {promotions.map((promo, idx) => {

                  return (
                    <RevealOnScroll key={promo.id || idx} variant="up" delay={idx * 80}>
                      <article className="group bg-theme-surface border border-theme rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl hover:border-[#dfba56]/70 transition-all duration-300 flex flex-col h-full">
                        <div className="relative aspect-16/9 overflow-hidden bg-theme-elevated">
                          <HotelImage
                            src={promo.image}
                            alt={promo.title}
                            loading="lazy"
                            decoding="async"
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
                          />
                          <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-60" />
                          <span className="absolute top-4 left-4 px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-stone-950/80 backdrop-blur-md border border-[#dfba56]/40 text-[#fae28e]">
                            Coco Privilege
                          </span>
                        </div>

                        <div className="p-7 sm:p-8 flex-1 flex flex-col">
                          <h2 className="font-serif text-xl sm:text-2xl font-bold text-theme-main group-hover:text-[#fae28e] transition-colors mb-3">
                            {promo.title}
                          </h2>
                          <p className="text-sm text-theme-muted leading-relaxed mb-6 line-clamp-3 font-light flex-1">
                            {promo.short_description}
                          </p>

                          <div className="pt-5 border-t border-theme flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                            <div className="text-theme-muted font-light">
                              {promo.valid_until ? (
                                <span className="font-mono text-[11px] text-[#fae28e]">
                                  {t('home.validUntil')} {promo.valid_until}
                                </span>
                              ) : (
                                <span className="text-[#fae28e] font-medium text-[11px]">
                                  {t('home.limitedAvailability')}
                                </span>
                              )}
                            </div>
                            <Link
                              to={`/promotions/${promo.slug}`}
                              className="font-bold text-[#fae28e] hover:underline self-start sm:self-auto inline-flex items-center gap-1 uppercase tracking-wider text-[11px]"
                            >
                              {t('promotions.viewDetails')} &rarr;
                            </Link>
                          </div>
                        </div>
                      </article>
                    </RevealOnScroll>
                  );
                })}
              </div>
            </div>
          )}
        </Container>
      </section>
    </div>
  );
}
