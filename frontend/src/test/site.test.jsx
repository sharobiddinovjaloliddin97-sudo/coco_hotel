import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import LanguageProvider from '../context/LanguageProvider';
import ThemeProvider from '../context/ThemeProvider';
import AppRouter from '../router/AppRouter';
import { translations, getNestedTranslation } from '../i18n';
import { createBookingRequest } from '../api/bookings';
import { getGallery } from '../api/hotel';
import { getRooms } from '../api/rooms';
const fixtures = vi.hoisted(() => ({
  room: { id: 1, name: 'Garden Room', slug: 'garden-room', price_per_night: '500000', max_adults: 2, max_children: 0, amenities: [], images: [], short_description: 'A room', description: 'A quiet room' },
  hotel: { name: 'Coco Hotel', hero_title: 'Your next stay', about_title: 'Our hotel', about_text: 'Our story', phone: '+998901234567', email: 'hotel@example.com', address: 'Tashkent' },
  promotion: { id: 1, title: 'Summer Stay', slug: 'summer-stay', short_description: 'Offer', description: 'Offer details' },
}));
vi.mock('../api/hotel', () => ({
  getHotelInformation: vi.fn(async () => fixtures.hotel),
  getGallery: vi.fn(async () => []),
  getServices: vi.fn(async () => [{ id: 1, name: 'Wi-Fi', icon: 'wifi' }]),
  getPromotions: vi.fn(async () => [fixtures.promotion]),
  getPromotionBySlug: vi.fn(async () => fixtures.promotion),
}));
vi.mock('../api/rooms', () => ({ getRooms: vi.fn(async () => [fixtures.room]), getFeaturedRooms: vi.fn(async () => [fixtures.room]), getRoomBySlug: vi.fn(async () => fixtures.room) }));
vi.mock('../api/bookings', () => ({ createBookingRequest: vi.fn(async payload => ({ status: 201, data: { ...payload, id: 42, status: 'NEW' } })) }));
function open(path, language = 'en') {
  localStorage.setItem('coco-language', language);
  return render(<LanguageProvider><ThemeProvider><MemoryRouter initialEntries={[path]}><AppRouter /></MemoryRouter></ThemeProvider></LanguageProvider>);
}
const paths = ['/', '/rooms', '/rooms/garden-room', '/about', '/services', '/gallery', '/promotions', '/promotions/summer-stay', '/contact', '/booking', '/missing'];
describe('Public pages', () => {
  for (const language of ['en', 'uz', 'ru']) for (const path of paths) {
    it(`${path} renders in ${language}`, async () => {
      open(path, language);
      await waitFor(() => expect(screen.getAllByRole('heading', { level: 1 }).length).toBe(1));
      await waitFor(() => expect(document.querySelector('main')?.textContent).not.toMatch(/\b(?:meta|booking|home|rooms|gallery|contact|common|services|promotions|about|footer)\.[a-zA-Z]+/));
    });
  }
  it('does not disguise a gallery network failure as stock photography', async () => {
    getGallery.mockRejectedValueOnce(new Error('offline'));
    open('/gallery');
    await screen.findByText(translations.en.common.errorTitle);
    expect(document.querySelector('img[src*="/images/"]')).toBeNull();
  });
  it('submits a real booking payload and shows the server reference', async () => {
    open('/booking');
    await screen.findByText(/Garden Room/, { selector: 'option' });
    fireEvent.change(document.getElementById('booking-fullname'), { target: { value: 'Guest Name' } });
    fireEvent.change(document.getElementById('booking-phone'), { target: { value: '+998901234567' } });
    fireEvent.change(document.getElementById('booking-email'), { target: { value: 'guest@example.com' } });
    expect(document.getElementById('booking-children').getAttribute('max')).toBe('0');
    fireEvent.click(screen.getByRole('button', { name: translations.en.booking.submit }));
    await waitFor(() => expect(createBookingRequest).toHaveBeenCalledWith(expect.objectContaining({ room: 1, full_name: 'Guest Name', email: 'guest@example.com', children: 0, website: '' })));
    await screen.findByText(/42/);
  });
  it('does not send a booking when the selected room no longer exists', async () => {
    getRooms.mockResolvedValueOnce([]);
    open('/booking?room=999');
    await screen.findByText(translations.en.booking.roomsUpdatingTitle);
    expect(createBookingRequest).not.toHaveBeenCalled();
  });
});

describe('Translation completeness', () => {
  const sources = import.meta.glob('../**/*.{js,jsx}', { query: '?raw', import: 'default', eager: true });
  const keys = new Set(Object.entries(sources).filter(([path]) => !path.includes('/test/')).flatMap(([,source]) => [...source.matchAll(/\bt\(['"]([^'"]+)['"]/g)].map(match => match[1])));
  for (const language of ['en', 'uz', 'ru']) it(`all literal keys exist in ${language}`, () => {
    const missing = [...keys].filter(key => !getNestedTranslation(translations[language], key));
    expect(missing).toEqual([]);
  });
});

describe('Gallery keyboard access', () => {
  it('opens the lightbox by keyboard and closes with Escape', async () => {
    getGallery.mockResolvedValueOnce([{ id: 5, image: 'https://example.com/room.jpg', title: 'Published hotel photo', category: 'rooms' }]);
    open('/gallery');
    const image = await screen.findByText('Published hotel photo');
    const trigger = image.closest('[role="button"]');
    trigger.focus();
    fireEvent.keyDown(trigger, { key: 'Enter' });
    await screen.findByRole('dialog');
    expect(document.activeElement.getAttribute('data-gallery-close')).not.toBeNull();
    fireEvent.keyDown(document, { key: 'Escape' });
    expect(screen.queryByRole('dialog')).toBeNull();
    expect(document.activeElement).toBe(trigger);
  });
});
