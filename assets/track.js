// GA4 event for clicks on the Rakuten Mobile referral (affiliate) link.
// Records WHICH button was used so CTA placement can be compared per page/language.
// Outbound clicks to other sites are already covered by GA4 enhanced measurement.
(function () {
  var AFFILIATE = 'r10.to/';

  function ctaLocation(a) {
    if (a.closest('#sticky-cta')) return 'sticky_bar';
    if (a.closest('#float-banner')) return 'float_banner';
    if (a.closest('.guide-cta')) return 'guide_bottom';
    if (a.closest('.guide-step')) return 'guide_step';
    if (a.closest('.plan-card')) return 'sim_plan_card';
    if (a.querySelector('img')) return 'top_banner';
    return 'inline';
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || a.href.indexOf(AFFILIATE) === -1) return;
    if (typeof window.gtag !== 'function') return; // GA blocked (ad blocker) — nothing to record
    window.gtag('event', 'affiliate_click', {
      cta_location: ctaLocation(a),
      page_lang: document.documentElement.lang || 'unknown',
      link_url: a.href,
      transport_type: 'beacon'
    });
  }, true);
})();
