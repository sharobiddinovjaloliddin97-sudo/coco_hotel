import { useLanguage } from '../hooks/useLanguage';
import { Suspense, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import HotelProvider from '../context/HotelProvider';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import LoadingState from '../components/common/LoadingState';
import HotelJsonLd from '../components/seo/HotelJsonLd';

function RouteLoadingFallback() {
  return (
    <div
      className="py-24 sm:py-32 flex justify-center items-center min-h-[50vh] bg-theme-main"
      role="status"
      aria-live="polite"
    >
      <LoadingState />
    </div>
  );
}

export default function MainLayout() {
  const { t } = useLanguage();
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo({ top: 0, behavior: 'instant' }); }, [pathname]);
  return (
    <HotelProvider>
      <HotelJsonLd />
      <div className="min-h-screen flex flex-col bg-theme-main text-theme-main antialiased transition-colors duration-200">
        <a href="#main-content" className="skip-link">{t('common.skip')}</a>
        <Header />
        <main id="main-content" className="flex-1">
          <Suspense fallback={<RouteLoadingFallback />}>
            <Outlet />
          </Suspense>
        </main>
        <Footer />
      </div>
    </HotelProvider>
  );
}
