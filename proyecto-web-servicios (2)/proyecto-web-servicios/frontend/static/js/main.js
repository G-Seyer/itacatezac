const navbar = document.getElementById("navbar");
const menuToggle = document.getElementById("menu-toggle");
const navContenido = document.getElementById("nav-contenido");
const dropdowns = document.querySelectorAll(".dropdown");
const navLinks = document.querySelectorAll(".nav-links a, .nav-cta a");

/* ============================= */
/* NAVBAR SCROLL */
/* ============================= */
window.addEventListener("scroll", () => {
    if (navbar && window.scrollY > 20) {
        navbar.classList.add("scrolled");
    } else if (navbar) {
        navbar.classList.remove("scrolled");
    }
});

/* ============================= */
/* MENÚ MÓVIL */
/* ============================= */
function abrirCerrarMenu() {
    if (!menuToggle || !navContenido) return;

    menuToggle.classList.toggle("activo");
    navContenido.classList.toggle("activo");
    document.body.classList.toggle("menu-abierto");
}

function cerrarMenu() {
    if (menuToggle && navContenido) {
        menuToggle.classList.remove("activo");
        navContenido.classList.remove("activo");
        document.body.classList.remove("menu-abierto");
    }

    dropdowns.forEach((dropdown) => {
        dropdown.classList.remove("activo");
    });
}

if (menuToggle && navContenido) {
    menuToggle.addEventListener("click", abrirCerrarMenu);
}

/* ============================= */
/* DROPDOWNS EN MÓVIL */
/* ============================= */
dropdowns.forEach((dropdown) => {
    const enlacePrincipal = dropdown.querySelector(":scope > a");
    const menuInterno = dropdown.querySelector(".dropdown-menu");

    if (enlacePrincipal && menuInterno) {
        enlacePrincipal.addEventListener("click", (e) => {
            if (window.innerWidth <= 860) {
                e.preventDefault();

                dropdowns.forEach((otroDropdown) => {
                    if (otroDropdown !== dropdown) {
                        otroDropdown.classList.remove("activo");
                    }
                });

                dropdown.classList.toggle("activo");
            }
        });
    }
});

/* ============================= */
/* CERRAR MENÚ MÓVIL AL NAVEGAR */
/* ============================= */
navLinks.forEach((link) => {
    link.addEventListener("click", () => {
        if (window.innerWidth <= 860) {
            const estaEnDropdownPrincipal = link.parentElement.classList.contains("dropdown");
            const estaEnSubmenu = link.closest(".dropdown-menu");

            if (!estaEnDropdownPrincipal || estaEnSubmenu) {
                cerrarMenu();
            }
        }
    });
});

window.addEventListener("resize", () => {
    if (window.innerWidth > 860) {
        cerrarMenu();
    }
});

/* ============================= */
/* CARRUSEL HERO */
/* ============================= */
const heroSlides = document.querySelectorAll(".hero-carousel .carousel-slide");
const heroIndicators = document.querySelectorAll(".hero-carousel .indicator");
const prevBtn = document.getElementById("carousel-prev");
const nextBtn = document.getElementById("carousel-next");

let currentHeroSlide = 0;
let autoHeroSlide = null;

function mostrarHeroSlide(index) {
    if (!heroSlides.length) return;

    heroSlides.forEach((slide, i) => {
        slide.classList.toggle("activo", i === index);
    });

    heroIndicators.forEach((indicator, i) => {
        indicator.classList.toggle("activo", i === index);
    });

    currentHeroSlide = index;
}

function siguienteHeroSlide() {
    if (!heroSlides.length) return;
    const nextIndex = (currentHeroSlide + 1) % heroSlides.length;
    mostrarHeroSlide(nextIndex);
}

function anteriorHeroSlide() {
    if (!heroSlides.length) return;
    const prevIndex = (currentHeroSlide - 1 + heroSlides.length) % heroSlides.length;
    mostrarHeroSlide(prevIndex);
}

function iniciarAutoHeroSlide() {
    if (!heroSlides.length) return;

    autoHeroSlide = setInterval(() => {
        siguienteHeroSlide();
    }, 4500);
}

function reiniciarAutoHeroSlide() {
    if (!heroSlides.length) return;

    clearInterval(autoHeroSlide);
    iniciarAutoHeroSlide();
}

if (heroSlides.length > 0) {
    if (prevBtn) {
        prevBtn.addEventListener("click", () => {
            anteriorHeroSlide();
            reiniciarAutoHeroSlide();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener("click", () => {
            siguienteHeroSlide();
            reiniciarAutoHeroSlide();
        });
    }

    heroIndicators.forEach((indicator, index) => {
        indicator.addEventListener("click", () => {
            mostrarHeroSlide(index);
            reiniciarAutoHeroSlide();
        });
    });

    iniciarAutoHeroSlide();
}

/* ============================= */
/* TABS + CARRUSEL SOLUCIONES */
/* ============================= */
const tabsSoluciones = document.querySelectorAll(".tab-solucion");
const slidesSoluciones = document.querySelectorAll(".slide-solucion");

let currentSolucionIndex = 0;
let autoSoluciones = null;

function limpiarEstadosSoluciones() {
    slidesSoluciones.forEach((slide) => {
        slide.classList.remove("activo", "preview-left", "preview-right");
    });
}

function activarSolucionPorIndice(index) {
    if (!slidesSoluciones.length || !tabsSoluciones.length) return;

    const total = slidesSoluciones.length;
    const currentIndex = ((index % total) + total) % total;
    const prevIndex = (currentIndex - 1 + total) % total;
    const nextIndex = (currentIndex + 1) % total;

    limpiarEstadosSoluciones();

    slidesSoluciones[currentIndex].classList.add("activo");

    if (window.innerWidth > 860) {
        slidesSoluciones[prevIndex].classList.add("preview-left");
        slidesSoluciones[nextIndex].classList.add("preview-right");
    }

    tabsSoluciones.forEach((tab, i) => {
        tab.classList.toggle("activo", i === currentIndex);
    });

    currentSolucionIndex = currentIndex;
}

function siguienteSolucion() {
    if (!slidesSoluciones.length) return;
    activarSolucionPorIndice(currentSolucionIndex + 1);
}

function iniciarAutoSoluciones() {
    if (!slidesSoluciones.length) return;

    autoSoluciones = setInterval(() => {
        siguienteSolucion();
    }, 2800);
}

function reiniciarAutoSoluciones() {
    if (!slidesSoluciones.length) return;

    clearInterval(autoSoluciones);
    iniciarAutoSoluciones();
}

tabsSoluciones.forEach((tab, index) => {
    tab.addEventListener("click", () => {
        activarSolucionPorIndice(index);
        reiniciarAutoSoluciones();
    });
});

if (tabsSoluciones.length && slidesSoluciones.length) {
    activarSolucionPorIndice(0);
    iniciarAutoSoluciones();
}

window.addEventListener("resize", () => {
    if (slidesSoluciones.length && tabsSoluciones.length) {
        activarSolucionPorIndice(currentSolucionIndex);
    }
});