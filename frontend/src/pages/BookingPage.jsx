import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { usePageMeta } from '../hooks/usePageMeta';
import { useHotel } from '../hooks/useHotel';
import { useLanguage } from '../hooks/useLanguage';
import { getRooms } from '../api/rooms';
import { createBookingRequest } from '../api/bookings';
import { formatUZSPrice, formatDate } from '../utils/formatters';
import Container from '../components/common/Container';
import LoadingState from '../components/common/LoadingState';
import ErrorState from '../components/common/ErrorState';
import BookingSummary from '../components/booking/BookingSummary';
import RevealOnScroll from '../components/common/RevealOnScroll';
import GoldWavePattern from '../components/common/GoldWavePattern';

function getTodayString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function getTomorrowString(baseDate) {
  const date = baseDate ? new Date(`${baseDate}T00:00:00`) : new Date();
  date.setDate(date.getDate() + 1);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export default function BookingPage() {
  const { language, t } = useLanguage();
  usePageMeta({
    title: t('meta.bookingTitle'),
    description: t('meta.bookingDesc'),
    canonicalPath: '/booking',
  });
  const { hotelInfo } = useHotel();
  const [searchParams] = useSearchParams();

  const today = getTodayString();

  // Rooms list state
  const [rooms, setRooms] = useState([]);
  const [loadingRooms, setLoadingRooms] = useState(true);
  const [roomsError, setRoomsError] = useState(false);

  // Form field state initialized from search parameters
  const [roomId, setRoomId] = useState(searchParams.get('room') || '');
  const [checkIn, setCheckIn] = useState(() => {
    const paramIn = searchParams.get('checkIn');
    return paramIn && paramIn >= today ? paramIn : today;
  });
  const [checkOut, setCheckOut] = useState(() => {
    const paramIn = searchParams.get('checkIn');
    const paramOut = searchParams.get('checkOut');
    const minIn = paramIn && paramIn >= today ? paramIn : today;
    return paramOut && paramOut > minIn ? paramOut : getTomorrowString(minIn);
  });
  const [adults, setAdults] = useState(() => {
    const paramAdults = parseInt(searchParams.get('adults'), 10);
    return !isNaN(paramAdults) && paramAdults >= 1 ? paramAdults : 1;
  });
  const [childrenCount, setChildrenCount] = useState(() => {
    const paramChildren = parseInt(searchParams.get('children'), 10);
    return !isNaN(paramChildren) && paramChildren >= 0 ? paramChildren : 0;
  });
  const [fullName, setFullName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [specialRequest, setSpecialRequest] = useState('');
  const [website, setWebsite] = useState('');

  // Submission state
  const [submitting, setSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);
  const [isDuplicate, setIsDuplicate] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);

  // Error feedback state
  const [fieldErrors, setFieldErrors] = useState({});
  const [generalError, setGeneralError] = useState('');

  const fetchRooms = () => {
    setLoadingRooms(true);
    setRoomsError(false);
    getRooms()
      .then((data) => {
        const roomList = data || [];
        setRoomsError(false);
        setRooms(roomList);
        setLoadingRooms(false);

        const queryRoomId = searchParams.get('room');
        if (queryRoomId && roomList.some((r) => String(r.id) === queryRoomId)) {
          setRoomId(queryRoomId);
        } else if (roomList.length > 0) {
          setRoomId((prevId) => prevId || String(roomList[0].id));
        }
      })
      .catch(() => {
        setRoomsError(true);
        setLoadingRooms(false);
      });
  };

  useEffect(() => {
    let isMounted = true;
    getRooms()
      .then((data) => {
        if (!isMounted) return;
        const roomList = data || [];
        setRoomsError(false);
        setRooms(roomList);
        setLoadingRooms(false);

        const queryRoomId = searchParams.get('room');
        if (queryRoomId && roomList.some((r) => String(r.id) === queryRoomId)) {
          setRoomId(queryRoomId);
        } else if (roomList.length > 0) {
          setRoomId((prevId) => prevId || String(roomList[0].id));
        }
      })
      .catch(() => {
        if (!isMounted) return;
        setRoomsError(true);
        setLoadingRooms(false);
      });

    return () => {
      isMounted = false;
    };
  }, [searchParams, language]);

  // Selected room object
  const selectedRoom = rooms.find((r) => String(r.id) === String(roomId)) || null;

  // Handle room change with capacity guard
  const handleRoomChange = (e) => {
    const newId = e.target.value;
    setRoomId(newId);
    setFieldErrors((prev) => ({ ...prev, room: '' }));

    const r = rooms.find((item) => String(item.id) === newId);
    if (r) {
      if (adults > r.max_adults) {
        setAdults(r.max_adults);
      }
      if (childrenCount > r.max_children) {
        setChildrenCount(r.max_children);
      }
    }
  };

  // Handle check-in change
  const handleCheckInChange = (e) => {
    const newIn = e.target.value;
    setCheckIn(newIn);
    setFieldErrors((prev) => ({ ...prev, check_in: '', check_out: '' }));

    if (checkOut <= newIn) {
      setCheckOut(getTomorrowString(newIn));
    }
  };

  // Handle check-out change
  const handleCheckOutChange = (e) => {
    setCheckOut(e.target.value);
    setFieldErrors((prev) => ({ ...prev, check_out: '' }));
  };

  // Client validation
  const validateForm = () => {
    const errors = {};

    if (!selectedRoom) {
      errors.room = t('booking.selectRoomRequired');
    }

    if (!checkIn) {
      errors.check_in = t('booking.specifyCheckIn');
    } else if (checkIn < today) {
      errors.check_in = t('widget.pastDateError');
    }

    if (!checkOut) {
      errors.check_out = t('booking.specifyCheckOut');
    } else if (checkOut <= checkIn) {
      errors.check_out = t('widget.dateOrderError');
    }

    if (adults < 1) {
      errors.adults = t('widget.adultRequired');
    } else if (selectedRoom && adults > selectedRoom.max_adults) {
      errors.adults = `${t('booking.roomCapacityPrefix')} ${selectedRoom.max_adults} ${t('booking.adultsPlural')}.`;
    }

    if (childrenCount < 0) {
      errors.children = t('booking.childrenNegativeError');
    } else if (selectedRoom && childrenCount > selectedRoom.max_children) {
      errors.children = `${t('booking.roomCapacityPrefix')} ${selectedRoom.max_children} ${t('booking.childrenPlural')}.`;
    }

    if (!fullName.trim()) {
      errors.full_name = t('booking.fullNameRequired');
    }

    if (!phone.trim()) {
      errors.phone = t('booking.phoneRequired');
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim()) {
      errors.email = t('booking.emailRequired');
    } else if (!emailRegex.test(email.trim())) {
      errors.email = t('booking.emailValidError');
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setGeneralError('');
    if (submitting) return;

    if (!validateForm()) {
      return;
    }

    setSubmitting(true);

    const payload = {
      room: Number(roomId),
      check_in: checkIn,
      check_out: checkOut,
      adults: Number(adults),
      children: Number(childrenCount),
      full_name: fullName.trim(),
      phone: phone.trim(),
      email: email.trim(),
      special_request: specialRequest.trim(),
      website,
    };

    try {
      const response = await createBookingRequest(payload);
      setSubmissionResult(response.data);
      setIsDuplicate(response.status === 200);
      setSubmitSuccess(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      if (err.response) {
        const { status, data } = err.response;

        if (status === 400 && data && typeof data === 'object') {
          const parsedFieldErrors = {};
          let generalMsg = '';

          Object.keys(data).forEach((key) => {
            const val = data[key];
            const msg = Array.isArray(val) ? val.join(' ') : String(val);

            if (key === 'non_field_errors') {
              generalMsg = msg;
            } else if (key === 'detail') {
              generalMsg = msg;
            } else {
              parsedFieldErrors[key] = msg;
            }
          });

          setFieldErrors(parsedFieldErrors);
          if (generalMsg) {
            setGeneralError(generalMsg);
          }
        } else if (status === 429) {
          setGeneralError(t('booking.rateLimitError'));
        } else {
          setGeneralError(t('booking.submissionError'));
        }
      } else {
        setGeneralError(t('booking.networkError'));
      }
    } finally {
      setSubmitting(false);
    }
  };

  // Reset form to submit another request
  const handleReset = () => {
    setSubmitSuccess(false);
    setIsDuplicate(false);
    setSubmissionResult(null);
    setFieldErrors({});
    setGeneralError('');
    setFullName('');
    setPhone('');
    setEmail('');
    setSpecialRequest('');
  };

  return (
    <div className="relative py-12 sm:py-16 lg:py-20 bg-theme-main transition-colors duration-200 overflow-hidden">
      <GoldWavePattern variant="hero" className="opacity-20 pointer-events-none" />

      <Container className="relative z-10">
        {/* Step Indicator matching reference */}
        <div className="flex items-center justify-center gap-4 sm:gap-8 mb-10 text-xs font-bold uppercase tracking-wider">
          <div className="flex items-center gap-2 text-theme-gold">
            <span className="w-6 h-6 rounded-full bg-gold-metallic text-stone-950 flex items-center justify-center text-xs font-bold shadow-xs">1</span>
            <span>{t('booking.details') || 'Details'}</span>
          </div>
          <span className="w-6 sm:w-10 h-px bg-theme-gold opacity-40" />
          <div className="flex items-center gap-2 text-theme-gold">
            <span className="w-6 h-6 rounded-full bg-gold-metallic text-stone-950 flex items-center justify-center text-xs font-bold shadow-xs">2</span>
            <span>{t('booking.contact') || 'Contact'}</span>
          </div>
          <span className="w-6 sm:w-10 h-px bg-theme-gold opacity-40" />
          <div className="flex items-center gap-2 text-theme-muted">
            <span className="w-6 h-6 rounded-full bg-theme-elevated border border-theme text-theme-muted flex items-center justify-center text-xs font-bold">3</span>
            <span>{t('booking.review') || 'Review'}</span>
          </div>
        </div>

        {/* HERO TITLE */}
        <RevealOnScroll variant="up">
          <div className="max-w-3xl mb-10 sm:mb-14">
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-theme-gold mb-2">
              {t('booking.reservationsDesk')}
            </p>
            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-serif font-bold text-theme-main tracking-tight mb-4">
              {t('booking.title')}
            </h1>
            <p className="text-base text-theme-muted leading-relaxed font-light">
              {t('booking.intro')}
            </p>
          </div>
        </RevealOnScroll>

        {/* LOADING ROOMS */}
        {loadingRooms ? (
          <div className="py-16">
            <LoadingState />
          </div>
        ) : roomsError ? (
          <div className="max-w-xl mx-auto py-12">
            <ErrorState onRetry={fetchRooms} />
          </div>
        ) : rooms.length === 0 ? (
          <div className="max-w-xl mx-auto py-12 p-8 bg-theme-surface border border-theme rounded-xs text-center shadow-lg">
            <h2 className="font-serif text-xl font-semibold text-theme-main mb-2">
              {t('booking.roomsUpdatingTitle')}
            </h2>
            <p className="text-sm text-theme-muted mb-6 leading-relaxed font-light">
              {t('booking.roomsUpdatingDesc')}
            </p>
            {hotelInfo?.phone && (
              <a
                href={`tel:${hotelInfo.phone}`}
                className="inline-flex items-center px-6 py-3 text-xs font-semibold uppercase tracking-widest bg-theme-gold text-stone-950 rounded-xs hover:brightness-110 transition-colors"
              >
                {t('booking.callFrontDesk')} ({hotelInfo.phone})
              </a>
            )}
          </div>
        ) : submitSuccess && submissionResult ? (
          /* SUCCESS VIEW */
          <RevealOnScroll variant="fade">
            <div className="max-w-3xl mx-auto space-y-8 animate-fadeIn">
              {/* Header Status Card */}
              <div className="p-8 sm:p-10 bg-theme-surface border border-theme rounded-xs shadow-2xl text-center space-y-4">
                <div className="w-14 h-14 mx-auto rounded-full bg-theme-elevated text-theme-gold flex items-center justify-center border border-theme-gold">
                  <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </div>

                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-theme-gold">
                  {isDuplicate ? t('booking.alreadyInProgress') : t('booking.successfullySubmitted')}
                </p>

                <h2 className="text-2xl sm:text-3xl font-serif font-semibold text-theme-main">
                  {isDuplicate
                    ? t('booking.receivedAlready')
                    : t('booking.requestReceived')}
                </h2>

                <p className="text-sm text-theme-muted max-w-lg mx-auto leading-relaxed font-light">
                  {isDuplicate
                    ? t('booking.duplicateMsg')
                    : t('booking.thankYouMsg')}
                </p>

                <div className="inline-block px-3.5 py-1 bg-theme-elevated border border-theme text-xs font-mono text-theme-gold rounded-xs">
                  {t('booking.referenceId')}: #{submissionResult.id} &bull; {t('booking.status')}: {t('booking.statusReceived')}
                </div>
              </div>

              {/* Request Summary Details Card */}
              <div className="bg-theme-surface border border-theme rounded-xs p-8 shadow-xl space-y-6">
                <h3 className="text-xs font-semibold uppercase tracking-[0.2em] text-theme-gold pb-2 border-b border-theme">
                  {t('booking.submittedDetails')}
                </h3>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-sm">
                  <div>
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-0.5 font-medium">
                      {t('booking.accommodation')}
                    </span>
                    <span className="font-semibold text-theme-main">
                      {submissionResult.room_name_snapshot || selectedRoom?.name || 'Hotel Room'}
                    </span>
                    {submissionResult.price_per_night_snapshot && (
                      <span className="text-xs text-theme-muted block">
                        {formatUZSPrice(submissionResult.price_per_night_snapshot)} / {t('rooms.perNight')}
                      </span>
                    )}
                  </div>

                  <div>
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-0.5 font-medium">
                      {t('rooms.guests')}
                    </span>
                    <span className="font-medium text-theme-main">
                      {submissionResult.adults} {submissionResult.adults === 1 ? t('booking.adult') : t('booking.adultsPlural')}
                      {submissionResult.children > 0 &&
                        `, ${submissionResult.children} ${submissionResult.children === 1 ? t('booking.child') : t('booking.childrenPlural')}`}
                    </span>
                  </div>

                  <div>
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-0.5 font-medium">
                      {t('booking.checkIn')}
                    </span>
                    <span className="font-medium text-theme-main">
                      {formatDate(submissionResult.check_in)}
                    </span>
                  </div>

                  <div>
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-0.5 font-medium">
                      {t('booking.checkOut')}
                    </span>
                    <span className="font-medium text-theme-main">
                      {formatDate(submissionResult.check_out)}
                    </span>
                  </div>

                  <div>
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-0.5 font-medium">
                      {t('booking.contactName')}
                    </span>
                    <span className="font-medium text-theme-main">
                      {submissionResult.full_name}
                    </span>
                  </div>

                  <div>
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-0.5 font-medium">
                      {t('booking.phoneAndEmail')}
                    </span>
                    <span className="font-medium text-theme-main block">
                      {submissionResult.phone}
                    </span>
                    <span className="text-xs text-theme-muted block">
                      {submissionResult.email}
                    </span>
                  </div>
                </div>

                {submissionResult.special_request && (
                  <div className="pt-4 border-t border-theme">
                    <span className="text-xs uppercase tracking-wider text-theme-subtle block mb-1 font-medium">
                      {t('booking.specialRequestsNote')}
                    </span>
                    <p className="text-sm text-theme-muted bg-theme-elevated p-4 border border-theme rounded-xs font-light">
                      {submissionResult.special_request}
                    </p>
                  </div>
                )}
              </div>

              {/* Crucial Hotel Confirmation Notice */}
              <div className="p-6 bg-theme-elevated border border-theme rounded-xs text-xs text-theme-muted leading-relaxed font-light">
                <strong className="text-theme-gold font-semibold block mb-1">
                  {t('booking.confirmationNoticeTitle')}
                </strong>
                {t('booking.confirmationNoticeText')}
              </div>

              {/* Actions */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4">
                <button
                  type="button"
                  onClick={handleReset}
                  className="w-full sm:w-auto px-6 py-3 text-xs font-semibold uppercase tracking-widest border border-theme-gold text-theme-gold hover:bg-theme-surface rounded-xs transition-colors cursor-pointer"
                >
                  {t('booking.submitAnother')}
                </button>
                <Link
                  to="/"
                  className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 text-xs font-semibold uppercase tracking-widest bg-theme-gold text-stone-950 rounded-xs hover:brightness-110 transition-colors shadow-sm"
                >
                  {t('booking.returnHome')} &rarr;
                </Link>
              </div>
            </div>
          </RevealOnScroll>
        ) : (
          /* MAIN FORM VIEW */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
            {/* Form Column (7 cols) */}
            <div className="lg:col-span-7 bg-theme-surface border border-[var(--color-gold-border)] rounded-3xl p-6 sm:p-8 lg:p-10 shadow-2xl transition-colors duration-200">
              <form onSubmit={handleSubmit} noValidate className="space-y-6">
                {/* Form-level error alert */}
                {generalError && (
                  <div
                    role="alert"
                    aria-live="polite"
                    className="p-4 bg-rose-950/20 border border-rose-500/50 text-rose-500 rounded-xs text-xs leading-relaxed"
                  >
                    {generalError}
                  </div>
                )}

                {/* 1. ROOM SELECTION */}
                <div>
                  <label
                    htmlFor="booking-room"
                    className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                  >
                    {t('booking.roomPreference')} <span className="text-theme-gold">*</span>
                  </label>
                  <select
                    id="booking-room"
                    value={roomId}
                    onChange={handleRoomChange}
                    aria-describedby={fieldErrors.room ? 'booking-room-error' : undefined}
                    className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main focus:outline-none transition-colors ${
                      fieldErrors.room
                        ? 'border-rose-500 focus:border-rose-400'
                        : 'border-theme focus:border-[var(--color-gold)]'
                    }`}
                  >
                    <option value="" className="bg-theme-surface text-theme-muted">-- {t('booking.chooseRoom')} --</option>
                    {rooms.map((r) => (
                      <option key={r.id} value={r.id} className="bg-theme-surface text-theme-main">
                        {r.name} — {formatUZSPrice(r.price_per_night)} / {t('rooms.perNight')}
                      </option>
                    ))}
                  </select>
                  {fieldErrors.room && (
                    <p id="booking-room-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                      {fieldErrors.room}
                    </p>
                  )}
                </div>

                {/* 2. DATES (Check-in & Check-out) */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label
                      htmlFor="booking-check-in"
                      className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                    >
                      {t('booking.checkInDate')} <span className="text-theme-gold">*</span>
                    </label>
                    <input
                      type="date"
                      id="booking-check-in"
                      min={today}
                      value={checkIn}
                      onChange={handleCheckInChange}
                      aria-describedby={fieldErrors.check_in ? 'booking-checkin-error' : undefined}
                      className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main focus:outline-none transition-colors ${
                        fieldErrors.check_in
                          ? 'border-rose-500 focus:border-rose-400'
                          : 'border-theme focus:border-[var(--color-gold)]'
                      }`}
                    />
                    {fieldErrors.check_in && (
                      <p id="booking-checkin-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                        {fieldErrors.check_in}
                      </p>
                    )}
                  </div>

                  <div>
                    <label
                      htmlFor="booking-check-out"
                      className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                    >
                      {t('booking.checkOutDate')} <span className="text-theme-gold">*</span>
                    </label>
                    <input
                      type="date"
                      id="booking-check-out"
                      min={checkIn ? getTomorrowString(checkIn) : today}
                      value={checkOut}
                      onChange={handleCheckOutChange}
                      aria-describedby={fieldErrors.check_out ? 'booking-checkout-error' : undefined}
                      className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main focus:outline-none transition-colors ${
                        fieldErrors.check_out
                          ? 'border-rose-500 focus:border-rose-400'
                          : 'border-theme focus:border-[var(--color-gold)]'
                      }`}
                    />
                    {fieldErrors.check_out && (
                      <p id="booking-checkout-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                        {fieldErrors.check_out}
                      </p>
                    )}
                  </div>
                </div>

                {/* 3. GUEST COUNTS (Adults & Children) */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label
                      htmlFor="booking-adults"
                      className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                    >
                      {t('booking.adultsLabel')} <span className="text-theme-gold">*</span>
                    </label>
                    <input
                      type="number"
                      id="booking-adults"
                      min="1"
                      max={selectedRoom?.max_adults || 10}
                      value={adults}
                      onChange={(e) => {
                        setAdults(parseInt(e.target.value, 10) || 1);
                        setFieldErrors((prev) => ({ ...prev, adults: '' }));
                      }}
                      aria-describedby={fieldErrors.adults ? 'booking-adults-error' : undefined}
                      className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main focus:outline-none transition-colors ${
                        fieldErrors.adults
                          ? 'border-rose-500 focus:border-rose-400'
                          : 'border-theme focus:border-[var(--color-gold)]'
                      }`}
                    />
                    {fieldErrors.adults && (
                      <p id="booking-adults-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                        {fieldErrors.adults}
                      </p>
                    )}
                    {selectedRoom && (
                      <span className="text-[11px] text-theme-subtle mt-0.5 block font-light">
                        {t('booking.maxCapacity')}: {selectedRoom.max_adults} {t('booking.adultsPlural')}
                      </span>
                    )}
                  </div>

                  <div>
                    <label
                      htmlFor="booking-children"
                      className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                    >
                      {t('booking.childrenLabel')}
                    </label>
                    <input
                      type="number"
                      id="booking-children"
                      min="0"
                      max={selectedRoom?.max_children ?? 10}
                      value={childrenCount}
                      onChange={(e) => {
                        setChildrenCount(parseInt(e.target.value, 10) || 0);
                        setFieldErrors((prev) => ({ ...prev, children: '' }));
                      }}
                      aria-describedby={fieldErrors.children ? 'booking-children-error' : undefined}
                      className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main focus:outline-none transition-colors ${
                        fieldErrors.children
                          ? 'border-rose-500 focus:border-rose-400'
                          : 'border-theme focus:border-[var(--color-gold)]'
                      }`}
                    />
                    {fieldErrors.children && (
                      <p id="booking-children-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                        {fieldErrors.children}
                      </p>
                    )}
                    {selectedRoom && (
                      <span className="text-[11px] text-theme-subtle mt-0.5 block font-light">
                        {t('booking.maxCapacity')}: {selectedRoom.max_children} {t('booking.childrenPlural')}
                      </span>
                    )}
                  </div>
                </div>

                <div className="hidden" aria-hidden="true"><label>Website<input name="website" tabIndex={-1} autoComplete="off" value={website} onChange={e => setWebsite(e.target.value)} /></label></div>
                {/* 4. GUEST CONTACT DETAILS */}
                <div className="pt-4 border-t border-theme space-y-4">
                  <h3 className="text-xs font-semibold uppercase tracking-[0.2em] text-theme-gold">
                    {t('booking.guestContact')}
                  </h3>

                  <div>
                    <label
                      htmlFor="booking-fullname"
                      className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                    >
                      {t('booking.fullName')} <span className="text-theme-gold">*</span>
                    </label>
                    <input
                      type="text"
                      id="booking-fullname"
                      autoComplete="name"
                      value={fullName}
                      onChange={(e) => {
                        setFullName(e.target.value);
                        setFieldErrors((prev) => ({ ...prev, full_name: '' }));
                      }}
                      placeholder="e.g. Elena Rostova"
                      aria-describedby={fieldErrors.full_name ? 'booking-fullname-error' : undefined}
                      className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main placeholder:text-theme-subtle focus:outline-none transition-colors ${
                        fieldErrors.full_name
                          ? 'border-rose-500 focus:border-rose-400'
                          : 'border-theme focus:border-[var(--color-gold)]'
                      }`}
                    />
                    {fieldErrors.full_name && (
                      <p id="booking-fullname-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                        {fieldErrors.full_name}
                      </p>
                    )}
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label
                        htmlFor="booking-phone"
                        className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                      >
                        {t('booking.phone')} <span className="text-theme-gold">*</span>
                      </label>
                      <input
                        type="tel"
                        id="booking-phone"
                        autoComplete="tel"
                        value={phone}
                        onChange={(e) => {
                          setPhone(e.target.value);
                          setFieldErrors((prev) => ({ ...prev, phone: '' }));
                        }}
                        placeholder="+998 90 123 4567"
                        aria-describedby={fieldErrors.phone ? 'booking-phone-error' : undefined}
                        className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main placeholder:text-theme-subtle focus:outline-none transition-colors ${
                          fieldErrors.phone
                            ? 'border-rose-500 focus:border-rose-400'
                            : 'border-theme focus:border-[var(--color-gold)]'
                        }`}
                      />
                      {fieldErrors.phone && (
                        <p id="booking-phone-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                          {fieldErrors.phone}
                        </p>
                      )}
                    </div>

                    <div>
                      <label
                        htmlFor="booking-email"
                        className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                      >
                        {t('booking.email')} <span className="text-theme-gold">*</span>
                      </label>
                      <input
                        type="email"
                        id="booking-email"
                        autoComplete="email"
                        value={email}
                        onChange={(e) => {
                          setEmail(e.target.value);
                          setFieldErrors((prev) => ({ ...prev, email: '' }));
                        }}
                        placeholder="elena@example.com"
                        aria-describedby={fieldErrors.email ? 'booking-email-error' : undefined}
                        className={`w-full px-3.5 py-2.5 bg-theme-input border rounded-xs text-sm text-theme-main placeholder:text-theme-subtle focus:outline-none transition-colors ${
                          fieldErrors.email
                            ? 'border-rose-500 focus:border-rose-400'
                            : 'border-theme focus:border-[var(--color-gold)]'
                        }`}
                      />
                      {fieldErrors.email && (
                        <p id="booking-email-error" role="alert" className="mt-1 text-xs text-rose-500 font-medium">
                          {fieldErrors.email}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* 5. SPECIAL REQUEST (Optional) */}
                <div className="pt-2">
                  <label
                    htmlFor="booking-special-request"
                    className="block text-[11px] font-semibold uppercase tracking-[0.15em] text-theme-gold mb-2"
                  >
                    {t('booking.specialRequests')}
                  </label>
                  <textarea
                    id="booking-special-request"
                    rows="3"
                    maxLength={5000}
                    value={specialRequest}
                    onChange={(e) => setSpecialRequest(e.target.value)}
                    placeholder={t('booking.specialRequestsPlaceholder')}
                    className="w-full px-3.5 py-2.5 bg-theme-input border border-theme rounded-xs text-sm text-theme-main placeholder:text-theme-subtle focus:outline-none focus:border-[var(--color-gold)] transition-colors"
                  />
                  <span className="text-[11px] text-theme-subtle mt-1 block font-light">
                    {t('booking.specialRequestsNote')}
                  </span>
                </div>

                {/* SUBMIT BUTTON */}
                <div className="pt-4">
                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-full inline-flex items-center justify-center px-8 py-4 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-110 active:scale-[0.98] transition-all shadow-lg focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
                  >
                    {submitting ? (
                      <span className="flex items-center gap-2">
                        <span className="w-3.5 h-3.5 border-2 border-stone-950/30 border-t-stone-950 rounded-full animate-spin" />
                        {t('booking.submitting')}
                      </span>
                    ) : (
                      t('booking.submit')
                    )}
                  </button>
                  <p className="text-[11px] text-theme-subtle text-center mt-2.5 font-light">
                    {t('booking.noChargeNote')}
                  </p>
                </div>
              </form>
            </div>

            {/* Sidebar Summary Column (5 cols) */}
            <div className="lg:col-span-5">
              <BookingSummary
                selectedRoom={selectedRoom}
                checkIn={checkIn}
                checkOut={checkOut}
                adults={adults}
                childrenCount={childrenCount}
                hotelInfo={hotelInfo}
              />
            </div>
          </div>
        )}
      </Container>
    </div>
  );
}
