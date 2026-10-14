// ========================================
// TaskBoard - JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    initClock();
    initSidebar();
    initProgressRing();
    initCardAnimations();
});

// --- Live Clock ---
function initClock() {
    const clockEl = document.getElementById('clock');
    if (!clockEl) return;

    function updateClock() {
        const now = new Date();
        clockEl.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
        });
    }

    updateClock();
    setInterval(updateClock, 1000);
}

// --- Sidebar Toggle ---
function initSidebar() {
    const toggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');

    if (!toggle || !sidebar) return;

    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
    });

    // Close sidebar on click outside (mobile)
    document.addEventListener('click', (e) => {
        if (
            sidebar.classList.contains('open') &&
            !sidebar.contains(e.target) &&
            !toggle.contains(e.target)
        ) {
            sidebar.classList.remove('open');
        }
    });
}

// --- Progress Ring ---
function initProgressRing() {
    const ring = document.querySelector('.progress-ring-fill');
    if (!ring) return;

    const total = parseInt(ring.dataset.total) || 0;
    const done = parseInt(ring.dataset.done) || 0;
    const circumference = 2 * Math.PI * 52; // r=52
    const percent = total > 0 ? done / total : 0;
    const offset = circumference * (1 - percent);

    // Animate after a small delay
    ring.style.strokeDasharray = circumference;
    ring.style.strokeDashoffset = circumference;

    requestAnimationFrame(() => {
        setTimeout(() => {
            ring.style.strokeDashoffset = offset;
        }, 200);
    });
}

// --- Card Stagger Animation ---
function initCardAnimations() {
    const cards = document.querySelectorAll('.task-card, .stat-card');
    cards.forEach((card, i) => {
        card.style.animationDelay = `${i * 0.05}s`;
    });
}
