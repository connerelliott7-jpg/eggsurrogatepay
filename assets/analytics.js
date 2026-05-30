// EggSurrogatePay — shared analytics (cta_click, sign_up)
(function () {
  'use strict';

  function isTrackable() {
    return window.location.hostname === 'eggsurrogatepay.com';
  }

  function bindTracking() {
    if (document.body && document.body.dataset.espTrackingBound === 'true') return;
    if (document.body) document.body.dataset.espTrackingBound = 'true';

    // cta_click — global delegation for primary CTA buttons
    document.addEventListener('click', function (event) {
      if (!isTrackable()) return;
      var target = event.target;
      var el = target && target.closest
        ? target.closest('.btn--primary, .btn-primary, [data-cta]')
        : null;
      if (!el) return;
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', 'cta_click', {
        event_category: 'conversion',
        cta_text: (el.textContent || '').trim().substring(0, 50),
        destination: el.href || '',
        page_path: window.location.pathname
      });
    });

    // sign_up — fire on email capture form submit
    document.addEventListener('submit', function (event) {
      if (!isTrackable()) return;
      var form = event.target;
      if (!form || form.tagName !== 'FORM') return;
      if (!form.hasAttribute('data-email-signup')) return;
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', 'sign_up', {
        method: 'email_form'
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindTracking, { once: true });
  } else {
    bindTracking();
  }
})();
