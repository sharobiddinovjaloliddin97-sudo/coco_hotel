import { useEffect } from 'react';
import { getCanonicalUrl } from '../config/site';

function updateMetaTag(attributeName, attributeValue, content) {
  let element = document.querySelector(`meta[${attributeName}="${attributeValue}"]`);
  if (!element) {
    element = document.createElement('meta');
    element.setAttribute(attributeName, attributeValue);
    document.head.appendChild(element);
  }
  element.setAttribute('content', content || '');
}

function updateCanonical(url) {
  let link = document.querySelector('link[rel="canonical"]');
  if (!link) {
    link = document.createElement('link');
    link.setAttribute('rel', 'canonical');
    document.head.appendChild(link);
  }
  link.setAttribute('href', url);
}

/**
 * Lightweight hook to manage document title, meta descriptions,
 * canonical link, Open Graph tags, and Twitter Cards.
 */
export function usePageMeta({
  title,
  description,
  canonicalPath,
  canonicalUrl,
  type = 'website',
} = {}) {
  useEffect(() => {
    // 1. Document Title formatting
    const rawTitle = (title || '').trim();
    const formattedTitle =
      !rawTitle || rawTitle === 'Coco Hotel'
        ? 'Coco Hotel'
        : `${rawTitle} | Coco Hotel`;

    const previousTitle = document.title;
    document.title = formattedTitle;

    // 2. Description
    if (description) {
      updateMetaTag('name', 'description', description);
    }

    // 3. Canonical URL
    const canonical =
      canonicalUrl || getCanonicalUrl(canonicalPath || window.location.pathname);
    updateCanonical(canonical);

    // 4. Open Graph
    updateMetaTag('property', 'og:title', formattedTitle);
    if (description) {
      updateMetaTag('property', 'og:description', description);
    }
    updateMetaTag('property', 'og:type', type);
    updateMetaTag('property', 'og:url', canonical);

    // 5. Twitter Card
    updateMetaTag('name', 'twitter:card', 'summary');
    updateMetaTag('name', 'twitter:title', formattedTitle);
    if (description) {
      updateMetaTag('name', 'twitter:description', description);
    }

    return () => {
      document.title = previousTitle;
    };
  }, [title, description, canonicalPath, canonicalUrl, type]);
}

export default usePageMeta;
