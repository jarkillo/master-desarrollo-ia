/**
 * LanguageSelector - Simple language switcher component
 */
import { useTranslation } from 'react-i18next';
import './LanguageSelector.css';

export const LanguageSelector = () => {
  const { i18n } = useTranslation();

  const languages = [
    { code: 'es', label: 'Español', flag: '🇪🇸' },
    { code: 'en', label: 'English', flag: '🇬🇧' },
  ];

  const changeLanguage = (langCode: string) => {
    i18n.changeLanguage(langCode);
  };

  return (
    <div className="language-selector">
      {languages.map((lang) => (
        <button
          key={lang.code}
          className={`lang-btn ${i18n.language === lang.code ? 'active' : ''}`}
          onClick={() => changeLanguage(lang.code)}
          title={lang.label}
        >
          <span className="flag">{lang.flag}</span>
          <span className="lang-code">{lang.code.toUpperCase()}</span>
        </button>
      ))}
    </div>
  );
};
