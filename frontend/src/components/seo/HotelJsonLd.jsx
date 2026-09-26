import { useEffect } from 'react';
import { useHotel } from '../../hooks/useHotel';
import { SITE_URL } from '../../config/site';

/**
 * Injects safe, factual Hotel JSON-LD structured data into the document head
 * based strictly on real backend hotel information.
 */
export default function HotelJsonLd() {
  const { hotelInfo } = useHotel();

  useEffect(() => {
    if (!hotelInfo) return;

    const schema = {
      '@context': 'https://schema.org',
      '@type': 'Hotel',
      name: hotelInfo.name || 'Coco Hotel',
      url: SITE_URL,
    };

    if (hotelInfo.phone) {
      schema.telephone = hotelInfo.phone;
    }
    if (hotelInfo.email) {
      schema.email = hotelInfo.email;
    }
    if (hotelInfo.about_text) {
      schema.description = hotelInfo.about_text;
    }
    if (hotelInfo.address) {
      schema.address = {
        '@type': 'PostalAddress',
        streetAddress: hotelInfo.address,
      };
    }
    if (hotelInfo.latitude && hotelInfo.longitude) {
      schema.geo = {
        '@type': 'GeoCoordinates',
        latitude: hotelInfo.latitude,
        longitude: hotelInfo.longitude,
      };
    }
    if (hotelInfo.check_in_time) {
      schema.checkinTime = hotelInfo.check_in_time;
    }
    if (hotelInfo.check_out_time) {
      schema.checkoutTime = hotelInfo.check_out_time;
    }

    const scriptId = 'hotel-json-ld';
    let scriptElement = document.getElementById(scriptId);
    if (!scriptElement) {
      scriptElement = document.createElement('script');
      scriptElement.id = scriptId;
      scriptElement.type = 'application/ld+json';
      document.head.appendChild(scriptElement);
    }
    scriptElement.textContent = JSON.stringify(schema);

    return () => {
      const existing = document.getElementById(scriptId);
      if (existing) {
        existing.remove();
      }
    };
  }, [hotelInfo]);

  return null;
}
