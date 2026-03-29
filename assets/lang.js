/**
 * Language detection & switcher
 * Detects browser language → matches to supported languages → defaults to English
 * Stores user preference in localStorage so manual override persists
 */

const SUPPORTED_LANGS = [
  { code: 'ja', label: '日本語', match: ['ja'] },
  { code: 'en', label: 'EN',     match: ['en'] },
  { code: 'zh-tw', label: '繁中', match: ['zh-tw', 'zh-hant', 'zh-hk', 'zh-mo'] },
  { code: 'vi', label: 'Vi',     match: ['vi'] },
  { code: 'my', label: 'MY',     match: ['my'] },
];

const DEFAULT_LANG = 'en';
const STORAGE_KEY = 'kurashi-otoku-lang';

function detectBrowserLang() {
  const langs = navigator.languages || [navigator.language || navigator.userLanguage || ''];
  for (const browserLang of langs) {
    const lower = browserLang.toLowerCase();
    for (const supported of SUPPORTED_LANGS) {
      for (const pattern of supported.match) {
        if (lower === pattern || lower.startsWith(pattern + '-')) {
          return supported.code;
        }
      }
    }
  }
  return DEFAULT_LANG;
}

function getActiveLang() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored && SUPPORTED_LANGS.some(l => l.code === stored)) {
    return stored;
  }
  return detectBrowserLang();
}

function setActiveLang(code) {
  localStorage.setItem(STORAGE_KEY, code);
  applyLang(code);
}

function applyLang(code) {
  // Update lang switcher buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    const btnLang = btn.getAttribute('data-lang');
    btn.classList.toggle('active', btnLang === code);
  });

  // Update html lang attribute
  document.documentElement.lang = code === 'zh-tw' ? 'zh-Hant' : code;

  // Show/hide content by data-lang attribute
  document.querySelectorAll('[data-lang-content]').forEach(el => {
    const elLang = el.getAttribute('data-lang-content');
    el.style.display = elLang === code ? '' : 'none';
  });

  // Update text nodes with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const translations = window.I18N && window.I18N[key];
    if (translations && translations[code]) {
      el.textContent = translations[code];
    }
  });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  const activeLang = getActiveLang();

  // Bind click handlers to lang buttons
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const lang = this.getAttribute('data-lang');
      if (lang) {
        setActiveLang(lang);
      }
    });
  });

  // Apply detected/stored language
  applyLang(activeLang);
});
