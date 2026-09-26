import HotelImage from '../components/common/HotelImage';
import { Link } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useHotel } from '../hooks/useHotel';
import { useLanguage } from '../hooks/useLanguage';
import Container from '../components/common/Container';
import SectionTitle from '../components/common/SectionTitle';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function AboutPage() {
  const { hotelInfo } = useHotel();
  const { t } = useLanguage();

  usePageMeta({
    title: t('meta.aboutTitle'),
    description: t('meta.aboutDesc'),
    canonicalPath: '/about',
  });

  const hotelName = hotelInfo?.name || 'Coco Hotel';
  const aboutTitle = hotelInfo?.about_title || t('about.title');
  const aboutText = hotelInfo?.about_text;
  const address = hotelInfo?.address;
  const checkInTime = hotelInfo?.check_in_time;
  const checkOutTime = hotelInfo?.check_out_time;

  return (
    <div className="flex flex-col bg-theme-main transition-colors duration-200">
      {/* 1. HERO (Split layout matching reference with lobby photo & wave pattern) */}
      <section
        aria-label="About Coco Hotel Header"
        className="relative bg-theme-secondary text-theme-main py-16 sm:py-24 border-b border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern variant="hero" className="opacity-30 pointer-events-none" />

        <Container className="relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-center">
            {/* Left text column */}
            <div className="lg:col-span-6 space-y-6">
              <RevealOnScroll variant="up">
                <p className="font-serif italic text-lg sm:text-xl text-theme-gold">
                  {t('home.aboutSubtitle')}
                </p>
                <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mt-1 mb-4">
                  {aboutTitle}
                </h1>
                <p className="text-base sm:text-lg text-theme-muted font-light leading-relaxed">
                  {hotelInfo?.hero_subtitle || t('home.aboutParagraph1')}
                </p>
                <div className="pt-4">
                  <Link
                    to="/booking"
                    className="inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 active:scale-[0.98] transition-all shadow-md focus-visible:outline-2 focus-visible:outline-[var(--color-gold)]"
                  >
                    {t('nav.bookNow')} &rarr;
                  </Link>
                </div>
              </RevealOnScroll>
            </div>

            {/* Right lobby photo column matching reference */}
            <div className="lg:col-span-6">
              <RevealOnScroll variant="fade" delay={150}>
                <div className="relative rounded-3xl overflow-hidden shadow-2xl border border-[var(--color-gold-border)] group">
                  <HotelImage
                    src={hotelInfo?.about_image}
                    alt="Coco Hotel Grand Lobby & Lounge"
                    className="w-full h-80 sm:h-96 lg:h-[420px] object-cover group-hover:scale-102 transition-transform duration-700 ease-out"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent pointer-events-none" />
                  <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-xs text-white/90 px-4 py-2 bg-black/50 backdrop-blur-md rounded-2xl border border-white/10">
                    <span className="font-serif tracking-wider font-semibold">{hotelName}</span>
                    <span className="text-[10px] uppercase tracking-widest text-amber-300 font-semibold">{t('nav.about')}</span>
                  </div>
                </div>
              </RevealOnScroll>
            </div>
          </div>
        </Container>
      </section>

      {/* 2. EDITORIAL QUOTE BLOCK */}
      <section className="py-12 bg-theme-main border-b border-theme">
        <Container>
          <RevealOnScroll variant="fade">
            <div className="max-w-3xl mx-auto text-center px-4 py-8 border-y border-[var(--color-gold-border)]">
              <span className="font-serif text-3xl sm:text-4xl text-theme-gold block mb-2">&ldquo;</span>
              <p className="font-serif text-xl sm:text-2xl text-theme-main italic leading-relaxed">
                {t('home.tranquilityDetailText')}
              </p>
              <div className="mt-4 flex items-center justify-center gap-2">
                <span className="h-px w-8 bg-theme-gold" />
                <span className="text-xs uppercase tracking-widest text-theme-gold font-bold">{hotelName}</span>
                <span className="h-px w-8 bg-theme-gold" />
              </div>
            </div>
          </RevealOnScroll>
        </Container>
      </section>

      {/* 3. THE STORY / OVERVIEW */}
      <section aria-label="Our Story" className="py-16 sm:py-24 bg-theme-main">
        <Container>
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-16 items-start">
            {/* Story text */}
            <div className="lg:col-span-7 space-y-6">
              <RevealOnScroll variant="left">
                <SectionTitle
                  subtitle={t('about.theExperience')}
                  title={t('about.quietCornerTitle')}
                />

                {aboutText ? (
                  <div className="text-base text-theme-muted leading-relaxed space-y-4 whitespace-pre-line font-light">
                    {aboutText}
                  </div>
                ) : (
                  <div className="text-base text-theme-muted leading-relaxed space-y-4 font-light">
                    <p>
                      {t('about.p1')}
                    </p>
                    <p>
                      {t('about.p2')}
                    </p>
                  </div>
                )}



                <div className="pt-4 flex flex-wrap gap-4">
                  <Link
                    to="/rooms"
                    className="inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 active:scale-[0.98] transition-all shadow-md focus-visible:outline-2 focus-visible:outline-[var(--color-gold)]"
                  >
                    {t('about.viewAccommodations')} &rarr;
                  </Link>
                  <Link
                    to="/contact"
                    className="inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest border border-[var(--color-gold)] text-theme-gold hover:bg-theme-surface rounded-full transition-all focus-visible:outline-2 focus-visible:outline-[var(--color-gold)]"
                  >
                    {t('about.contactConcierge')}
                  </Link>
                </div>
              </RevealOnScroll>
            </div>

            {/* Sanctuary values card */}
            <div className="lg:col-span-5 space-y-6">
              <RevealOnScroll variant="right" delay={150}>
                <div className="p-8 sm:p-10 bg-theme-surface border border-[var(--color-gold-border)] rounded-3xl shadow-2xl space-y-6 transition-colors duration-200">
                  <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-theme-gold pb-2 border-b border-theme">
                    {t('about.coreEssentials')}
                  </h2>

                  <div className="space-y-5 text-sm text-theme-muted">
                    <div>
                      <h3 className="font-serif font-bold text-base text-theme-main mb-1">{t('about.restfulSpacesTitle')}</h3>
                      <p className="text-xs leading-relaxed text-theme-muted font-light">
                        {t('about.restfulSpacesDesc')}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-serif font-bold text-base text-theme-main mb-1">{t('about.attentiveHospitalityTitle')}</h3>
                      <p className="text-xs leading-relaxed text-theme-muted font-light">
                        {t('about.attentiveHospitalityDesc')}
                      </p>
                    </div>

                    <div>
                      <h3 className="font-serif font-bold text-base text-theme-main mb-1">{t('about.convenientLocationTitle')}</h3>
                      <p className="text-xs leading-relaxed text-theme-muted font-light">
                        {t('about.convenientLocationDesc')}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Practical stay details card */}
                {(checkInTime || checkOutTime || address) && (
                  <div className="p-6 bg-theme-elevated border border-theme rounded-2xl space-y-3 text-xs text-theme-muted mt-6 transition-colors duration-200 shadow-md">
                    <h3 className="font-bold text-theme-main uppercase tracking-wider text-[11px]">
                      {t('about.guestStayDetails')}
                    </h3>
                    {address && (
                      <p className="text-theme-muted font-light">
                        <strong className="text-theme-main">{t('home.address')}:</strong> {address}
                      </p>
                    )}
                    {(checkInTime || checkOutTime) && (
                      <div className="grid grid-cols-2 gap-2 pt-2 border-t border-theme">
                        {checkInTime && (
                          <p>
                            <strong className="text-theme-main">{t('booking.checkIn')}:</strong> {checkInTime}
                          </p>
                        )}
                        {checkOutTime && (
                          <p>
                            <strong className="text-theme-main">{t('booking.checkOut')}:</strong> {checkOutTime}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </RevealOnScroll>
            </div>
          </div>
        </Container>
      </section>
    </div>
  );
}
