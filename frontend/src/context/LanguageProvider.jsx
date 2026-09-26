import { useState, useEffect, useCallback, useMemo } from 'react';
import { LanguageContext } from './LanguageContext';
import { translations, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE, getNestedTranslation } from '../i18n';

const STORAGE_KEY = 'coco-language';

function getInitialLanguage() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved && SUPPORTED_LANGUAGES.includes(saved)) {
      return saved;
    }
  } catch {
    // localStorage not accessible
  }

  // Detect browser language
  if (typeof navigator !== 'undefined' && navigator.language) {
    const browser = navigator.language.toLowerCase();
    if (browser.startsWith('uz')) return 'uz';
    if (browser.startsWith('ru')) return 'ru';
    if (browser.startsWith('en')) return 'en';
  }

  return DEFAULT_LANGUAGE;
}

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(getInitialLanguage);

  useEffect(() => {
    // Sync document element lang attribute
    document.documentElement.lang = language;
    try {
      localStorage.setItem(STORAGE_KEY, language);
    } catch {
      // Ignore
    }
    // Dispatch custom event so non-React Axios client can pick up language changes instantly
    window.dispatchEvent(new CustomEvent('coco-language-changed', { detail: language }));
  }, [language]);

  const changeLanguage = useCallback((newLang) => {
    if (SUPPORTED_LANGUAGES.includes(newLang)) {
      document.documentElement.lang = newLang;
      setLanguage(newLang);
    }
  }, []);

  const t = useCallback(
    (key, params = {}) => {
      // 1. Try selected language
      let text = getNestedTranslation(translations[language], key);

      // 2. Fallback to English
      if (!text && language !== 'en') {
        text = getNestedTranslation(translations.en, key);
      }

      // 3. Fallback to key itself
      if (!text) {
        return key;
      }

      // Replace variables like {count}
      if (params && typeof params === 'object') {
        Object.entries(params).forEach(([paramKey, val]) => {
          text = text.replace(new RegExp(`\\{${paramKey}\\}`, 'g'), String(val));
        });
      }

      return text;
    },
    [language]
  );

  const value = useMemo(
    () => ({
      language,
      changeLanguage,
      t,
      supportedLanguages: SUPPORTED_LANGUAGES,
    }),
    [language, changeLanguage, t]
  );

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export default LanguageProvider;
