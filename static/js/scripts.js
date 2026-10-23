// Ozbix IT Solutions - Global JavaScript

function openMenu() {
    const sideMenu = document.getElementById("sideMenu");
    if (sideMenu) {
        sideMenu.classList.remove("-translate-x-full");
    }

    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.classList.add("opacity-0", "pointer-events-none");
    }
}

function closeMenu() {
    const sideMenu = document.getElementById("sideMenu");
    if (sideMenu) {
        sideMenu.classList.add("-translate-x-full");
    }

    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.classList.remove("opacity-0", "pointer-events-none");
    }
}

// Universal Modal Helper Functions
function openModal(id) {
    const targetModal = (id && typeof id === 'string') ? document.getElementById(id) : document.getElementById('modal');
    if (targetModal) {
        targetModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(id) {
    const targetModal = (id && typeof id === 'string') ? document.getElementById(id) : document.getElementById('modal');
    if (targetModal) {
        targetModal.classList.add('hidden');
        document.body.style.overflow = '';
    }
}

// Global Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Backdrop click to close modal
    const modalEl = document.getElementById('modal');
    if (modalEl) {
        modalEl.addEventListener('click', function(e) {
            if (e.target === modalEl) {
                closeModal('modal');
            }
        });
    }

    // Escape key to close modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal('modal');
        }
    });

    // Swiper Carousel Initialization (only when element exists)
    if (typeof Swiper !== 'undefined' && document.querySelector(".myServices")) {
        new Swiper(".myServices", {
            slidesPerView: 4,
            spaceBetween: 25,
            loop: true,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
            breakpoints: {
                0: { slidesPerView: 1 },
                640: { slidesPerView: 2 },
                1024: { slidesPerView: 3 },
                1400: { slidesPerView: 4 },
            },
        });
    }
});
