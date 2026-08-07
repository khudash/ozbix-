
// ===========

function openMenu() {
    document.getElementById("sideMenu").classList.remove("-translate-x-full");

    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.classList.add("opacity-0", "pointer-events-none");
    }
}
function closeMenu() {
    document.getElementById("sideMenu").classList.add("-translate-x-full");

    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.classList.remove("opacity-0", "pointer-events-none");
    }
}

const swiper = new Swiper(".myServices", {
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
        768: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
        1400: { slidesPerView: 4 },
    },
});
