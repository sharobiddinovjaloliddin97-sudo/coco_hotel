import HotelImage from '../../components/common/HotelImage';
import { Link } from 'react-router-dom';
import { formatUZSPrice } from '../../utils/formatters';
import { useLanguage } from '../../hooks/useLanguage';
import { getRoomImageUrl } from '../../utils/roomImages';

export default function RoomCard({ room, searchParams = '' }) {
  const { t, language } = useLanguage();
  if (!room) return null;

  const displayImage = getRoomImageUrl(room);
  const imageAlt = room.primary_image?.alt_text || room.name;

  const querySuffix = searchParams ? (searchParams.startsWith('?') ? searchParams : `?${searchParams}`) : '';
  const bookingQuery = searchParams
    ? `${searchParams.includes('?') ? searchParams : `?${searchParams}`}&room=${room.id}`
    : `?room=${room.id}`;

  return (
    <article className="group flex flex-col bg-white dark:bg-[#151922] border border-stone-200 dark:border-stone-800/80 rounded-2xl overflow-hidden shadow-md hover:shadow-xl hover:border-amber-400/80 dark:hover:border-amber-400/60 transition-all duration-300">
      {/* 1. Image Container */}
      <div className="relative aspect-16/10 sm:aspect-4/3 w-full overflow-hidden bg-stone-100 dark:bg-stone-900">
        <HotelImage
          src={displayImage}
          alt={imageAlt}
          loading="lazy"
          decoding="async"
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 ease-out"
        />

        {/* Featured Badge */}
        {room.is_featured && (
          <span className="absolute top-3.5 left-3.5 bg-black/80 border border-amber-400 text-amber-400 text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full backdrop-blur-md shadow-md">
            ★ {t('rooms.featured')}
          </span>
        )}

        {/* Breakfast Included pill */}
        <span className="absolute bottom-3 left-3 bg-black/75 border border-white/20 text-white text-[11px] font-medium px-2.5 py-0.5 rounded-md backdrop-blur-md">
          ☕ {language === 'ru' ? 'Завтрак включен' : language === 'uz' ? 'Nonushta kiritilgan' : 'Breakfast included'}
        </span>
      </div>

      {/* 2. Card Content */}
      <div className="flex-1 flex flex-col p-5 sm:p-6">
        {/* Room Title */}
        <h3 className="text-xl sm:text-2xl font-serif font-bold text-stone-900 dark:text-white mb-2 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors">
          <Link
            to={`/rooms/${room.slug}${querySuffix}`}
            className="focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400 rounded-sm"
          >
            {room.name}
          </Link>
        </h3>

        {/* Description */}
        {room.short_description && (
          <p className="text-sm text-stone-600 dark:text-stone-300 line-clamp-2 mb-4 leading-relaxed font-normal">
            {room.short_description}
          </p>
        )}

        {/* Room Badges / Specs */}
        <div className="flex flex-wrap items-center gap-2 mb-6 py-3 border-y border-stone-150 dark:border-stone-800">
          {room.max_adults != null && (
            <span
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-stone-100 dark:bg-stone-800/90 text-xs font-semibold text-stone-800 dark:text-stone-200 border border-stone-200/70 dark:border-stone-700/60"
              title="Sig‘im"
            >
              <svg className="w-3.5 h-3.5 text-amber-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>
                {room.max_adults} {room.max_adults === 1 ? t('booking.adult') : t('booking.adultsPlural')}
                {room.max_children != null && room.max_children > 0 && ` + ${room.max_children} ${t('booking.childrenPlural')}`}
              </span>
            </span>
          )}

          {room.bed_type && (
            <span
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-stone-100 dark:bg-stone-800/90 text-xs font-semibold text-stone-800 dark:text-stone-200 border border-stone-200/70 dark:border-stone-700/60"
              title="Karavot turi"
            >
              <svg className="w-3.5 h-3.5 text-amber-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
              <span>{room.bed_type}</span>
            </span>
          )}

          {room.room_size && (
            <span
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-stone-100 dark:bg-stone-800/90 text-xs font-semibold text-stone-800 dark:text-stone-200 border border-stone-200/70 dark:border-stone-700/60"
              title="Maydoni"
            >
              <svg className="w-3.5 h-3.5 text-amber-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
              <span>{room.room_size} m²</span>
            </span>
          )}
        </div>

        {/* 3. Pricing and Actions: Bold, High-Contrast and Clear */}
        <div className="mt-auto pt-2 flex flex-wrap items-end justify-between gap-3">
          <div>
            <span className="text-[11px] uppercase tracking-wider text-stone-500 dark:text-stone-400 block font-semibold mb-0.5">
              {t('rooms.startingFrom')}
            </span>
            <div className="flex items-baseline gap-1">
              <span className="text-2xl font-bold font-sans text-amber-600 dark:text-amber-400 tracking-tight">
                {formatUZSPrice(room.price_per_night, language)}
              </span>
              <span className="text-xs text-stone-500 dark:text-stone-400 font-medium">
                / {t('rooms.perNight')}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Link
              to={`/rooms/${room.slug}${querySuffix}`}
              className="px-3.5 py-2 text-xs font-bold text-stone-700 dark:text-stone-200 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-500/10 rounded-xl transition-colors"
            >
              {t('rooms.viewRoom')}
            </Link>
            <Link
              to={`/booking${bookingQuery}`}
              className="px-4 py-2.5 text-xs font-bold uppercase tracking-wider bg-gold-metallic gold-glow text-stone-950 rounded-xl hover:brightness-105 active:scale-95 transition-all shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
            >
              {t('rooms.bookNow')}
            </Link>
          </div>
        </div>
      </div>
    </article>
  );
}
