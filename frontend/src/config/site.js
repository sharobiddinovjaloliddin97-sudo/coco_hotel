/**
 * Centralized site-level configuration and canonical URL generator.
 */
export const SITE_URL = (import.meta.env.VITE_SITE_URL || 'https://coco-hotel.uz').replace(/\/+$/, '');

/**
 * Returns a standardized canonical URL for a given path.
 * Strips any query parameters or hash fragments to ensure canonical purity.
 */
export function getCanonicalUrl(path = '') {
  if (!path || path === '/') {
    return `${SITE_URL}/`;
  }
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  const pathOnly = cleanPath.split('?')[0].split('#')[0];
  return `${SITE_URL}${pathOnly}`;
}
