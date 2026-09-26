import { useState, useEffect } from 'react';
import { getHotelInformation } from '../api/hotel';
import { HotelContext } from './hotelContextDef';
import { useLanguage } from '../hooks/useLanguage';

export default function HotelProvider({ children }) {
  const { language } = useLanguage();
  const [result, setResult] = useState({ language: null, data: null, error: null });
  useEffect(() => {
    let active = true;
    getHotelInformation()
      .then(data => { if (active) setResult({ language, data, error: null }); })
      .catch(error => { if (active) setResult({ language, data: null, error }); });
    return () => { active = false; };
  }, [language]);
  const loading = result.language !== language;
  return <HotelContext.Provider value={{ hotelInfo: loading ? null : result.data, loading, error: loading ? null : result.error }}>{children}</HotelContext.Provider>;
}
