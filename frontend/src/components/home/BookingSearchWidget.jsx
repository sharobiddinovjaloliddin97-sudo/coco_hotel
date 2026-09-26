import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../../hooks/useLanguage';

function getTodayString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getTomorrowString() {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const year = tomorrow.getFullYear();
  const month = String(tomorrow.getMonth() + 1).padStart(2, '0');
  const day = String(tomorrow.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export default function BookingSearchWidget({ className = '', glass = false }) {
  const navigate = useNavigate();
  const { t } = useLanguage();
  const today = getTodayString();
  const tomorrow = getTomorrowString();

  const [checkIn, setCheckIn] = useState(today);
  const [checkOut, setCheckOut] = useState(tomorrow);
  const [adults, setAdults] = useState(2);
  const [children, setChildren] = useState(0);
  const [validationError, setValidationError] = useState('');

  const handleCheckInChange = (e) => {
    const newCheckIn = e.target.value;
    setCheckIn(newCheckIn);
    setValidationError('');
    if (checkOut <= newCheckIn) {
      const nextDay = new Date(`${newCheckIn}T00:00:00`);
      nextDay.setDate(nextDay.getDate() + 1);
      const y = nextDay.getFullYear();
      const m = String(nextDay.getMonth() + 1).padStart(2, '0');
      const d = String(nextDay.getDate()).padStart(2, '0');
      setCheckOut(`${y}-${m}-${d}`);
    }
  };

  const handleCheckOutChange = (e) => {
    setCheckOut(e.target.value);
    setValidationError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!checkIn) {
      setValidationError(t('widget.selectCheckIn'));
      return;
    }
    if (!checkOut) {
      setValidationError(t('widget.selectCheckOut'));
      return;
    }
    if (checkIn < today) {
      setValidationError(t('widget.pastDateError'));
      return;
    }
    if (checkOut <= checkIn) {
      setValidationError(t('widget.dateOrderError'));
      return;
    }
    if (adults < 1) {
      setValidationError(t('widget.adultRequired'));
      return;
    }

    const searchParams = new URLSearchParams({
      checkIn,
      checkOut,
      adults: String(adults),
      children: String(children),
    });

    navigate(`/booking?${searchParams.toString()}`);
  };

  const containerClasses = glass
    ? `bg-black/65 backdrop-blur-xl border border-white/20 text-white rounded-2xl sm:rounded-3xl shadow-2xl p-4 sm:p-7 ${className}`
    : `bg-theme-surface rounded-2xl sm:rounded-3xl shadow-xl border border-theme p-4 sm:p-7 transition-colors duration-200 ${className}`;

  const labelClasses = glass
    ? "text-[11px] font-bold uppercase tracking-[0.18em] text-amber-300 mb-1.5 flex items-center gap-1.5"
    : "text-[11px] font-bold uppercase tracking-[0.18em] text-theme-gold mb-1.5 flex items-center gap-1.5";

  const inputClasses = glass
    ? "w-full px-3.5 py-3 sm:py-2.5 bg-black/40 border border-white/25 rounded-xl text-sm font-medium text-white placeholder-white/60 focus:border-amber-400 focus:bg-black/60 focus:outline-none transition-colors"
    : "w-full px-3.5 py-3 sm:py-2.5 bg-theme-input border border-theme rounded-xl text-sm font-medium text-theme-main focus:border-[var(--color-gold)] focus:outline-none transition-colors";

  const iconClasses = glass ? "w-3.5 h-3.5 text-amber-300 shrink-0" : "w-3.5 h-3.5 text-theme-gold shrink-0";

  return (
    <div className={containerClasses}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Check-In */}
          <div className="flex flex-col">
            <label htmlFor="search-check-in" className={labelClasses}>
              <svg className={iconClasses} fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 9v7.5" />
              </svg>
              {t('booking.checkIn')}
            </label>
            <input
              type="date"
              id="search-check-in"
              min={today}
              value={checkIn}
              onChange={handleCheckInChange}
              required
              className={inputClasses}
            />
          </div>

          {/* Check-Out */}
          <div className="flex flex-col">
            <label htmlFor="search-check-out" className={labelClasses}>
              <svg className={iconClasses} fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 9v7.5" />
              </svg>
              {t('booking.checkOut')}
            </label>
            <input
              type="date"
              id="search-check-out"
              min={checkIn || today}
              value={checkOut}
              onChange={handleCheckOutChange}
              required
              className={inputClasses}
            />
          </div>

          {/* Adults */}
          <div className="flex flex-col">
            <label htmlFor="search-adults" className={labelClasses}>
              <svg className={iconClasses} fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
              {t('rooms.adults')}
            </label>
            <select
              id="search-adults"
              value={adults}
              onChange={(e) => setAdults(Number(e.target.value))}
              className={inputClasses}
            >
              {[1, 2, 3, 4, 5, 6].map((num) => (
                <option key={num} value={num} className="bg-stone-900 text-white">
                  {num} {num === 1 ? t('booking.adult') : t('booking.adultsPlural')}
                </option>
              ))}
            </select>
          </div>

          {/* Children */}
          <div className="flex flex-col">
            <label htmlFor="search-children" className={labelClasses}>
              <svg className={iconClasses} fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
              </svg>
              {t('rooms.children')}
            </label>
            <select
              id="search-children"
              value={children}
              onChange={(e) => setChildren(Number(e.target.value))}
              className={inputClasses}
            >
              {[0, 1, 2, 3, 4].map((num) => (
                <option key={num} value={num} className="bg-stone-900 text-white">
                  {num} {num === 1 ? t('booking.child') : t('booking.childrenPlural')}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Validation error message */}
        {validationError && (
          <p role="alert" className="text-xs text-rose-400 font-medium">
            {validationError}
          </p>
        )}

        {/* Action Button */}
        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 active:scale-[0.98] transition-all shadow-md focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] cursor-pointer"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth="2.5" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
            {t('home.checkRooms')}
          </button>
        </div>
      </form>
    </div>
  );
}
