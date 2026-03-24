/* =====================================================
   STUDIO ALBERTO — JavaScript Interaktionen
   Reservierungssystem, Animationen & UI
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {

    // === Navbar Scroll Effect ===
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    const handleScroll = () => {
        const currentScroll = window.scrollY;
        if (currentScroll > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    };
    window.addEventListener('scroll', handleScroll);

    // === Mobile Navigation ===
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }

    // Close menu on link click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // === Active Link on Scroll ===
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    const sectionObserverOptions = {
        root: null,
        rootMargin: '-50% 0px -50% 0px',
        threshold: 0
    };

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
    }, sectionObserverOptions);

    sections.forEach(section => sectionObserver.observe(section));

    // === Scroll Animations ===
    const animateElements = document.querySelectorAll(
        '.fade-in, .fade-in-left, .fade-in-right, .scale-in'
    );

    const animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                animationObserver.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -60px 0px',
        threshold: 0.1
    });

    animateElements.forEach(el => animationObserver.observe(el));

    // === Hero Particles ===
    const particlesContainer = document.getElementById('heroParticles');
    if (particlesContainer) {
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDuration = (8 + Math.random() * 12) + 's';
            particle.style.animationDelay = (Math.random() * 10) + 's';
            particle.style.width = (2 + Math.random() * 4) + 'px';
            particle.style.height = particle.style.width;
            particle.style.opacity = String(0.2 + Math.random() * 0.4);
            particlesContainer.appendChild(particle);
        }
    }

    // === Smooth scroll for anchor links ===
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href === '#') return;
            const target = document.querySelector(href);
            if (target) {
                const offset = navbar.offsetHeight + 20;
                const position = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({
                    top: position,
                    behavior: 'smooth'
                });
            }
        });
    });

    // === Booking Form ===
    const bookingForm = document.getElementById('bookingForm');
    const bookingSuccess = document.getElementById('bookingSuccess');
    const newBookingBtn = document.getElementById('newBookingBtn');

    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();

            // Validate required fields
            const name = bookingForm.querySelector('#bookingName');
            const phone = bookingForm.querySelector('#bookingPhone');
            const date = bookingForm.querySelector('#bookingDate');
            const service = bookingForm.querySelector('input[name="service"]:checked');
            const time = bookingForm.querySelector('input[name="time"]:checked');

            if (!name.value || !phone.value || !date.value) {
                shakeElement(bookingForm.querySelector('.btn'));
                return;
            }

            if (!service) {
                shakeElement(document.querySelector('.service-select-grid'));
                return;
            }

            if (!time) {
                shakeElement(document.querySelector('.time-slots'));
                return;
            }

            // Simulate booking
            const btn = bookingForm.querySelector('button[type="submit"]');
            const originalText = btn.textContent;
            btn.textContent = 'Wird gebucht...';
            btn.disabled = true;
            btn.style.opacity = '0.7';

            setTimeout(() => {
                bookingForm.style.display = 'none';
                bookingSuccess.classList.add('show');

                // Fill in success details
                const serviceName = service.nextElementSibling.querySelector('.s-name').textContent;
                const timeValue = time.nextElementSibling.textContent;
                const dateValue = new Date(date.value).toLocaleDateString('de-CH', {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                });

                const summaryEl = document.getElementById('bookingSummary');
                if (summaryEl) {
                    summaryEl.innerHTML =
                        '<strong>' + serviceName + '</strong><br>' +
                        dateValue + ' um ' + timeValue + ' Uhr';
                }

                btn.textContent = originalText;
                btn.disabled = false;
                btn.style.opacity = '1';
            }, 1500);
        });
    }

    if (newBookingBtn) {
        newBookingBtn.addEventListener('click', () => {
            bookingSuccess.classList.remove('show');
            bookingForm.style.display = 'flex';
            bookingForm.reset();
        });
    }

    // Set min date for booking (today)
    const bookingDate = document.getElementById('bookingDate');
    if (bookingDate) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        bookingDate.min = yyyy + '-' + mm + '-' + dd;
    }

    // === Contact Form ===
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const btn = contactForm.querySelector('button[type="submit"]');
            const originalText = btn.textContent;
            btn.textContent = 'Wird gesendet...';
            btn.disabled = true;

            setTimeout(() => {
                btn.textContent = '✓ Nachricht gesendet!';
                btn.style.background = '#27ae60';
                btn.style.borderColor = '#27ae60';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                    btn.style.borderColor = '';
                    btn.disabled = false;
                    contactForm.reset();
                }, 3000);
            }, 1200);
        });
    }

    // === Shake animation helper ===
    function shakeElement(el) {
        if (!el) return;
        el.style.animation = 'shake 0.5s ease';
        el.addEventListener('animationend', () => {
            el.style.animation = '';
        }, { once: true });
    }

    // === Counter Animation ===
    const counterElements = document.querySelectorAll('[data-count]');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counterElements.forEach(el => counterObserver.observe(el));

    function animateCounter(el) {
        const target = parseInt(el.dataset.count, 10);
        const duration = 2000;
        const step = Math.ceil(target / (duration / 16));
        let current = 0;
        const suffix = el.dataset.suffix || '';

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current + suffix;
        }, 16);
    }

    // === Testimonial carousel auto-scroll (optional) ===
    const track = document.querySelector('.testimonials-track');
    if (track) {
        let scrollAmount = 0;
        const cards = track.querySelectorAll('.testimonial-card');
        if (cards.length > 3) {
            // Clone cards for infinite scroll
            cards.forEach(card => {
                const clone = card.cloneNode(true);
                track.appendChild(clone);
            });
        }
    }

});

// === Add shake animation style ===
const shakeStyle = document.createElement('style');
shakeStyle.textContent = '\n    @keyframes shake {\n        0%, 100% { transform: translateX(0); }\n        20% { transform: translateX(-8px); }\n        40% { transform: translateX(8px); }\n        60% { transform: translateX(-4px); }\n        80% { transform: translateX(4px); }\n    }\n';
document.head.appendChild(shakeStyle);
