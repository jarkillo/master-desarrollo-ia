/**
 * i18n Configuration
 *
 * Configures internationalization with Spanish as default language
 * and English as an option.
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import es from './locales/es.json';
import en from './locales/en.json';

// Initialize i18next
i18n
  // Detect user language
  .use(LanguageDetector)
  // Pass i18n instance to react-i18next
  .use(initReactI18next)
  // Initialize
  .init({
    resources: {
      es: { translation: es },
      en: { translation: en },
    },
    // Default language is Spanish
    fallbackLng: 'es',
    lng: 'es', // Force Spanish as initial language

    // Namespace configuration
    defaultNS: 'translation',
    ns: ['translation'],

    // Debug only in development
    debug: import.meta.env.DEV,

    // React-specific options
    react: {
      useSuspense: false, // Avoid suspense to prevent loading delays
    },

    // Interpolation options
    interpolation: {
      escapeValue: false, // React already escapes by default
    },

    // Detection options (prioritize localStorage)
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
      lookupLocalStorage: 'i18nextLng',
    },
  });

export default i18n;
