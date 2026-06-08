/**
 * Cookie Consent Banner
 * Displays a cookie consent banner and handles Google Analytics loading based on user choice
 */

(function(window) {
  'use strict';

  var CookieConsent = {
    STORAGE_KEY: 'cookieConsent',

    /**
     * Initialize the cookie consent banner
     * @param {Object} options - Configuration options
     * @param {string} options.gtagId - Google Analytics tracking ID
     * @param {Object} options.translations - Translation object for the banner text
     */
    init: function(options) {
      this.gtagId = options.gtagId;
      this.translations = options.translations || this.getDefaultTranslations();

      var consent = this.getConsent();

      if (consent === 'accepted') {
        this.loadGtag();
      } else if (consent === null) {
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', this.showBanner.bind(this));
        } else {
          this.showBanner();
        }
      }
      // If declined, do nothing
    },

    /**
     * Get user consent from localStorage
     * @returns {string|null} 'accepted', 'declined', or null
     */
    getConsent: function() {
      try {
        return localStorage.getItem(this.STORAGE_KEY);
      } catch (e) {
        return null;
      }
    },

    /**
     * Save user consent to localStorage
     * @param {string} value - 'accepted' or 'declined'
     */
    saveConsent: function(value) {
      try {
        localStorage.setItem(this.STORAGE_KEY, value);
      } catch (e) {
        console.warn('Could not save consent to localStorage:', e);
      }
    },

    /**
     * Load Google Analytics dynamically
     */
    loadGtag: function() {
      if (!this.gtagId) return;

      // Initialize dataLayer
      window.dataLayer = window.dataLayer || [];
      window.gtag = function() {
        window.dataLayer.push(arguments);
      };

      // Load gtag.js script
      var script = document.createElement('script');
      script.async = true;
      script.src = 'https://www.googletagmanager.com/gtag/js?id=' + this.gtagId;
      script.onload = function() {
        gtag('js', new Date());
        gtag('config', this.gtagId);
      }.bind(this);

      var firstScript = document.getElementsByTagName('script')[0];
      firstScript.parentNode.insertBefore(script, firstScript);
    },

    /**
     * Show the consent banner
     */
    showBanner: function() {
      var banner = this.createBanner();
      document.body.appendChild(banner);
    },

    /**
     * Create the banner DOM element
     * @returns {HTMLElement}
     */
    createBanner: function() {
      var container = document.createElement('div');
      container.id = 'cookie-consent-banner';
      container.className = 'cookie-consent-banner';

      var content = document.createElement('div');
      content.className = 'cookie-consent-content';

      var message = document.createElement('p');
      message.className = 'cookie-consent-message';
      message.textContent = this.translations.message;

      var buttons = document.createElement('div');
      buttons.className = 'cookie-consent-buttons';

      var acceptBtn = document.createElement('button');
      acceptBtn.className = 'cookie-consent-button cookie-consent-accept';
      acceptBtn.textContent = this.translations.accept;
      acceptBtn.onclick = this.handleAccept.bind(this);

      var declineBtn = document.createElement('button');
      declineBtn.className = 'cookie-consent-button cookie-consent-decline';
      declineBtn.textContent = this.translations.decline;
      declineBtn.onclick = this.handleDecline.bind(this);

      buttons.appendChild(acceptBtn);
      buttons.appendChild(declineBtn);
      content.appendChild(message);
      content.appendChild(buttons);
      container.appendChild(content);

      return container;
    },

    /**
     * Handle user accepting cookies
     */
    handleAccept: function() {
      this.saveConsent('accepted');
      this.hideBanner();
      this.loadGtag();
    },

    /**
     * Handle user declining cookies
     */
    handleDecline: function() {
      this.saveConsent('declined');
      this.hideBanner();
    },

    /**
     * Hide and remove the banner
     */
    hideBanner: function() {
      var banner = document.getElementById('cookie-consent-banner');
      if (banner && banner.parentNode) {
        banner.parentNode.removeChild(banner);
      }
    },

    /**
     * Get default English translations
     * @returns {Object}
     */
    getDefaultTranslations: function() {
      return {
        message: 'We use cookies to improve your experience. You can accept or decline.',
        accept: 'Accept All',
        decline: 'Decline'
      };
    }
  };

  // Export to global scope
  window.CookieConsent = CookieConsent;

})(window);

/**
 * Inject CSS styles
 */
(function() {
  var css = [
    '.cookie-consent-banner {',
    '  position: fixed;',
    '  bottom: 0;',
    '  left: 0;',
    '  right: 0;',
    '  z-index: 9999;',
    '  background: rgba(0, 0, 0, 0.5);',
    '  backdrop-filter: blur(4px);',
    '  -webkit-backdrop-filter: blur(4px);',
    '  padding: 16px;',
    '}',
    '',
    '.cookie-consent-content {',
    '  max-width: 900px;',
    '  margin: 0 auto;',
    '  background: white;',
    '  border-radius: 12px;',
    '  padding: 20px;',
    '  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);',
    '  display: flex;',
    '  flex-direction: column;',
    '  gap: 16px;',
    '}',
    '',
    '@media (min-width: 600px) {',
    '  .cookie-consent-content {',
    '    flex-direction: row;',
    '    align-items: center;',
    '    justify-content: space-between;',
    '  }',
    '}',
    '',
    '.cookie-consent-message {',
    '  margin: 0;',
    '  font-size: 14px;',
    '  line-height: 1.5;',
    '  color: #333;',
    '  flex: 1;',
    '}',
    '',
    '.cookie-consent-buttons {',
    '  display: flex;',
    '  gap: 12px;',
    '  flex-shrink: 0;',
    '}',
    '',
    '.cookie-consent-button {',
    '  padding: 10px 20px;',
    '  border: none;',
    '  border-radius: 6px;',
    '  font-size: 14px;',
    '  font-weight: 500;',
    '  cursor: pointer;',
    '  transition: background-color 0.2s, transform 0.1s;',
    '}',
    '',
    '.cookie-consent-button:hover {',
    '  transform: translateY(-1px);',
    '}',
    '',
    '.cookie-consent-button:active {',
    '  transform: translateY(0);',
    '}',
    '',
    '.cookie-consent-accept {',
    '  background: #4a90e2;',
    '  color: white;',
    '}',
    '',
    '.cookie-consent-accept:hover {',
    '  background: #3a7bc8;',
    '}',
    '',
    '.cookie-consent-decline {',
    '  background: #f5f5f5;',
    '  color: #666;',
    '}',
    '',
    '.cookie-consent-decline:hover {',
    '  background: #e5e5e5;',
    '}'
  ].join('\n');

  var style = document.createElement('style');
  style.textContent = css;
  var head = document.head || document.getElementsByTagName('head')[0];
  head.appendChild(style);
})();
