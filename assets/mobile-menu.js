/* LA Traders — Mobile Menu Injector
   Auto-injects hamburger button + slide-in mobile menu into every page.
   Uses the site's existing nav structure to build menu sections.
   Purple + gold animated hamburger. */
(function () {
  'use strict';

  // Only on mobile
  if (window.matchMedia('(min-width: 861px)').matches) return;

  // Don't double-inject
  if (document.querySelector('.hamburger')) return;

  // ── Build hamburger button ──
  var hamburger = document.createElement('button');
  hamburger.className = 'hamburger';
  hamburger.setAttribute('aria-label', 'Toggle menu');
  hamburger.setAttribute('aria-expanded', 'false');
  hamburger.innerHTML = '<span></span><span></span><span></span>';

  // ── Build backdrop ──
  var backdrop = document.createElement('div');
  backdrop.className = 'mobile-menu-backdrop';

  // ── Build mobile menu ──
  var menu = document.createElement('div');
  menu.className = 'mobile-menu';

  // ── Collect nav links from the page ──
  // Works for both homepage (nav-item > a) and subpages (mega-item > a)
  var navLinks = document.querySelectorAll('.nav-links .nav-item > a, .nav-links .mega-item > a');
  var navDropdowns = document.querySelectorAll('.nav-links .nav-dropdown, .nav-links .mega-dropdown');

  // Build menu sections
  var sections = [];

  // The System
  sections.push({
    title: 'The System',
    links: [
      { href: '/#protocol', label: 'The 6:00 AM Protocol' },
      { href: '/#rrr', label: 'RRR Framework' },
      { href: '/glossary/a-plus-setup/', label: 'The A+ Setup' },
      { href: '/glossary/six-am-protocol/', label: '6:00 AM Protocol' },
      { href: '/glossary/rrr-framework/', label: 'RRR Framework' },
      { href: '/glossary/reveal/', label: 'Reveal' },
      { href: '/glossary/retrace/', label: 'Retrace' },
      { href: '/glossary/run/', label: 'Run' }
    ]
  });

  // Glossary
  sections.push({
    title: 'Glossary',
    links: [
      { href: '/glossary/', label: 'All Terms' },
      { href: '/glossary/market-structure/', label: 'Market Structure' },
      { href: '/glossary/liquidity/', label: 'Liquidity' },
      { href: '/glossary/order-block/', label: 'Price Action' },
      { href: '/glossary/new-york-session/', label: 'Sessions & Time' },
      { href: '/glossary/risk-to-reward/', label: 'Risk & Execution' },
      { href: '/glossary/es-futures/', label: 'Instruments' },
      { href: '/glossary/options-contract/', label: 'Options' }
    ]
  });

  // Tools
  sections.push({
    title: 'Tools',
    links: [
      { href: '/tools/', label: 'All Tools & Session Clock' },
      { href: '/tools/daily-checklist/', label: 'Interactive Checklist' },
      { href: '/tools/position-size-calculator/', label: 'Position Size Calculator' },
      { href: '/tools/journal/', label: 'Trade Journal' },
      { href: '/#checklist', label: 'Free PDF Checklist' },
      { href: '/#oslite', label: 'RRR OS Lite — $17' }
    ]
  });

  // Legal
  sections.push({
    title: 'Legal',
    links: [
      { href: '/terms/', label: 'Terms of Service' },
      { href: '/privacy/', label: 'Privacy Policy' }
    ]
  });

  // Build HTML
  var html = '';
  sections.forEach(function (sec) {
    html += '<div class="mm-section">';
    html += '<h5>' + sec.title + '</h5>';
    html += '<ul>';
    sec.links.forEach(function (link) {
      html += '<li><a href="' + link.href + '">' + link.label + '</a></li>';
    });
    html += '</ul>';
    html += '</div>';
  });
  menu.innerHTML = html;

  // ── Insert into DOM ──
  // Find nav element
  var nav = document.querySelector('nav');
  if (!nav) return;

  // Insert hamburger into nav (right side)
  nav.appendChild(hamburger);

  // Insert menu + backdrop at end of body
  document.body.appendChild(backdrop);
  document.body.appendChild(menu);

  // ── Toggle logic ──
  var isOpen = false;

  function toggleMenu() {
    isOpen = !isOpen;
    hamburger.classList.toggle('open', isOpen);
    menu.classList.toggle('open', isOpen);
    backdrop.classList.toggle('open', isOpen);
    hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }

  function closeMenu() {
    if (!isOpen) return;
    isOpen = false;
    hamburger.classList.remove('open');
    menu.classList.remove('open');
    backdrop.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  hamburger.addEventListener('click', function (e) {
    e.stopPropagation();
    toggleMenu();
  });

  backdrop.addEventListener('click', closeMenu);

  // Close on link click (for SPA-like nav)
  menu.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') closeMenu();
  });

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });

  // Close on resize to desktop
  window.addEventListener('resize', function () {
    if (window.innerWidth > 860) closeMenu();
  });
})();
