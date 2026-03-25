/* =====================================================
   HAPA GmbH — JavaScript Interaktionen
   Navigation · Scroll-Animationen · Smooth Scroll
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

    // ============================================================
    // NAVBAR — Scroll-Effekt & Sticky
    // ============================================================
    var navbar = document.getElementById('navbar');

    function handleNavScroll() {
        if (window.scrollY > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    window.addEventListener('scroll', handleNavScroll, { passive: true });
    handleNavScroll();

    // ============================================================
    // NAVBAR — Aktiver Link beim Scrollen
    // ============================================================
    var sections = document.querySelectorAll('section[id]');
    var navLinks = document.querySelectorAll('.nav-link');

    var sectionObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var id = entry.target.getAttribute('id');
                navLinks.forEach(function (link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, {
        root: null,
        rootMargin: '-50% 0px -50% 0px',
        threshold: 0
    });

    sections.forEach(function (s) { sectionObserver.observe(s); });

    // ============================================================
    // HAMBURGER MENÜ (Mobile)
    // ============================================================
    var navToggle = document.getElementById('navToggle');
    var navMenu = document.getElementById('navMenu');

    var overlay = document.createElement('div');
    overlay.classList.add('nav-overlay');
    document.body.appendChild(overlay);

    function openMenu() {
        navMenu.classList.add('active');
        navToggle.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        navToggle.setAttribute('aria-label', 'Menü schliessen');
        navToggle.setAttribute('aria-expanded', 'true');
    }

    function closeMenu() {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        navToggle.setAttribute('aria-label', 'Menü öffnen');
        navToggle.setAttribute('aria-expanded', 'false');
    }

    if (navToggle) {
        navToggle.addEventListener('click', function () {
            if (navMenu.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }

    overlay.addEventListener('click', closeMenu);

    document.querySelectorAll('.nav-link').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeMenu();
    });

    // ============================================================
    // SMOOTH SCROLL für Anker-Links (mit Offset)
    // ============================================================
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var href = this.getAttribute('href');
            if (href === '#') return;
            var target = document.querySelector(href);
            if (!target) return;
            e.preventDefault();
            var offset = navbar.offsetHeight + 20;
            var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top: top, behavior: 'smooth' });
        });
    });

    // ============================================================
    // SCROLL-ANIMATIONEN (IntersectionObserver)
    // ============================================================
    var animateElements = document.querySelectorAll('.fade-up');

    var animObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                animObserver.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.1
    });

    animateElements.forEach(function (el) { animObserver.observe(el); });

}); // end DOMContentLoaded
