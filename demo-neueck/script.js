/* =====================================================
   NEUECK IMBISS WATTWIL — JavaScript Interaktionen
   Intro · Sticky Nav · Hamburger · Animationen · Filter
   ===================================================== */

/* ============================================================
   DÜRÜM INTRO — Auto-dismiss + click-to-skip
   ============================================================ */
(function () {
    var intro = document.getElementById('durum-intro');
    if (!intro) return;

    document.body.style.overflow = 'hidden';

    function dismiss() {
        intro.classList.add('intro-exit');
        setTimeout(function () {
            intro.remove();
            document.body.style.overflow = '';
        }, 880);
    }

    // Auto-dismiss after 3.5s
    var autoTimer = setTimeout(dismiss, 3500);

    // Click/tap anywhere to skip
    intro.addEventListener('click', function () {
        clearTimeout(autoTimer);
        dismiss();
    }, { once: true });
}());

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
    var animateElements = document.querySelectorAll(
        '.fade-in, .fade-in-left, .fade-in-right, .fade-up'
    );

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

    // ============================================================
    // COUNTER ANIMATION — Zahlen hochzählen
    // ============================================================
    var statNumbers = document.querySelectorAll('.stat-number[data-target]');

    var counterObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(function (el) { counterObserver.observe(el); });

    function animateCounter(el) {
        var target = parseFloat(el.getAttribute('data-target'));
        var isDecimal = el.hasAttribute('data-decimal');
        var prefix = el.getAttribute('data-prefix') || '';
        var suffix = el.getAttribute('data-suffix') || '';
        var duration = 2000;
        var startTime = null;

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
            var current = eased * target;

            if (isDecimal) {
                el.textContent = prefix + current.toFixed(1) + suffix;
            } else {
                el.textContent = prefix + Math.floor(current) + suffix;
            }

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        }

        requestAnimationFrame(step);
    }

    // ============================================================
    // MENU FILTER
    // ============================================================
    var filterBtns = document.querySelectorAll('.filter-btn');
    var menuCards = document.querySelectorAll('.menu-card');

    filterBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            var filter = this.getAttribute('data-filter');

            filterBtns.forEach(function (b) { b.classList.remove('active'); });
            this.classList.add('active');

            menuCards.forEach(function (card) {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.classList.remove('hidden');
                    card.style.animation = 'menuFadeIn 0.4s ease forwards';
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });

    // ============================================================
    // OPEN/CLOSED STATUS
    // ============================================================
    var statusBadge = document.getElementById('openStatus');
    if (statusBadge) {
        var now = new Date();
        var hour = now.getHours();
        // Open 11:00 - 22:00
        if (hour >= 11 && hour < 22) {
            statusBadge.textContent = 'Jetzt geöffnet';
            statusBadge.className = 'status-badge open';
        } else {
            statusBadge.textContent = 'Geschlossen · Öffnet um 11:00';
            statusBadge.className = 'status-badge closed';
        }
    }

}); // end DOMContentLoaded

// ============================================================
// MENU FADE-IN KEYFRAME (injected once)
// ============================================================
var menuStyle = document.createElement('style');
menuStyle.textContent = '\
    @keyframes menuFadeIn {\
        from { opacity: 0; transform: translateY(10px); }\
        to   { opacity: 1; transform: translateY(0); }\
    }\
';
document.head.appendChild(menuStyle);
