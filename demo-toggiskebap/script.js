/* ============================================================
   TOGGI'S KEBAP — JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ============================================================
    // MENU DATA (for ordering system)
    // ============================================================
    const menuData = [
        // Kebap & Dürüm
        { id: 1,  cat: 'kebap', name: 'Döner Kebab (Klein)', price: 11.00 },
        { id: 2,  cat: 'kebap', name: 'Kebab im Taschenbrot (Normal)', price: 13.00 },
        { id: 3,  cat: 'kebap', name: 'Mega Kebab im Taschenbrot', price: 15.00 },
        { id: 4,  cat: 'kebap', name: 'Dürüm (Klein)', price: 11.00 },
        { id: 5,  cat: 'kebap', name: 'Dürüm im Fladenbrot (Normal)', price: 13.00 },
        { id: 6,  cat: 'kebap', name: 'Mega Dürüm im Fladenbrot', price: 15.00 },
        { id: 7,  cat: 'kebap', name: 'Toggi Kebab im Taschenbrot', price: 16.00 },
        { id: 8,  cat: 'kebap', name: 'Toggi Dürüm im Fladenbrot', price: 16.00 },
        { id: 9,  cat: 'kebap', name: 'XXL Dürüm im Fladenbrot', price: 19.00 },
        { id: 10, cat: 'kebap', name: 'Dönerbox (Normal)', price: 13.00 },
        { id: 11, cat: 'kebap', name: 'Dönerbox XL', price: 16.00 },
        // Pizza
        { id: 12, cat: 'pizza', name: 'Pizza Margherita', price: 14.50 },
        { id: 13, cat: 'pizza', name: 'Pizza Funghi', price: 15.50 },
        { id: 14, cat: 'pizza', name: 'Pizza Prosciutto', price: 16.50 },
        { id: 15, cat: 'pizza', name: 'Pizza Stromboli', price: 16.50 },
        { id: 16, cat: 'pizza', name: 'Pizza Oriental', price: 16.50 },
        { id: 17, cat: 'pizza', name: 'Calzone', price: 16.50 },
        { id: 18, cat: 'pizza', name: 'Pizza Salame', price: 17.50 },
        { id: 19, cat: 'pizza', name: 'Pizza Sucuk', price: 17.50 },
        { id: 20, cat: 'pizza', name: 'Pizza Napoli', price: 17.50 },
        { id: 21, cat: 'pizza', name: 'Pizza Prosciutto e Funghi', price: 17.50 },
        { id: 22, cat: 'pizza', name: 'Pizza Padroné', price: 18.50 },
        { id: 23, cat: 'pizza', name: 'Pizza Porcini', price: 18.50 },
        { id: 24, cat: 'pizza', name: 'Pizza Frutti di Mare', price: 19.50 },
        // Pide
        { id: 25, cat: 'pide', name: 'Lahmacun', price: 8.00 },
        { id: 26, cat: 'pide', name: 'Pide Käse', price: 12.00 },
        { id: 27, cat: 'pide', name: 'Pide Spinat', price: 12.00 },
        { id: 28, cat: 'pide', name: 'Pide Hackfleisch', price: 13.00 },
        { id: 29, cat: 'pide', name: 'Pide Sucuk', price: 13.00 },
        { id: 30, cat: 'pide', name: 'Pide Döner', price: 14.00 },
        { id: 31, cat: 'pide', name: 'Pide Poulet', price: 14.00 },
        { id: 32, cat: 'pide', name: 'Pide Mix', price: 15.00 },
        // Türkische Spezialitäten
        { id: 33, cat: 'tuerkisch', name: 'Börek Käse', price: 10.00 },
        { id: 34, cat: 'tuerkisch', name: 'Börek Spinat', price: 10.00 },
        { id: 35, cat: 'tuerkisch', name: 'Sandwich Poulet', price: 9.00 },
        { id: 36, cat: 'tuerkisch', name: 'Sandwich Döner', price: 9.00 },
        { id: 37, cat: 'tuerkisch', name: 'Taco Döner', price: 9.00 },
        { id: 38, cat: 'tuerkisch', name: 'Taco Poulet', price: 9.00 },
        { id: 39, cat: 'tuerkisch', name: 'Taco Falafel', price: 9.00 },
        // Salate
        { id: 40, cat: 'salate', name: 'Gemischter Salat', price: 8.00 },
        { id: 41, cat: 'salate', name: 'Hirtensalat', price: 10.00 },
        { id: 42, cat: 'salate', name: 'Griechischer Salat', price: 11.00 },
        { id: 43, cat: 'salate', name: 'Thunfisch Salat', price: 12.00 },
        { id: 44, cat: 'salate', name: 'Poulet Salat', price: 12.00 },
        { id: 45, cat: 'salate', name: 'Döner Salat', price: 13.00 },
        { id: 46, cat: 'salate', name: 'Caesar Salat', price: 12.00 },
        // Snacks
        { id: 47, cat: 'snacks', name: 'Pommes Frites', price: 6.00 },
        { id: 48, cat: 'snacks', name: 'Pommes mit Käse', price: 8.00 },
        { id: 49, cat: 'snacks', name: 'Loaded Fries', price: 10.00 },
        { id: 50, cat: 'snacks', name: 'Chicken Nuggets (6 Stk.)', price: 7.00 },
        { id: 51, cat: 'snacks', name: 'Chicken Nuggets (9 Stk.)', price: 9.00 },
        { id: 52, cat: 'snacks', name: 'Falafel (6 Stk.)', price: 7.00 },
        { id: 53, cat: 'snacks', name: 'Zwiebelringe', price: 6.00 },
        { id: 54, cat: 'snacks', name: 'Mozzarella Sticks', price: 7.00 },
        { id: 55, cat: 'snacks', name: 'Frühlingsrollen', price: 6.00 },
        // Getränke
        { id: 56, cat: 'getraenke', name: 'Coca-Cola 0.5l', price: 4.00 },
        { id: 57, cat: 'getraenke', name: 'Coca-Cola Zero 0.5l', price: 4.00 },
        { id: 58, cat: 'getraenke', name: 'Fanta 0.5l', price: 4.00 },
        { id: 59, cat: 'getraenke', name: 'Sprite 0.5l', price: 4.00 },
        { id: 60, cat: 'getraenke', name: 'Rivella 0.5l', price: 4.00 },
        { id: 61, cat: 'getraenke', name: 'Eistee 0.5l', price: 4.00 },
        { id: 62, cat: 'getraenke', name: 'Uludag 0.5l', price: 4.00 },
        { id: 63, cat: 'getraenke', name: 'Ayran 0.25l', price: 3.50 },
        { id: 64, cat: 'getraenke', name: 'Ayran 0.5l', price: 5.00 },
        { id: 65, cat: 'getraenke', name: 'Wasser 0.5l', price: 3.00 },
        { id: 66, cat: 'getraenke', name: 'Mineral 0.5l', price: 3.00 },
        { id: 67, cat: 'getraenke', name: 'Red Bull', price: 5.00 },
        { id: 68, cat: 'getraenke', name: 'Orangensaft 0.33l', price: 4.00 },
        { id: 69, cat: 'getraenke', name: 'Apfelschorle 0.5l', price: 4.00 },
        { id: 70, cat: 'getraenke', name: 'Capri-Sun', price: 2.50 },
        { id: 71, cat: 'getraenke', name: 'Bier 0.33l', price: 5.00 },
        { id: 72, cat: 'getraenke', name: 'Bier 0.5l', price: 6.00 },
        { id: 73, cat: 'getraenke', name: 'Efes 0.5l', price: 6.00 },
        { id: 74, cat: 'getraenke', name: 'Radler 0.5l', price: 5.00 },
    ];

    // Delivery fee per town
    const deliveryFees = {
        'wattwil': 3,
        'ebnat-kappel': 5,
        'ebnat kappel': 5,
        'lichtensteig': 5,
        'bütschwil': 7,
        'buetschwil': 7,
        'ganterschwil': 7,
        'bazenheid': 9,
    };

    // Order state
    const cart = {};
    let orderType = 'pickup';
    let deliveryFee = 0;

    // ============================================================
    // INTRO ANIMATION — remove overlay after animation
    // ============================================================
    const introOverlay = document.getElementById('intro-overlay');
    if (introOverlay) {
        setTimeout(() => {
            introOverlay.style.display = 'none';
        }, 4500);
    }

    // ============================================================
    // NAVBAR
    // ============================================================
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Scroll effect
    function handleScroll() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        updateActiveNav();
    }
    window.addEventListener('scroll', handleScroll);
    handleScroll();

    // Mobile toggle
    navToggle.addEventListener('click', () => {
        const isOpen = navMenu.classList.toggle('open');
        navToggle.classList.toggle('active');
        navToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('open');
            navToggle.classList.remove('active');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });

    // Active nav link based on scroll position
    function updateActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        const scrollPos = window.scrollY + 100;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    // ============================================================
    // SCROLL ANIMATIONS (IntersectionObserver)
    // ============================================================
    const fadeElements = document.querySelectorAll('.fade-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger animation
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 50);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    fadeElements.forEach(el => observer.observe(el));

    // ============================================================
    // HERO PARTICLES
    // ============================================================
    const particlesContainer = document.getElementById('heroParticles');
    if (particlesContainer) {
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            const size = Math.random() * 4 + 2;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.bottom = '-10px';
            particle.style.animationDuration = (Math.random() * 10 + 8) + 's';
            particle.style.animationDelay = (Math.random() * 10) + 's';
            particlesContainer.appendChild(particle);
        }
    }

    // ============================================================
    // MENU TABS (Speisekarte)
    // ============================================================
    const menuTabs = document.querySelectorAll('.menu-tab');
    const menuCategories = document.querySelectorAll('.menu-category');

    menuTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const cat = tab.dataset.category;
            menuTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            menuCategories.forEach(c => {
                c.classList.remove('active');
                if (c.id === 'cat-' + cat) {
                    c.classList.add('active');
                    // Re-observe fade elements inside
                    c.querySelectorAll('.fade-up:not(.visible)').forEach(el => observer.observe(el));
                }
            });
        });
    });

    // ============================================================
    // ORDER SYSTEM
    // ============================================================

    // --- Delivery toggle ---
    const deliveryBtns = document.querySelectorAll('.delivery-btn');
    const deliveryAddressSection = document.getElementById('deliveryAddress');

    deliveryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            deliveryBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            orderType = btn.dataset.type;
            if (orderType === 'delivery') {
                deliveryAddressSection.style.display = 'block';
            } else {
                deliveryAddressSection.style.display = 'none';
                deliveryFee = 0;
            }
            updateOrderSummary();
        });
    });

    // --- Town badge click for delivery fee ---
    const townBadges = document.querySelectorAll('.town-badge');
    townBadges.forEach(badge => {
        badge.addEventListener('click', () => {
            townBadges.forEach(b => b.classList.remove('selected'));
            badge.classList.add('selected');
            deliveryFee = parseFloat(badge.dataset.fee);
            const deliveryInfo = document.getElementById('deliveryInfo');
            if (deliveryInfo) {
                deliveryInfo.style.display = 'block';
                deliveryInfo.textContent = 'Liefergebühr: CHF ' + deliveryFee.toFixed(2);
            }
            updateOrderSummary();
        });
    });

    // --- Day/Time selection ---
    const orderDaySelect = document.getElementById('orderDay');
    const orderTimeSelect = document.getElementById('orderTime');
    const dayNames = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];

    function populateDays() {
        orderDaySelect.innerHTML = '';
        const today = new Date();
        for (let i = 0; i < 7; i++) {
            const d = new Date(today);
            d.setDate(today.getDate() + i);
            const dayOfWeek = d.getDay();
            // Skip Sunday (0)
            if (dayOfWeek === 0) continue;
            const option = document.createElement('option');
            const dateStr = d.toLocaleDateString('de-CH', { day: '2-digit', month: '2-digit', year: 'numeric' });
            const label = i === 0 ? 'Heute' : (i === 1 ? 'Morgen' : dayNames[dayOfWeek]);
            option.value = dateStr;
            option.textContent = label + ' — ' + dateStr;
            option.dataset.dayOfWeek = dayOfWeek;
            orderDaySelect.appendChild(option);
        }
        populateTimes();
    }

    function populateTimes() {
        orderTimeSelect.innerHTML = '';
        const now = new Date();
        const selectedOption = orderDaySelect.options[orderDaySelect.selectedIndex];
        if (!selectedOption) return;

        const isToday = selectedOption.textContent.startsWith('Heute');
        const startHour = 10;
        const endHour = 21;

        for (let h = startHour; h < endHour; h++) {
            for (let m = 0; m < 60; m += 15) {
                // If today, skip past times (add 30 min buffer)
                if (isToday) {
                    const slotTime = new Date(now);
                    slotTime.setHours(h, m, 0, 0);
                    if (slotTime.getTime() < now.getTime() + 30 * 60 * 1000) continue;
                }
                const option = document.createElement('option');
                const timeStr = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');
                option.value = timeStr;
                option.textContent = timeStr + ' Uhr';
                orderTimeSelect.appendChild(option);
            }
        }

        // If no times available
        if (orderTimeSelect.options.length === 0) {
            const option = document.createElement('option');
            option.textContent = 'Keine Zeiten verfügbar';
            option.disabled = true;
            orderTimeSelect.appendChild(option);
        }
    }

    orderDaySelect.addEventListener('change', populateTimes);
    populateDays();

    // --- Build order items list ---
    const orderItemsList = document.getElementById('orderItemsList');
    const orderCatTabs = document.querySelectorAll('.order-cat-tab');

    function renderOrderItems(filterCat) {
        orderItemsList.innerHTML = '';
        const items = filterCat === 'all' ? menuData : menuData.filter(i => i.cat === filterCat);
        items.forEach(item => {
            const qty = cart[item.id] || 0;
            const div = document.createElement('div');
            div.className = 'order-item';
            div.dataset.cat = item.cat;
            div.innerHTML =
                '<div class="order-item-info">' +
                    '<span class="order-item-name">' + escapeHtml(item.name) + '</span><br>' +
                    '<span class="order-item-price">CHF ' + item.price.toFixed(2) + '</span>' +
                '</div>' +
                '<div class="order-item-controls">' +
                    '<button class="qty-btn qty-minus" data-id="' + item.id + '" type="button"' + (qty === 0 ? ' disabled' : '') + '>−</button>' +
                    '<span class="qty-value' + (qty > 0 ? ' has-items' : '') + '">' + qty + '</span>' +
                    '<button class="qty-btn qty-plus" data-id="' + item.id + '" type="button">+</button>' +
                '</div>';
            orderItemsList.appendChild(div);
        });

        // Attach listeners
        orderItemsList.querySelectorAll('.qty-plus').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = parseInt(btn.dataset.id, 10);
                cart[id] = (cart[id] || 0) + 1;
                renderOrderItems(getCurrentOrderCat());
                updateOrderSummary();
            });
        });
        orderItemsList.querySelectorAll('.qty-minus').forEach(btn => {
            btn.addEventListener('click', () => {
                const id = parseInt(btn.dataset.id, 10);
                if (cart[id] && cart[id] > 0) {
                    cart[id]--;
                    if (cart[id] === 0) delete cart[id];
                }
                renderOrderItems(getCurrentOrderCat());
                updateOrderSummary();
            });
        });
    }

    function getCurrentOrderCat() {
        const active = document.querySelector('.order-cat-tab.active');
        return active ? active.dataset.ordercat : 'all';
    }

    orderCatTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            orderCatTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderOrderItems(tab.dataset.ordercat);
        });
    });

    renderOrderItems('all');

    // --- Order summary ---
    function updateOrderSummary() {
        const summaryDiv = document.getElementById('orderSummary');
        const summaryItems = document.getElementById('summaryItems');
        const subtotalEl = document.getElementById('subtotalPrice');
        const deliveryFeeLineEl = document.getElementById('deliveryFeeLine');
        const deliveryFeeEl = document.getElementById('deliveryFeePrice');
        const totalEl = document.getElementById('totalPrice');

        const itemIds = Object.keys(cart).filter(id => cart[id] > 0);
        if (itemIds.length === 0) {
            summaryDiv.style.display = 'none';
            return;
        }

        summaryDiv.style.display = 'block';
        summaryItems.innerHTML = '';
        let subtotal = 0;

        itemIds.forEach(id => {
            const item = menuData.find(i => i.id === parseInt(id, 10));
            if (!item) return;
            const qty = cart[id];
            const lineTotal = item.price * qty;
            subtotal += lineTotal;
            const div = document.createElement('div');
            div.className = 'summary-item';
            div.innerHTML =
                '<span>' + qty + '× ' + escapeHtml(item.name) + '</span>' +
                '<span>CHF ' + lineTotal.toFixed(2) + '</span>';
            summaryItems.appendChild(div);
        });

        subtotalEl.textContent = 'CHF ' + subtotal.toFixed(2);

        if (orderType === 'delivery' && deliveryFee > 0) {
            deliveryFeeLineEl.style.display = 'flex';
            deliveryFeeEl.textContent = 'CHF ' + deliveryFee.toFixed(2);
        } else {
            deliveryFeeLineEl.style.display = 'none';
        }

        const total = subtotal + (orderType === 'delivery' ? deliveryFee : 0);
        totalEl.textContent = 'CHF ' + total.toFixed(2);
    }

    // --- Submit order ---
    const submitBtn = document.getElementById('submitOrder');
    const orderModal = document.getElementById('orderModal');
    const closeModalBtn = document.getElementById('closeModal');
    const modalOrderType = document.getElementById('modalOrderType');

    submitBtn.addEventListener('click', () => {
        const nameInput = document.getElementById('orderName');
        const phoneInput = document.getElementById('orderPhone');

        if (!nameInput.value.trim()) {
            nameInput.style.borderColor = '#e74c3c';
            nameInput.focus();
            return;
        }
        nameInput.style.borderColor = '';

        if (!phoneInput.value.trim()) {
            phoneInput.style.borderColor = '#e74c3c';
            phoneInput.focus();
            return;
        }
        phoneInput.style.borderColor = '';

        if (Object.keys(cart).filter(id => cart[id] > 0).length === 0) return;

        // Show modal
        modalOrderType.textContent = orderType === 'delivery' ? 'Lieferung' : 'Abholung';
        orderModal.classList.add('visible');
    });

    closeModalBtn.addEventListener('click', () => {
        orderModal.classList.remove('visible');
        // Reset order
        Object.keys(cart).forEach(k => delete cart[k]);
        document.getElementById('orderName').value = '';
        document.getElementById('orderPhone').value = '';
        document.getElementById('orderNotes').value = '';
        renderOrderItems(getCurrentOrderCat());
        updateOrderSummary();
    });

    // Close modal on overlay click
    orderModal.addEventListener('click', (e) => {
        if (e.target === orderModal) {
            closeModalBtn.click();
        }
    });

    // ============================================================
    // UTILITY
    // ============================================================
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

});
