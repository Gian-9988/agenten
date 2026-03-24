/* =====================================================
   HUENAILS NAGELSTUDIO — JavaScript Interaktionen
   Sticky Nav · Hamburger · Animationen · Formulare
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // ============================================================
    // NAVBAR — Scroll-Effekt & Sticky
    // ============================================================
    const navbar = document.getElementById('navbar');

    const handleNavScroll = () => {
        if (window.scrollY > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };
    window.addEventListener('scroll', handleNavScroll, { passive: true });
    handleNavScroll(); // initial check

    // ============================================================
    // NAVBAR — Aktiver Link beim Scrollen
    // ============================================================
    const sections  = document.querySelectorAll('section[id]');
    const navLinks  = document.querySelectorAll('.nav-link');

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
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

    sections.forEach(s => sectionObserver.observe(s));

    // ============================================================
    // HAMBURGER MENÜ (Mobile)
    // ============================================================
    const navToggle  = document.getElementById('navToggle');
    const navMenu    = document.getElementById('navMenu');

    // Create overlay for mobile menu backdrop
    const overlay = document.createElement('div');
    overlay.classList.add('nav-overlay');
    document.body.appendChild(overlay);

    function openMenu() {
        navMenu.classList.add('active');
        navToggle.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        navToggle.setAttribute('aria-label', 'Menü schließen');
    }

    function closeMenu() {
        navMenu.classList.remove('active');
        navToggle.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        navToggle.setAttribute('aria-label', 'Menü öffnen');
    }

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            if (navMenu.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }

    overlay.addEventListener('click', closeMenu);

    // Close menu on nav link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // Close menu on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });

    // ============================================================
    // SMOOTH SCROLL für Anker-Links (mit Offset für Sticky Navbar)
    // ============================================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (!target) return;
            e.preventDefault();
            const offset = navbar.offsetHeight + 20;
            const top = target.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });

    // ============================================================
    // SCROLL-ANIMATIONEN (IntersectionObserver)
    // ============================================================
    const animateElements = document.querySelectorAll(
        '.fade-in, .fade-in-left, .fade-in-right, .fade-up'
    );

    const animObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
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

    animateElements.forEach(el => animObserver.observe(el));

    // Hero-Elemente sofort sichtbar machen (sind beim Load schon im Viewport)
    document.querySelectorAll('.hero-content .fade-up').forEach(el => {
        // small rAF delay so CSS transition still fires
        requestAnimationFrame(() => {
            requestAnimationFrame(() => el.classList.add('visible'));
        });
    });

    // ============================================================
    // TERMIN BUCHEN — Minimum-Datum auf heute setzen
    // ============================================================
    const bookingDate = document.getElementById('bookingDate');
    if (bookingDate) {
        const today = new Date();
        const yyyy  = today.getFullYear();
        const mm    = String(today.getMonth() + 1).padStart(2, '0');
        const dd    = String(today.getDate()).padStart(2, '0');
        bookingDate.min = `${yyyy}-${mm}-${dd}`;
    }

    // ============================================================
    // TERMIN BUCHEN — Formular-Submit
    // ============================================================
    const bookingForm    = document.getElementById('bookingForm');
    const bookingSuccess = document.getElementById('bookingSuccess');
    const newBookingBtn  = document.getElementById('newBookingBtn');

    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const nameEl    = bookingForm.querySelector('#bookingName');
            const serviceEl = bookingForm.querySelector('#bookingService');
            const dateEl    = bookingForm.querySelector('#bookingDate');
            const timeEl    = bookingForm.querySelector('#bookingTime');

            // Simple validation
            if (!nameEl.value.trim() || !serviceEl.value || !dateEl.value || !timeEl.value) {
                shakeElement(bookingForm.querySelector('button[type="submit"]'));
                highlightEmpty([nameEl, serviceEl, dateEl, timeEl]);
                return;
            }

            const btn = bookingForm.querySelector('button[type="submit"]');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<span>Wird gesendet …</span>';
            btn.disabled = true;

            setTimeout(() => {
                // Show success state
                bookingForm.style.display = 'none';
                bookingSuccess.classList.add('show');

                const summaryEl = document.getElementById('bookingSummary');
                if (summaryEl) {
                    const dateFormatted = new Date(dateEl.value + 'T00:00:00').toLocaleDateString('de-CH', {
                        weekday: 'long',
                        day:     'numeric',
                        month:   'long',
                        year:    'numeric'
                    });
                    summaryEl.textContent = `${serviceEl.value} · ${dateFormatted} um ${timeEl.value} Uhr`;
                }

                btn.innerHTML = originalHTML;
                btn.disabled  = false;
            }, 1400);
        });
    }

    if (newBookingBtn) {
        newBookingBtn.addEventListener('click', () => {
            bookingSuccess.classList.remove('show');
            bookingForm.style.display = '';
            bookingForm.reset();
        });
    }

    // ============================================================
    // KONTAKT — Formular-Submit
    // ============================================================
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const nameEl    = contactForm.querySelector('#contactName');
            const emailEl   = contactForm.querySelector('#contactEmail');
            const messageEl = contactForm.querySelector('#contactMessage');
            const privacyEl = contactForm.querySelector('#contactPrivacy');

            if (!nameEl.value.trim() || !emailEl.value.trim() || !messageEl.value.trim()) {
                shakeElement(contactForm.querySelector('button[type="submit"]'));
                highlightEmpty([nameEl, emailEl, messageEl]);
                return;
            }

            if (!privacyEl.checked) {
                shakeElement(contactForm.querySelector('.checkbox-label'));
                return;
            }

            const btn = contactForm.querySelector('button[type="submit"]');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<span>Wird gesendet …</span>';
            btn.disabled = true;

            setTimeout(() => {
                btn.innerHTML = '<span>✓ Nachricht gesendet!</span>';
                btn.style.background = '#4caf88';
                btn.style.borderColor = '#4caf88';

                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.background = '';
                    btn.style.borderColor = '';
                    btn.disabled = false;
                    contactForm.reset();
                }, 3000);
            }, 1200);
        });
    }

    // ============================================================
    // HELPER — Shake-Animation
    // ============================================================
    function shakeElement(el) {
        if (!el) return;
        el.style.animation = 'shake 0.5s ease';
        el.addEventListener('animationend', () => {
            el.style.animation = '';
        }, { once: true });
    }

    // ============================================================
    // HELPER — Leere Pflichtfelder hervorheben
    // ============================================================
    function highlightEmpty(fields) {
        fields.forEach(field => {
            if (!field) return;
            const empty = !field.value || field.value === '';
            if (empty) {
                field.style.borderColor = '#e07070';
                field.addEventListener('input', () => {
                    field.style.borderColor = '';
                }, { once: true });
            }
        });
    }

});

// ============================================================
// Shake-Keyframe (injected once)
// ============================================================
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20%       { transform: translateX(-8px); }
        40%       { transform: translateX(8px); }
        60%       { transform: translateX(-5px); }
        80%       { transform: translateX(5px); }
    }
`;
document.head.appendChild(shakeStyle);
