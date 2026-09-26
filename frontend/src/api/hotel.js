import apiClient from './client';

/**
 * Fetch singleton hotel information (branding, contacts, hero, about).
 */
export async function getHotelInformation() {
  const response = await apiClient.get('/hotel/');
  return response.data;
}

/**
 * Fetch active hotel services/amenities list.
 */
export async function getServices() {
  const response = await apiClient.get('/services/');
  return response.data;
}

/**
 * Fetch active gallery images showcase list.
 */
export async function getGallery() {
  const response = await apiClient.get('/gallery/');
  return response.data;
}

/**
 * Fetch active promotions list.
 */
export async function getPromotions() {
  const response = await apiClient.get('/promotions/');
  return response.data;
}

/**
 * Fetch single promotion details by slug.
 */
export async function getPromotionBySlug(slug) {
  const response = await apiClient.get(`/promotions/${slug}/`);
  return response.data;
}
