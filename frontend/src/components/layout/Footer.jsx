import { Link } from 'react-router-dom';
import { useHotel } from '../../hooks/useHotel';
import { useLanguage } from '../../hooks/useLanguage';
import CocoLogo from '../common/CocoLogo';

export default function Footer() {
  const currentYear = new Date().getFullYear();
  const { hotelInfo } = useHotel();
  const { t } = useLanguage();

  const hotelName = hotelInfo?.name || 'Coco Hotel';
  const phone = hotelInfo?.phone;
  const secondaryPhone = hotelInfo?.secondary_phone;
  const email = hotelInfo?.email;
  const address = hotelInfo?.address;

  return (
    <footer className="relative bg-theme-secondary text-theme-muted mt-auto border-t border-theme overflow-hidden transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14 lg:py-18 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 lg:gap-14">
          {/* Brand */}
          <div className="space-y-4">
            <Link
              to="/"
              className="inline-block focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs"
              aria-label="Coco Hotel Home"
            >
              <CocoLogo size="default" />
            </Link>
            <p className="text-sm text-theme-muted max-w-sm leading-relaxed font-light">
              {t('footer.tagline')}
            </p>
          </div>

          {/* Navigation */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-[0.2em] text-theme-gold mb-4">
              {t('footer.explore')}
            </h3>
            <ul className="space-y-2.5 text-sm text-theme-muted">
              <li>
                <Link to="/rooms" className="hover:text-theme-gold transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs">
                  {t('footer.roomsSuites')}
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-theme-gold transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs">
                  {t('footer.aboutHotel')}
                </Link>
              </li>
              <li>
                <Link to="/services" className="hover:text-theme-gold transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs">
                  {t('footer.servicesAmenities')}
                </Link>
              </li>
              <li>
                <Link to="/gallery" className="hover:text-theme-gold transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs">
                  {t('footer.gallery')}
                </Link>
              </li>
              <li>
                <Link to="/promotions" className="hover:text-theme-gold transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs">
                  {t('footer.offers')}
                </Link>
              </li>
              <li>
                <Link to="/booking" className="hover:text-theme-gold transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs">
                  {t('footer.reserve')}
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Area */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-[0.2em] text-theme-gold mb-4">
              {t('footer.contactConcierge')}
            </h3>
            <div className="space-y-3.5 text-sm text-theme-muted">
              {address && (
                <a
                  href={hotelInfo?.map_url || "https://yandex.uz/maps/-/CPwOM2O3"}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-start gap-2.5 hover:text-amber-500 transition-colors group"
                  title="Yandex Maps lokatsiyasini ochish"
                >
                  <svg className="w-4 h-4 text-theme-gold mt-0.5 shrink-0 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span className="group-hover:underline underline-offset-2">{address} ↗</span>
                </a>
              )}

              {phone && (
                <p className="flex items-center gap-2.5">
                  <svg className="w-4 h-4 text-theme-gold shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <a href={`tel:${phone}`} className="hover:text-theme-main transition-colors">
                    {phone}
                  </a>
                </p>
              )}

              {secondaryPhone && (
                <p className="flex items-center gap-2 pl-6 text-xs text-theme-subtle">
                  <a href={`tel:${secondaryPhone}`} className="hover:text-theme-muted transition-colors">
                    Alt: {secondaryPhone}
                  </a>
                </p>
              )}

              {email && (
                <p className="flex items-center gap-2.5">
                  <svg className="w-4 h-4 text-theme-gold shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <a href={`mailto:${email}`} className="hover:text-theme-main transition-colors">
                    {email}
                  </a>
                </p>
              )}

              <div className="pt-2">
                <Link
                  to="/contact"
                  className="inline-flex items-center text-xs font-semibold uppercase tracking-widest text-theme-gold hover:underline transition-colors focus-visible:outline-2 focus-visible:outline-[var(--color-gold)] rounded-xs"
                >
                  {t('footer.sendMessage')} &rarr;
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom copyright */}
        <div className="mt-12 pt-8 border-t border-theme flex flex-col sm:flex-row items-center justify-between text-xs text-theme-subtle">
          <p>&copy; {currentYear} {hotelName}. {t('footer.rights')}</p>
          <p className="mt-2 sm:mt-0 font-light tracking-wider">{t('footer.tranquilStay')}</p>
        </div>
      </div>
    </footer>
  );
}
