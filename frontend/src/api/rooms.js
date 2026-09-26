import apiClient from './client';

/**
 * Fetch active featured rooms for homepage highlight.
 */
export async function getFeaturedRooms() {
  const response = await apiClient.get('/rooms/', {
    params: { featured: 'true' },
  });
  return response.data;
}

/**
 * Fetch full active rooms catalogue with optional filters.
 */
export async function getRooms(params = {}) {
  const response = await apiClient.get('/rooms/', { params });
  return response.data;
}

/**
 * Fetch single room details by slug.
 */
export async function getRoomBySlug(slug) {
  const response = await apiClient.get(`/rooms/${slug}/`);
  return response.data;
}
