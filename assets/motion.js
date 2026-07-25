/* LA Traders — Motion Layer
   anime.js-powered scroll reveals + micro-interactions.
   Loaded async after mobile-menu.js (which loads anime.js from CDN).
   Respects prefers-reduced-motion. */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Wait for anime.js (loaded by mobile-menu.js) ──
  var animeReady = !!window.anime;
  if (!animeReady) {
    // Poll briefly; mobile-menu.js loads it async
    var polls = 0;
    var pollInterval = setInterval(function () {
      polls++;
      if (window.anime || polls > 30) {
        clearInterval(pollInterval);
        animeReady = !!window.anime;
        init();
      }
    }, 100);
  } else {
    init();
  }

  function init() {
    initScrollReveals();
    initButtonMicro();
    initHeroStagger();
  }

  // ── Scroll-triggered reveals (anime.js stagger) ──
  function initScrollReveals() {
    var els = document.querySelectorAll('.reveal:not(.in)');
    if (!els.length) return;

    if (reducedMotion || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }

    // If anime.js isn't available, fall back to CSS class toggle
    if (!animeReady) {
      var ioCSS = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('in'); ioCSS.unobserve(e.target); }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -5% 0px' });
      els.forEach(function (el) { ioCSS.observe(el); });
      setTimeout(function () { els.forEach(function (el) { el.classList.add('in'); }); }, 2500);
      return;
    }

    // anime.js powered: stagger within each group
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        io.unobserve(el);

        // Check for staggered children
        var staggerChildren = el.querySelectorAll('.reveal-child');
        if (staggerChildren.length) {
          window.anime({
            targets: el,
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 500,
            easing: 'easeOutCubic'
          });
          window.anime({
            targets: staggerChildren,
            opacity: [0, 1],
            translateY: [16, 0],
            delay: window.anime.stagger(80, { start: 100 }),
            duration: 500,
            easing: 'easeOutCubic'
          });
        } else {
          window.anime({
            targets: el,
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 600,
            easing: 'easeOutCubic'
          });
        }
        el.classList.add('in');
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -5% 0px' });

    els.forEach(function (el) { io.observe(el); });

    // Fallback: reveal after 3s
    setTimeout(function () {
      els.forEach(function (el) {
        if (!el.classList.contains('in')) {
          el.classList.add('in');
          el.style.opacity = '1';
          el.style.transform = 'none';
        }
      });
    }, 3000);
  }

  // ── Button micro-interactions ──
  function initButtonMicro() {
    if (reducedMotion || !animeReady) return;

    document.querySelectorAll('.btn, .nav-cta, .mega-nav-cta, .nav-discord').forEach(function (btn) {
      btn.addEventListener('mouseenter', function () {
        window.anime({
          targets: btn,
          scale: 1.03,
          duration: 200,
          easing: 'easeOutQuad'
        });
      });
      btn.addEventListener('mouseleave', function () {
        window.anime({
          targets: btn,
          scale: 1,
          duration: 200,
          easing: 'easeOutQuad'
        });
      });
    });
  }

  // ── Hero stagger (runs on page load if hero elements exist) ──
  function initHeroStagger() {
    if (reducedMotion) return;

    var heroLogo = document.querySelector('.hero-logo');
    var heroEyebrow = document.querySelector('.hero-eyebrow');
    var heroH1 = document.querySelector('.hero h1');
    var heroSub = document.querySelector('.hero-sub');
    var heroCtas = document.querySelector('.hero-ctas');
    var heroRrr = document.querySelector('.hero-rrr');

    // Only run on homepage hero
    if (!heroH1 && !heroSub) return;

    // The homepage already has CSS animations (hero-rise keyframes).
    // For subpages that add .hero-stagger class, we use anime.js timeline.
    var heroSection = document.querySelector('.hero-stagger');
    if (!heroSection) return;

    var tl = window.anime.timeline({ easing: 'easeOutExpo' });
    if (heroLogo) tl.add({ targets: heroLogo, opacity: [0, 1], translateY: [20, 0], duration: 600 });
    if (heroEyebrow) tl.add({ targets: heroEyebrow, opacity: [0, 1], translateY: [16, 0], duration: 500 }, '-=400');
    if (heroH1) tl.add({ targets: heroH1, opacity: [0, 1], translateY: [24, 0], duration: 700 }, '-=350');
    if (heroSub) tl.add({ targets: heroSub, opacity: [0, 1], translateY: [20, 0], duration: 500 }, '-=500');
    if (heroCtas) tl.add({ targets: heroCtas, opacity: [0, 1], translateY: [16, 0], duration: 500 }, '-=400');
    if (heroRrr) tl.add({ targets: heroRrr, opacity: [0, 1], translateY: [12, 0], duration: 400 }, '-=300');
  }
})();
