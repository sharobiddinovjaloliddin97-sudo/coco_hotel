import { lazy } from 'react';
import { Routes, Route } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';

const HomePage = lazy(() => import('../pages/HomePage'));
const RoomsPage = lazy(() => import('../pages/RoomsPage'));
const RoomDetailPage = lazy(() => import('../pages/RoomDetailPage'));
const AboutPage = lazy(() => import('../pages/AboutPage'));
const ServicesPage = lazy(() => import('../pages/ServicesPage'));
const GalleryPage = lazy(() => import('../pages/GalleryPage'));
const PromotionsPage = lazy(() => import('../pages/PromotionsPage'));
const PromotionDetailPage = lazy(() => import('../pages/PromotionDetailPage'));
const ContactPage = lazy(() => import('../pages/ContactPage'));
const BookingPage = lazy(() => import('../pages/BookingPage'));
const NotFoundPage = lazy(() => import('../pages/NotFoundPage'));

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="rooms" element={<RoomsPage />} />
        <Route path="rooms/:slug" element={<RoomDetailPage />} />
        <Route path="about" element={<AboutPage />} />
        <Route path="services" element={<ServicesPage />} />
        <Route path="gallery" element={<GalleryPage />} />
        <Route path="promotions" element={<PromotionsPage />} />
        <Route path="promotions/:slug" element={<PromotionDetailPage />} />
        <Route path="contact" element={<ContactPage />} />
        <Route path="booking" element={<BookingPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
