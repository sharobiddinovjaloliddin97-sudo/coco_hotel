import { useState } from 'react';
import { useLanguage } from '../../hooks/useLanguage';

export default function HotelImage({ src, alt = '', className = '', ...props }) {
  const [failedSrc, setFailedSrc] = useState(null);
  const { t } = useLanguage();
  if (!src || failedSrc === src) {
    return <div role="img" aria-label={t('common.photoPending')} className={`photo-placeholder ${className}`}>
      <span aria-hidden="true" className="photo-monogram">C</span>
      <span className="photo-placeholder-label">{t('common.photoPending')}</span>
    </div>;
  }
  return <img {...props} src={src} alt={alt} className={className} onError={() => setFailedSrc(src)} />;
}
