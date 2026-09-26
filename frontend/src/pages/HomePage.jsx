import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useHotel } from '../hooks/useHotel';
import { useLanguage } from '../hooks/useLanguage';
import { usePageMeta } from '../hooks/usePageMeta';
import { getFeaturedRooms } from '../api/rooms';
import { getServices, getGallery, getPromotions } from '../api/hotel';
import Container from '../components/common/Container';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import HotelImage from '../components/common/HotelImage';
import RoomCard from '../components/rooms/RoomCard';
import ServiceIcon from '../components/common/ServiceIcon';
import HeroSlider from '../components/home/HeroSlider';

export default function HomePage() {
  const { hotelInfo, error: hotelError } = useHotel();
  const { language, t } = useLanguage();
  const [result, setResult] = useState({ language: null });
  const [attempt, setAttempt] = useState(0);
  const loading = result.language !== language || result.attempt !== attempt;

  usePageMeta({ title: t('meta.homeTitle'), description: t('meta.homeDesc'), canonicalPath: '/' });

  useEffect(() => {
    let active = true;
    Promise.allSettled([getFeaturedRooms(), getServices(), getGallery(), getPromotions()])
      .then(([rooms, services, gallery, promotions]) => {
        if (active) setResult({ language, attempt, rooms, services, gallery, promotions });
      });
    return () => { active = false; };
  }, [language, attempt]);

  const list = (name) => (result[name]?.status === 'fulfilled' ? result[name].value || [] : []);
  const name = hotelInfo?.name || 'Coco Hotel';

  const bookingBadgeText =
    language === 'ru'
      ? 'Оценка по отзывам Booking.com: 8,8 — Потрясающе'
      : language === 'uz'
      ? "Booking.com baholashi: 8.8 — Ajoyib va qulay"
      : 'Booking.com Guest Review Score: 8.8 — Fabulous';

  return (
    <div className="hotel-home bg-theme-main transition-colors duration-200">
      {/* 1. Full-Width Immersive Rotating Hero Slider */}
      <HeroSlider hotelInfo={hotelInfo} />

      {/* 2. Trust & Booking.com Rating Banner */}
      <section className="border-b border-theme bg-theme-surface py-5">
        <Container>
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <span className="inline-flex items-center justify-center w-11 h-11 rounded-xl bg-amber-400/15 text-amber-500 font-bold text-lg border border-amber-400/30">
                8.8
              </span>
              <div>
                <p className="text-sm font-bold text-theme-main">{bookingBadgeText}</p>
                <p className="text-xs text-theme-muted">
                  {language === 'ru'
                    ? '30 номеров • Завтрак включен • Бесплатная парковка • 24/7 Сервис'
                    : language === 'uz'
                    ? "30 ta shinam xona • Nonushta kiritilgan • Bepul avtoturargoh • 24/7 Xizmat"
                    : '30 elegant rooms • Breakfast included • Free private parking • 24/7 Reception'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-6 text-xs text-theme-muted">
              <div className="flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500" />
                <span>{language === 'ru' ? 'Свободные номера есть' : language === 'uz' ? 'Xonalar mavjud' : 'Rooms available'}</span>
              </div>
              <Link to="/rooms" className="font-semibold text-theme-gold hover:underline">
                {language === 'ru' ? 'Прайс-лист' : language === 'uz' ? 'Narxlar ro‘yxati' : 'View Rates'} ↗
              </Link>
            </div>
          </div>
        </Container>
      </section>

      {hotelError && (
        <Container>
          <p role="alert" className="mt-6 text-theme-muted">
            {t('common.errorMessage')}
          </p>
        </Container>
      )}

      {/* 3. Featured Rooms Showcase */}
      <section className="editorial-section">
        <Container>
          <div className="section-heading">
            <div>
              <p className="eyebrow">{t('home.accommodations')}</p>
              <h2>{t('home.featuredRooms')}</h2>
            </div>
            <Link className="text-link" to="/rooms">
              {t('home.viewAllRooms')} ↗
            </Link>
          </div>

          {loading ? (
            <LoadingState />
          ) : result.rooms?.status === 'rejected' ? (
            <ErrorState
              title={t('common.errorTitle')}
              message={t('common.errorMessage')}
              onRetry={() => setAttempt((a) => a + 1)}
            />
          ) : list('rooms').length ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-7">
              {list('rooms').map((room) => (
                <RoomCard key={room.id} room={room} />
              ))}
            </div>
          ) : (
            <p className="empty-note">{t('booking.roomsUpdatingDesc')}</p>
          )}
        </Container>
      </section>

      {/* 4. Hotel Story / About Section */}
      <section className="story-section">
        <Container className="story-grid">
          <HotelImage
            src={hotelInfo?.about_image || '/images/hero/hero_lobby.jpg'}
            alt={name}
            loading="lazy"
            className="story-photo shadow-lg"
          />
          <div className="story-copy">
            <p className="eyebrow">{t('home.aboutSubtitle')}</p>
            <h2>{hotelInfo?.about_title || t('home.aboutTitle')}</h2>
            <p className="whitespace-pre-line text-theme-muted leading-relaxed">
              {hotelInfo?.about_text || t('home.aboutParagraph1')}
            </p>
            <div className="pt-2">
              <Link className="text-link" to="/about">
                {t('home.readStory')} ↗
              </Link>
            </div>
          </div>
        </Container>
      </section>

      {/* 5. Comprehensive Services (Booking.com verified) */}
      <section className="editorial-section">
        <Container>
          <div className="section-heading">
            <div>
              <p className="eyebrow">{t('home.servicesBadge')}</p>
              <h2>{t('home.servicesTitle')}</h2>
            </div>
            <Link className="text-link" to="/services">
              {t('home.exploreAllServices')} ↗
            </Link>
          </div>

          {loading ? (
            <LoadingState />
          ) : result.services?.status === 'rejected' ? (
            <ErrorState onRetry={() => setAttempt((a) => a + 1)} />
          ) : (
            <div className="service-grid bg-theme-surface rounded-xl overflow-hidden shadow-sm">
              {list('services').map((service) => (
                <article key={service.id} className="service-tile hover:bg-theme-secondary/50 transition-colors">
                  <ServiceIcon name={service.icon || service.name} className="w-7 h-7 text-theme-gold" />
                  <h3 className="text-theme-main font-semibold mt-4 mb-2">{service.name}</h3>
                  <p className="text-theme-muted text-sm leading-relaxed">{service.description}</p>
                </article>
              ))}
            </div>
          )}
        </Container>
      </section>

      {/* 6. Gallery Preview */}
      {!loading && list('gallery').length > 0 && (
        <section className="editorial-section pt-0">
          <Container>
            <div className="section-heading">
              <div>
                <p className="eyebrow">{t('home.galleryBadge')}</p>
                <h2>{t('home.galleryTitle')}</h2>
              </div>
              <Link className="text-link" to="/gallery">
                {t('home.viewFullGallery')} ↗
              </Link>
            </div>
            <div className="editorial-gallery">
              {list('gallery')
                .slice(0, 3)
                .map((item) => (
                  <Link to="/gallery" key={item.id} className="gallery-preview shadow-sm">
                    <HotelImage
                      src={item.image}
                      alt={item.alt_text || item.title}
                      loading="lazy"
                      className="w-full h-full object-cover"
                    />
                    <span>{item.title || name} ↗</span>
                  </Link>
                ))}
            </div>
          </Container>
        </section>
      )}

      {/* 7. Highlights / Guarantees */}
      <section className="editorial-section bg-theme-secondary/40 border-y border-theme">
        <Container>
          <div className="request-steps">
            {[1, 2, 3].map((number) => (
              <article key={number}>
                <span>0{number}</span>
                <h3 className="text-theme-main">{t(`home.highlight${number}Title`)}</h3>
                <p className="text-theme-muted">{t(`home.highlight${number}Desc`)}</p>
              </article>
            ))}
          </div>
        </Container>
      </section>

      {/* 8. Location & Contacts Section */}
      <section className="visit-section">
        <Container className="visit-grid">
          <div>
            <p className="eyebrow">{t('home.locationSubtitle')}</p>
            <h2>
              {t('home.planVisit')}
              <br />
              {name}
            </h2>
            {/* Clickable Address Link */}
            <div className="mt-4">
              <a
                href={hotelInfo?.map_url || "https://yandex.uz/maps/-/CPwOM2O3"}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-start gap-2.5 text-stone-700 dark:text-stone-300 hover:text-amber-600 dark:hover:text-amber-400 transition-colors"
                title={language === 'ru' ? 'Открыть локацию в Яндекс.Картах' : language === 'uz' ? 'Lokatsiyani xaritada ochish' : 'Open in Maps'}
              >
                <span className="text-xl shrink-0 group-hover:scale-110 transition-transform">📍</span>
                <span className="underline decoration-amber-400/60 underline-offset-4 font-medium leading-relaxed">
                  {hotelInfo?.address || '156 Bogibuston Street, Tashkent 100022, Uzbekistan'}
                </span>
                <span className="text-amber-500 font-bold group-hover:translate-x-0.5 transition-transform">↗</span>
              </a>
            </div>

            <p className="text-xs text-stone-500 dark:text-stone-400 mt-2.5">
              {language === 'ru'
                ? 'Режим работы: 24/7 (Круглосуточно)'
                : language === 'uz'
                ? 'Ish tartibi: 24/7 (Kechayu kunduz)'
                : 'Working hours: 24/7 (Round-the-clock)'}
            </p>
          </div>
          <div className="visit-actions">
            {hotelInfo?.phone && (
              <a className="text-link text-base" href={`tel:${hotelInfo.phone.replace(/[\s()-]/g, '')}`}>
                📞 {hotelInfo.phone} ↗
              </a>
            )}
            {hotelInfo?.secondary_phone && (
              <a className="text-link text-sm" href={`tel:${hotelInfo.secondary_phone.replace(/[\s()-]/g, '')}`}>
                📞 {hotelInfo.secondary_phone} ↗
              </a>
            )}
            <a
              className="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-400/60 text-amber-600 dark:text-amber-400 font-bold text-xs uppercase tracking-wider transition-all shadow-xs"
              href={hotelInfo?.map_url || "https://yandex.uz/maps/-/CPwOM2O3"}
              target="_blank"
              rel="noopener noreferrer"
            >
              <span>📍</span>
              <span>
                {language === 'ru'
                  ? 'Открыть локацию (Яндекс.Карты)'
                  : language === 'uz'
                  ? 'Lokatsiyani ko‘rish (Yandex Xarita)'
                  : 'Open Location (Yandex Maps)'} ↗
              </span>
            </a>
            <Link className="hotel-button" to="/booking">
              {t('home.checkRooms')} →
            </Link>
          </div>
        </Container>
      </section>
    </div>
  );
}
