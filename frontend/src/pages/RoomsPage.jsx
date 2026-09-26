import { useState, useEffect, useMemo } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useLanguage } from '../hooks/useLanguage';
import { getRooms } from '../api/rooms';
import Container from '../components/common/Container';
import SectionTitle from '../components/common/SectionTitle';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import RoomCard from '../components/rooms/RoomCard';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

export default function RoomsPage() {
  const { language, t } = useLanguage();
  usePageMeta({
    title: t('meta.roomsTitle'),
    description: t('meta.roomsDesc'),
    canonicalPath: '/rooms',
  });

  const [searchParams] = useSearchParams();
  const searchParamsString = searchParams.toString();

  const [rooms, setRooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('all');

  const fetchRooms = () => {
    setLoading(true);
    setError(false);
    getRooms()
      .then((data) => {
        setError(false);
        setRooms(data || []);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  };

  useEffect(() => {
    let isMounted = true;
    getRooms()
      .then((data) => {
        if (isMounted) {
          setError(false);
        setRooms(data || []);
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

  const categories = [
    { id: 'all', label: t('common.all') },
    { id: 'deluxe', label: 'Deluxe' },
    { id: 'suites', label: 'Suites' },
    { id: 'family', label: language === 'uz' ? 'Oilaviy' : language === 'ru' ? 'Семейные' : 'Family' },
  ];

  const filteredRooms = useMemo(() => {
    if (selectedFilter === 'all') return rooms;
    return rooms.filter((room) => {
      const slug = (room.slug || '').toLowerCase();
      const name = (room.name || '').toLowerCase();
      if (selectedFilter === 'deluxe') {
        return slug.includes('deluxe') || name.includes('deluxe');
      }
      if (selectedFilter === 'suites') {
        return slug.includes('suite') || name.includes('suite');
      }
      if (selectedFilter === 'family') {
        return slug.includes('family') || name.includes('family') || room.max_adults >= 3;
      }
      return true;
    });
  }, [rooms, selectedFilter]);

  return (
    <div className="flex flex-col bg-theme-main transition-colors duration-200">
      {/* 1. ROOMS PAGE HERO */}
      <section
        aria-label="Rooms Overview"
        className="relative bg-theme-secondary text-theme-main py-16 sm:py-24 border-b border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern variant="top-right" className="opacity-30 pointer-events-none" />

        <Container className="relative z-10 text-center">
          <RevealOnScroll variant="up">
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-theme-gold mb-3">
              Coco Hotel Accommodations
            </p>
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mb-4">
              Rooms & Suites
            </h1>
            <p className="text-base sm:text-lg text-theme-muted font-light max-w-2xl mx-auto leading-relaxed mb-8">
              Discover elegant rooms designed for your comfort and tranquil relaxation.
            </p>

            {/* Filter Pills matching reference */}
            <div className="inline-flex items-center p-1 rounded-full border border-theme bg-theme-surface shadow-md">
              {categories.map((cat) => (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setSelectedFilter(cat.id)}
                  className={`px-5 py-2 text-xs font-bold tracking-wider rounded-full transition-all cursor-pointer ${
                    selectedFilter === cat.id
                      ? 'bg-gold-metallic text-stone-950 shadow-sm'
                      : 'text-theme-muted hover:text-theme-main'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </RevealOnScroll>
        </Container>
      </section>

      {/* 2. ROOM LISTINGS */}
      <section aria-label="Available Rooms" className="py-16 sm:py-24 bg-theme-main transition-colors duration-200">
        <Container>
          {loading ? (
            <LoadingState />
          ) : error ? (
            <ErrorState onRetry={fetchRooms} />
          ) : filteredRooms.length > 0 ? (
            <div className="space-y-12">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {filteredRooms.map((room, idx) => (
                  <RevealOnScroll key={room.id} variant="up" delay={idx * 80}>
                    <RoomCard
                      room={room}
                      searchParams={searchParamsString}
                    />
                  </RevealOnScroll>
                ))}
              </div>
            </div>
          ) : (
            <div className="p-12 bg-theme-surface border border-theme rounded-2xl text-center max-w-xl mx-auto shadow-md">
              <h2 className="font-serif text-xl font-bold text-theme-main mb-3">
                No rooms match the selected filter
              </h2>
              <p className="text-sm text-theme-muted mb-6 leading-relaxed font-light">
                Please select another category or view all accommodations.
              </p>
              <button
                type="button"
                onClick={() => setSelectedFilter('all')}
                className="inline-flex items-center px-6 py-3 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 transition-colors shadow-sm"
              >
                Reset Filter
              </button>
            </div>
          )}
        </Container>
      </section>

      {/* 3. BOOKING CTA SECTION */}
      <section
        aria-label="Reservation Inquiry"
        className="relative py-16 sm:py-24 bg-theme-secondary border-t border-theme overflow-hidden transition-colors duration-200"
      >
        <GoldWavePattern variant="subtle" className="opacity-20 pointer-events-none" />

        <Container className="relative z-10 text-center">
          <RevealOnScroll variant="up">
            <SectionTitle
              subtitle={t('rooms.planYourVisit')}
              title={t('rooms.readyTitle')}
              centered
            />
            <p className="text-sm sm:text-base text-theme-muted max-w-xl mx-auto mb-8 leading-relaxed font-light">
              {t('rooms.readyDesc')}
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to={searchParamsString ? `/booking?${searchParamsString}` : '/booking'}
                className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 transition-all shadow-md focus-visible:outline-2 focus-visible:outline-[var(--color-gold)]"
              >
                {t('rooms.bookStay')} &rarr;
              </Link>
              <Link
                to="/contact"
                className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-xs font-bold uppercase tracking-widest border border-[var(--color-gold)] text-theme-gold hover:bg-theme-surface rounded-full transition-all focus-visible:outline-2 focus-visible:outline-[var(--color-gold)]"
              >
                {t('rooms.inquireDirectly')}
              </Link>
            </div>
          </RevealOnScroll>
        </Container>
      </section>
    </div>
  );
}
