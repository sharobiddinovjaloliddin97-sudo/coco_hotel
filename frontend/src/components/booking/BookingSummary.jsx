import HotelImage from '../../components/common/HotelImage';
import { formatUZSPrice, formatDate } from '../../utils/formatters';
import { useLanguage } from '../../hooks/useLanguage';
import { getRoomImageUrl } from '../../utils/roomImages';

export default function BookingSummary({
  selectedRoom,
  checkIn,
  checkOut,
  adults,
  childrenCount,
  hotelInfo,
}) {
  const { t } = useLanguage();
  const phone = hotelInfo?.phone;
  const email = hotelInfo?.email;

  // Calculate nights
  let nights = 1;
  if (checkIn && checkOut) {
    const d1 = new Date(checkIn);
    const d2 = new Date(checkOut);
    const diffTime = d2.getTime() - d1.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays > 0) nights = diffDays;
  }

  const roomImage = selectedRoom ? getRoomImageUrl(selectedRoom) : null;
  const pricePerNight = selectedRoom?.price_per_night ? Number(selectedRoom.price_per_night) : 0;
  const totalPrice = pricePerNight * nights;

  return (
    <aside aria-label="Stay Summary and Booking Policy" className="space-y-6">
      {/* Selected Room & Dates Card */}
      <div className="bg-theme-surface border border-[var(--color-gold-border)] rounded-2xl p-6 sm:p-7 shadow-2xl transition-colors duration-200">
        <h2 className="text-xs font-bold uppercase tracking-[0.2em] text-theme-gold mb-4">
          {t('booking.staySummary')}
        </h2>

        {selectedRoom ? (
          <div className="space-y-4">
            {/* Room Thumbnail & Title */}
            <div className="flex gap-4 items-center pb-4 border-b border-theme">
              {roomImage && (
                <div className="w-20 h-16 rounded-xl overflow-hidden bg-theme-elevated shrink-0 border border-theme">
                  <HotelImage
                    src={roomImage}
                    alt={selectedRoom.name}
                    className="w-full h-full object-cover"
                  />
                </div>
              )}
              <div>
                <h3 className="text-base font-serif font-bold text-theme-main">
                  {selectedRoom.name}
                </h3>
                <p className="text-xs text-theme-muted mt-0.5">
                  {formatUZSPrice(selectedRoom.price_per_night)} / {t('rooms.perNight')}
                </p>
              </div>
            </div>

            <div className="pt-2 grid grid-cols-2 gap-3 text-xs">
              <div>
                <span className="text-theme-subtle uppercase tracking-wider block font-semibold mb-0.5">{t('booking.checkIn')}</span>
                <span className="font-semibold text-theme-main">
                  {checkIn ? formatDate(checkIn) : t('booking.notSelected')}
                </span>
              </div>
              <div>
                <span className="text-theme-subtle uppercase tracking-wider block font-semibold mb-0.5">{t('booking.checkOut')}</span>
                <span className="font-semibold text-theme-main">
                  {checkOut ? formatDate(checkOut) : t('booking.notSelected')}
                </span>
              </div>
            </div>

            <div className="pt-2 border-t border-theme flex items-center justify-between text-xs text-theme-muted">
              <span>{t('rooms.guests')}:</span>
              <span className="font-semibold text-theme-main">
                {adults} {adults === 1 ? t('booking.adult') : t('booking.adultsPlural')}
                {childrenCount > 0 && `, ${childrenCount} ${childrenCount === 1 ? t('booking.child') : t('booking.childrenPlural')}`}
              </span>
            </div>

            {/* Price calculation */}
            <div className="pt-3 border-t border-theme space-y-1.5 text-xs">
              <div className="flex justify-between text-theme-muted">
                <span>{nights} {nights === 1 ? 'night' : 'nights'}</span>
                <span>{formatUZSPrice(pricePerNight)} × {nights}</span>
              </div>
              <div className="pt-2 border-t border-theme flex items-baseline justify-between">
                <span className="font-bold text-sm uppercase tracking-wider text-theme-main">Total</span>
                <span className="text-2xl font-serif font-bold text-theme-gold">
                  {formatUZSPrice(totalPrice)}
                </span>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-sm text-theme-muted italic font-light">
            {t('booking.chooseRoomHint')}
          </p>
        )}
      </div>

      {/* Booking Policy Information */}
      <div className="bg-theme-elevated border border-theme rounded-xs p-6 text-theme-muted transition-colors duration-200">
        <div className="flex items-start gap-3">
          <svg
            className="w-5 h-5 text-theme-gold mt-0.5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth="1.5"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
            />
          </svg>
          <div className="space-y-2 text-xs leading-relaxed font-light text-theme-muted">
            <h3 className="font-semibold text-theme-gold uppercase tracking-wider text-[11px]">
              {t('booking.policyTitle')}
            </h3>
            <p>
              {t('booking.policyP1')}
            </p>
            <p>
              {t('booking.policyP2')}
            </p>
          </div>
        </div>
      </div>

      {/* Direct Contact Option */}
      {(phone || email) && (
        <div className="bg-theme-surface border border-theme rounded-xs p-6 text-theme-muted space-y-3 text-xs transition-colors duration-200">
          <h3 className="font-semibold text-theme-main uppercase tracking-wider text-[11px]">
            {t('booking.immediateAssistance')}
          </h3>
          <p className="text-theme-muted leading-relaxed font-light">
            {t('booking.conciergeService')}
          </p>
          <div className="pt-1 space-y-1.5 font-medium">
            {phone && (
              <p>
                {t('booking.telephone')}:{' '}
                <a href={`tel:${phone}`} className="text-theme-gold hover:underline">
                  {phone}
                </a>
              </p>
            )}
            {email && (
              <p>
                {t('booking.email')}:{' '}
                <a href={`mailto:${email}`} className="text-theme-gold hover:underline">
                  {email}
                </a>
              </p>
            )}
          </div>
        </div>
      )}
    </aside>
  );
}
