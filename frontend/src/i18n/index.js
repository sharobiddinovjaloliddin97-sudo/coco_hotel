import en from './en';
import { completeTranslations } from './complete';
import uz from './uz';
import ru from './ru';

export const translations = { en: completeTranslations('en', en), uz: completeTranslations('uz', uz), ru: completeTranslations('ru', ru) };
export const SUPPORTED_LANGUAGES = ['uz', 'ru', 'en'];
export const DEFAULT_LANGUAGE = 'en';

export function getNestedTranslation(obj, path) {
  if (!obj || !path) return null;
  const parts = path.split('.');
  let current = obj;
  for (const part of parts) {
    if (current && typeof current === 'object' && part in current) {
      current = current[part];
    } else {
      return null;
    }
  }
  return typeof current === 'string' ? current : null;
}
