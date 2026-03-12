/* ============================================
   LuxeStay - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initMobileMenu();
    initScrollAnimations();
    initChatbot();
    initAlertDismiss();
    initSmoothScroll();
});

/* ---- Sticky Navbar ---- */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll);
    handleScroll(); // Initial check
}

/* ---- Mobile Menu ---- */
function initMobileMenu() {
    const toggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');
    if (!toggle || !navLinks) return;

    toggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const icon = toggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    });

    // Close menu on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            const icon = toggle.querySelector('i');
            icon.classList.add('fa-bars');
            icon.classList.remove('fa-times');
        });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!navLinks.contains(e.target) && !toggle.contains(e.target)) {
            navLinks.classList.remove('active');
        }
    });
}

/* ---- Scroll Animations ---- */
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.card, .glass-card, .testimonial-card, .menu-card, .gallery-item, .stat-card, .offer-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        observer.observe(el);
    });
}

/* ---- Chatbot ---- */
function initChatbot() {
    const toggle = document.getElementById('chatbotToggle');
    const window_el = document.getElementById('chatbotWindow');
    const input = document.getElementById('chatInput');

    if (!toggle || !window_el) return;

    toggle.addEventListener('click', () => {
        window_el.classList.toggle('active');
        if (window_el.classList.contains('active')) {
            input?.focus();
        }
    });

    // Enter key to send
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const messages = document.getElementById('chatMessages');
    if (!input || !messages) return;

    const text = input.value.trim();
    if (!text) return;

    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-message user';
    userMsg.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
    messages.appendChild(userMsg);

    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'chat-message bot typing';
    typingIndicator.innerHTML = `<div class="bubble">...</div>`;
    messages.appendChild(typingIndicator);
    messages.scrollTop = messages.scrollHeight;

    try {
        const response = await fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        typingIndicator.remove();

        const botMsg = document.createElement('div');
        botMsg.className = 'chat-message bot';
        botMsg.innerHTML = `<div class="bubble">${data.reply}</div>`;
        messages.appendChild(botMsg);
    } catch (error) {
        typingIndicator.remove();
        const botMsg = document.createElement('div');
        botMsg.className = 'chat-message bot';
        botMsg.innerHTML = `<div class="bubble">${getBotResponse(text)}</div>`; // Fallback to local
        messages.appendChild(botMsg);
    }

    messages.scrollTop = messages.scrollHeight;
}

function getBotResponse(text) {
    const lower = text.toLowerCase();

    if (lower.includes('room') || lower.includes('book') || lower.includes('stay')) {
        return '🛏️ We have luxurious Standard, Deluxe, and Suite rooms available. <br><br>Would you like to <a href="/rooms/" style="color:var(--primary);font-weight:600;">browse our rooms</a> or make a booking?';
    }
    if (lower.includes('restaurant') || lower.includes('food') || lower.includes('menu') || lower.includes('dine') || lower.includes('eat')) {
        return '🍽️ Our restaurant offers an exquisite menu with both vegetarian and non-vegetarian options. <br><br>Check out our <a href="/restaurant/" style="color:var(--primary);font-weight:600;">digital menu</a>!';
    }
    if (lower.includes('table') || lower.includes('reservation') || lower.includes('reserve')) {
        return '📅 I can help you reserve a table! Please visit our <a href="/bookings/table/" style="color:var(--primary);font-weight:600;">table reservation page</a> to book your spot.';
    }
    if (lower.includes('price') || lower.includes('cost') || lower.includes('rate')) {
        return '💰 Our room rates start from ₹4,999 per night for Standard rooms, ₹8,999 for Deluxe, and ₹14,999 for Suites. Special offers may apply!';
    }
    if (lower.includes('contact') || lower.includes('phone') || lower.includes('email')) {
        return '📞 You can reach us at:<br>Phone: +91 98765 43210<br>Email: info@luxestay.com<br><br>Or visit our <a href="/contact/" style="color:var(--primary);font-weight:600;">contact page</a>.';
    }
    if (lower.includes('check') && (lower.includes('in') || lower.includes('out'))) {
        return '🕐 Check-in time is 2:00 PM and check-out time is 12:00 PM. Early check-in and late check-out can be arranged upon request.';
    }
    if (lower.includes('hello') || lower.includes('hi') || lower.includes('hey')) {
        return '👋 Hello! Welcome to LuxeStay. How can I assist you today? I can help with room bookings, restaurant reservations, or answer any questions!';
    }
    if (lower.includes('thank')) {
        return '😊 You\'re welcome! Is there anything else I can help you with?';
    }

    return '🤔 I\'d be happy to help! Could you please tell me more about what you\'re looking for? I can assist with:<br><br>🛏️ Room bookings<br>🍽️ Restaurant & menu<br>📅 Table reservations<br>💰 Pricing info<br>📞 Contact details';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/* ---- Alert Auto-dismiss ---- */
function initAlertDismiss() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert, index) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(50px)';
            setTimeout(() => alert.remove(), 500);
        }, 4000 + (index * 500));
    });
}

/* ---- Smooth Scroll ---- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/* ---- Counter Animation ---- */
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                counter.textContent = target.toLocaleString();
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current).toLocaleString();
            }
        }, 16);
    });
}

/* ---- Lazy Loading Images ---- */
if ('IntersectionObserver' in window) {
    const imgObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                imgObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imgObserver.observe(img);
    });
}

// Heatmap analytics tracker mock
document.addEventListener('click', (e) => {
    const heatmapData = JSON.parse(localStorage.getItem('heatmap_data') || '[]');
    heatmapData.push({
        x: e.pageX,
        y: e.pageY,
        path: window.location.pathname,
        time: new Date().toISOString()
    });
    // Keep only last 100 clicks
    if (heatmapData.length > 100) heatmapData.shift();
    localStorage.setItem('heatmap_data', JSON.stringify(heatmapData));
});

console.log('LuxeStay Premium features initialized.');
