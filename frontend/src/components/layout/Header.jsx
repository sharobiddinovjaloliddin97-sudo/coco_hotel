import { useState, useEffect } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { useLanguage } from '../../hooks/useLanguage';
import { useTheme } from '../../hooks/useTheme';
import CocoLogo from '../common/CocoLogo';

export default function Header() {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentPath, setCurrentPath] = useState(location.pathname);
  const { language, changeLanguage, t } = useLanguage();
  const { theme, toggleTheme } = useTheme();

  const navLinks = [
    { key: 'home', name: t('nav.home'), path: '/' },
    { key: 'rooms', name: t('nav.rooms'), path: '/rooms' },
    { key: 'about', name: t('nav.about'), path: '/about' },
    { key: 'services', name: t('nav.services'), path: '/services' },
    { key: 'gallery', name: t('nav.gallery'), path: '/gallery' },
    { key: 'promotions', name: t('nav.promotions') || t('nav.offers'), path: '/promotions' },
    { key: 'contact', name: t('nav.contact'), path: '/contact' },
  ];

  const languages = [
    { code: 'uz', label: 'UZ' },
    { code: 'ru', label: 'RU' },
    { code: 'en', label: 'EN' },
  ];

  // Reset mobile menu when location changes
  if (location.pathname !== currentPath) {
    setCurrentPath(location.pathname);
    setMobileMenuOpen(false);
  }

  // Handle escape key to close menu
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && mobileMenuOpen) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [mobileMenuOpen]);

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [mobileMenuOpen]);

  const toggleMenu = () => {
    setMobileMenuOpen((prev) => !prev);
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 dark:bg-[#0f1115]/95 backdrop-blur-md border-b border-stone-200/90 dark:border-white/10 transition-colors duration-200">
      <div className="max-w-[1440px] w-full mx-auto px-4 sm:px-6 lg:px-8 xl:px-10">
        <div className="flex items-center justify-between h-20 sm:h-22">
          {/* 1. Brand / Logo */}
          <Link
            to="/"
            className="flex items-center shrink-0 rounded-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-gold)]"
            aria-label="Coco Hotel Home"
          >
            <CocoLogo size="default" />
          </Link>

          {/* 2. Desktop Navigation: Evenly spaced, crisp, single-line typography */}
          <nav
            aria-label="Main Navigation"
            className="hidden lg:flex items-center gap-4 xl:gap-7 2xl:gap-8 mx-4"
          >
            {navLinks.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                end={link.path === '/'}
                className={({ isActive }) =>
                  `whitespace-nowrap inline-flex items-center h-10 px-1 py-2 text-[12.5px] xl:text-[13px] uppercase tracking-wider font-semibold transition-all duration-200 relative outline-none focus:outline-none focus-visible:ring-1 focus-visible:ring-amber-400 ${
                    isActive
                      ? 'text-amber-600 dark:text-amber-400 font-bold after:absolute after:bottom-0 after:left-0 after:right-0 after:h-[2.5px] after:rounded-full after:bg-gradient-to-r after:from-amber-400 after:via-amber-500 after:to-amber-600'
                      : 'text-stone-700 hover:text-stone-950 dark:text-stone-300 dark:hover:text-white after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 after:w-0 hover:after:w-full after:h-[2px] after:rounded-full after:bg-amber-400/80 after:transition-all after:duration-250'
                  }`
                }
              >
                {link.name}
              </NavLink>
            ))}
          </nav>

          {/* 3. Right Controls: Language, Theme, Book Now, Mobile Hamburger */}
          <div className="flex items-center gap-2 sm:gap-3 xl:gap-4 shrink-0">
            {/* Language Selector */}
            <div
              className="inline-flex items-center p-1 rounded-full border border-stone-200 dark:border-stone-800 bg-stone-100/90 dark:bg-stone-900/90 shadow-xs"
              role="group"
              aria-label="Language selection"
            >
              {languages.map((item) => (
                <button
                  key={item.code}
                  type="button"
                  onClick={() => changeLanguage(item.code)}
                  aria-pressed={language === item.code}
                  className={`px-2.5 py-1 text-[11px] font-bold tracking-wider rounded-full transition-all cursor-pointer ${
                    language === item.code
                      ? 'bg-gold-metallic text-stone-950 shadow-xs font-bold'
                      : 'text-stone-600 hover:text-stone-950 dark:text-stone-400 dark:hover:text-white'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>

            {/* Theme Toggle Button */}
            <button
              type="button"
              onClick={toggleTheme}
              aria-label={theme === 'dark' ? t('theme.switchToLight') : t('theme.switchToDark')}
              className="w-9 h-9 inline-flex items-center justify-center rounded-full border border-stone-200 dark:border-stone-800 bg-stone-100/90 dark:bg-stone-900/90 text-stone-700 dark:text-amber-400 hover:border-amber-400 hover:text-amber-500 transition-colors cursor-pointer shadow-xs focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
              title={theme === 'dark' ? t('theme.switchToLight') : t('theme.switchToDark')}
            >
              {theme === 'dark' ? (
                // Sun icon for switching to light
                <svg className="w-4 h-4 text-amber-400" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
                </svg>
              ) : (
                // Moon icon for switching to dark
                <svg className="w-4 h-4 text-stone-700" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
                </svg>
              )}
            </button>

            {/* Book Now Button */}
            <Link
              to="/booking"
              className="hidden md:inline-flex items-center justify-center px-4 py-2 xl:px-6 xl:py-2.5 text-[11px] xl:text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-105 active:scale-[0.98] transition-all shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
            >
              {t('nav.bookNow')}
            </Link>

            {/* Mobile menu button */}
            <button
              type="button"
              id="mobile-menu-button"
              aria-controls="mobile-navigation"
              aria-expanded={mobileMenuOpen}
              aria-label={mobileMenuOpen ? t('nav.closeMenu') : t('nav.menu')}
              onClick={toggleMenu}
              className="lg:hidden inline-flex items-center justify-center w-10 h-10 rounded-full text-stone-700 dark:text-stone-200 hover:text-amber-500 hover:bg-stone-100 dark:hover:bg-stone-900 border border-stone-200 dark:border-stone-800 transition-colors cursor-pointer focus:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="2"
                stroke="currentColor"
                aria-hidden="true"
              >
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* 4. Luxury Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div
          id="mobile-navigation"
          aria-label="Mobile Navigation"
          className="lg:hidden fixed inset-x-0 top-20 bottom-0 z-40 bg-white/98 dark:bg-[#0f1115]/98 backdrop-blur-2xl border-t border-stone-200 dark:border-white/10 flex flex-col justify-between px-6 py-6 overflow-y-auto"
        >
          {/* Navigation Links List */}
          <nav className="space-y-1.5">
            {navLinks.map((link) => (
              <NavLink
                key={link.path}
                to={link.path}
                end={link.path === '/'}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `flex items-center justify-between px-4 py-3.5 rounded-xl text-sm uppercase tracking-widest font-semibold transition-all ${
                    isActive
                      ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 font-bold border-l-4 border-amber-500 shadow-xs'
                      : 'text-stone-700 dark:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-900 hover:text-amber-500'
                  }`
                }
              >
                <span>{link.name}</span>
                <span className="text-amber-500/60 font-serif text-lg">›</span>
              </NavLink>
            ))}
          </nav>

          {/* Bottom Actions: Call 24/7, Location Map & Book Now */}
          <div className="pt-6 mt-6 border-t border-stone-200 dark:border-stone-800 space-y-3">
            {/* Quick 24/7 Call Link */}
            <a
              href="tel:+998880000051"
              className="flex items-center justify-center gap-2.5 py-3 px-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900/60 text-xs font-semibold text-stone-700 dark:text-stone-300 hover:text-amber-500 transition-colors"
            >
              <span>📞</span>
              <span>24/7 Qabulxona: +998 88 000-00-51</span>
            </a>

            {/* Quick Location Map Link */}
            <a
              href="https://yandex.uz/maps/-/CPwOM2O3"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2.5 py-3 px-4 rounded-xl border border-amber-400/40 bg-amber-500/10 text-xs font-bold text-amber-600 dark:text-amber-400 hover:bg-amber-500/20 transition-colors"
            >
              <span>📍</span>
              <span>{language === 'ru' ? 'Локация (Яндекс.Карты): Богибустон 156' : language === 'uz' ? 'Lokatsiya (Yandex Xarita): Bog‘ibuston 156' : 'Location (Yandex Maps): 156 Bogibuston'} ↗</span>
            </a>

            {/* Big Action Book Button */}
            <Link
              to="/booking"
              onClick={() => setMobileMenuOpen(false)}
              className="block w-full text-center py-3.5 text-xs font-bold uppercase tracking-widest bg-gold-metallic gold-glow text-stone-950 rounded-full hover:brightness-105 active:scale-[0.98] transition-all shadow-lg"
            >
              {t('nav.bookNow')}
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
