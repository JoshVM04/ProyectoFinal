// ===== TRIP506 - SISTEMA ULTRA PREMIUM =====

// Configuración global
const CONFIG = {
    DEBUG: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
    ANIMATIONS: true,
    PRELOADER_DELAY: 1000,
    PARTICLES_COUNT: 50,
    NOTIFICATION_DURATION: 4000
};

// Estado de la aplicación
const AppState = {
    currentCategory: null,
    currentProvince: null,
    menuOpen: false,
    preloaderVisible: true,
    particlesInitialized: false
};

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Trip506 - Sistema premium iniciado');
    
    // Inicializar componentes
    initPreloader();
    initParticles();
    initMobileMenu();
    initCategoryInteractions();
    initProvinceSelection();
    initCloseDestinos();
    initSmoothScroll();
    initBackToTop();
    initImageOptimization();
    initNotifications();
    initCursorEffect();
    
    // Inicializar efectos especiales
    initParallaxEffects();
    initIntersectionObservers();
    initLazyLoading();
    
    // Debug mode
    if (CONFIG.DEBUG) {
        console.log('🔧 Modo desarrollo activado');
        initDebugTools();
    }
});

// ===== PRELOADER =====
function initPreloader() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    
    // Ocultar preloader después del delay
    setTimeout(() => {
        preloader.style.opacity = '0';
        setTimeout(() => {
            preloader.style.display = 'none';
            AppState.preloaderVisible = false;
            dispatchEvent(new CustomEvent('app:loaded'));
        }, 500);
    }, CONFIG.PRELOADER_DELAY);
}

// ===== EFECTO PARTÍCULAS =====
function initParticles() {
    const particlesContainer = document.getElementById('hero-particles');
    if (!particlesContainer || AppState.particlesInitialized) return;
    
    for (let i = 0; i < CONFIG.PARTICLES_COUNT; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Posición aleatoria
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        // Tamaño aleatorio
        const size = Math.random() * 3 + 1;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Opacidad aleatoria
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        
        // Delay de animación aleatorio
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.animationDuration = `${Math.random() * 10 + 15}s`;
        
        particlesContainer.appendChild(particle);
    }
    
    AppState.particlesInitialized = true;
}

// ===== MENÚ MÓVIL PREMIUM =====
function initMobileMenu() {
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (!menuToggle || !mobileMenu) return;
    
    // Toggle menu
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        const isOpening = mobileMenu.classList.toggle('hidden');
        
        // Animar ícono hamburguesa
        if (isOpening) {
            menuToggle.classList.remove('active');
        } else {
            menuToggle.classList.add('active');
        }
        
        // Bloquear scroll cuando el menú está abierto
        document.body.style.overflow = isOpening ? '' : 'hidden';
        AppState.menuOpen = !isOpening;
    });
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (AppState.menuOpen && 
            !mobileMenu.contains(e.target) && 
            !menuToggle.contains(e.target)) {
            closeMobileMenu();
        }
    });
    
    // Cerrar menú al hacer clic en un enlace
    mobileMenu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            closeMobileMenu();
        });
    });
    
    // Cerrar menú con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && AppState.menuOpen) {
            closeMobileMenu();
        }
    });
    
    function closeMobileMenu() {
        mobileMenu.classList.add('hidden');
        menuToggle.classList.remove('active');
        document.body.style.overflow = '';
        AppState.menuOpen = false;
    }
}

// ===== INTERACCIONES DE CATEGORÍAS =====
function initCategoryInteractions() {
    // Toggle dropdowns de provincias
    document.addEventListener('click', function(e) {
        const toggleBtn = e.target.closest('.province-toggle-premium');
        
        if (toggleBtn) {
            e.preventDefault();
            e.stopPropagation();
            
            const card = toggleBtn.closest('.category-card-premium');
            const dropdown = card.querySelector('[data-province-dropdown]');
            const icon = toggleBtn.querySelector('i');
            
            // Cerrar otros dropdowns
            document.querySelectorAll('[data-province-dropdown]').forEach(d => {
                if (d !== dropdown) {
                    d.classList.add('hidden');
                    const otherIcon = d.closest('.category-card-premium')?.querySelector('.province-toggle-premium i');
                    if (otherIcon) {
                        otherIcon.className = 'fas fa-chevron-down';
                    }
                }
            });
            
            // Toggle dropdown actual
            const isHidden = dropdown.classList.toggle('hidden');
            
            // Animar ícono
            if (isHidden) {
                icon.className = 'fas fa-chevron-down';
            } else {
                icon.className = 'fas fa-chevron-up';
                animateElement(dropdown, 'slideDown');
            }
        }
    });
    
    // Cerrar dropdowns al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.category-card-premium') && !e.target.closest('[data-province-dropdown]')) {
            closeAllDropdowns();
        }
    });
    
    function closeAllDropdowns() {
        document.querySelectorAll('[data-province-dropdown]').forEach(dropdown => {
            dropdown.classList.add('hidden');
            const icon = dropdown.closest('.category-card-premium')?.querySelector('.province-toggle-premium i');
            if (icon) {
                icon.className = 'fas fa-chevron-down';
            }
        });
    }
}

// ===== SELECCIÓN DE PROVINCIAS =====
function initProvinceSelection() {
    document.addEventListener('click', function(e) {
        const provinceBtn = e.target.closest('.province-btn-premium');
        
        if (provinceBtn) {
            e.preventDefault();
            e.stopPropagation();
            
            const category = provinceBtn.getAttribute('data-category');
            const province = provinceBtn.getAttribute('data-province');
            
            // Actualizar estado
            AppState.currentCategory = category;
            AppState.currentProvince = province;
            
            // Mostrar destinos
            showDestinosForProvince(category, province);
            
            // Cerrar todos los dropdowns
            closeAllDropdowns();
            
            // Trackear evento (para analytics)
            trackEvent('province_selected', { category, province });
        }
    });
}

// ===== MOSTRAR DESTINOS POR PROVINCIA =====
function showDestinosForProvince(category, province) {
    const section = document.querySelector('[data-destinos-section]');
    const grid = document.getElementById('grid-destinos');
    const title = document.getElementById('titulo-provincia');
    const description = document.getElementById('descripcion-provincia');
    
    if (!section || !grid || !title || !description) {
        console.error('❌ Elementos de destino no encontrados');
        return;
    }
    
    // Obtener destinos
    const destinos = window.destinosData?.[category]?.[province] || [];
    
    // Traducir nombres
    const nombreProvincia = translateProvince(province);
    const nombreCategoria = translateCategory(category);
    
    // Actualizar UI
    title.textContent = `${nombreCategoria} en ${nombreProvincia}`;
    description.textContent = `${destinos.length} destinos únicos disponibles`;
    
    // Limpiar grid
    grid.innerHTML = '';
    
    if (destinos.length === 0) {
        // Mostrar estado vacío
        grid.innerHTML = createEmptyState();
    } else {
        // Crear cards de destinos
        destinos.forEach((destino, index) => {
            const card = createDestinoCard(destino, index);
            grid.appendChild(card);
        });
    }
    
    // Mostrar sección
    section.classList.remove('hidden');
    animateElement(section, 'slideUp');
    
    // Scroll a la sección
    setTimeout(() => {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
    
    // Mostrar notificación
    showNotification(`📍 Mostrando ${destinos.length} destinos en ${nombreProvincia}`, 'success');
}

// ===== CREAR CARD DE DESTINO =====
function createDestinoCard(destino, index) {
    const precioFormateado = new Intl.NumberFormat('es-CR', {
        style: 'currency',
        currency: 'CRC',
        minimumFractionDigits: 0
    }).format(destino.precio);
    
    const card = document.createElement('div');
    card.className = 'destino-card-premium animate-scale-in';
    card.style.animationDelay = `${index * 100}ms`;
    card.innerHTML = `
        <div class="bg-white rounded-2xl overflow-hidden border border-gray-200 hover:border-primary-500 transition-all duration-300 hover:shadow-xl group">
            <div class="relative h-56 overflow-hidden">
                <img src="${destino.imagen}" 
                     alt="${destino.nombre}"
                     class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                     loading="lazy"
                     onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'">
                <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>
                
                ${destino.destacado ? `
                <div class="absolute top-4 left-4">
                    <span class="px-3 py-1 rounded-full bg-gradient-to-r from-amber-500 to-amber-600 text-white text-xs font-bold">
                        Destacado
                    </span>
                </div>
                ` : ''}
                
                <div class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full flex items-center shadow-sm">
                    <i class="fas fa-star text-amber-400 mr-1"></i>
                    <span class="text-gray-900 font-bold">${destino.rating}</span>
                </div>
                
                <div class="absolute bottom-4 left-4">
                    <span class="px-3 py-1 rounded-full bg-white/90 backdrop-blur-sm text-gray-900 text-xs font-medium">
                        ${destino.provincia}
                    </span>
                </div>
            </div>
            
            <div class="p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-2">${destino.nombre}</h3>
                <p class="text-gray-600 text-sm mb-4">${destino.descripcion}</p>
                
                <div class="flex items-center justify-between pt-4 border-t border-gray-100">
                    <div>
                        <div class="text-2xl font-bold text-primary-600">${precioFormateado}</div>
                        <div class="text-xs text-gray-500">por persona</div>
                    </div>
                    
                    <div class="flex gap-2">
                        <button class="w-10 h-10 rounded-full bg-gray-100 hover:bg-primary-100 text-gray-600 hover:text-primary-600 flex items-center justify-center transition-colors">
                            <i class="fas fa-heart"></i>
                        </button>
                        <button class="px-4 py-2 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 text-white font-medium hover:from-primary-600 hover:to-primary-700 transition-all duration-300 shadow-md hover:shadow-lg">
                            Reservar
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// ===== ESTADO VACÍO =====
function createEmptyState() {
    return `
        <div class="md:col-span-2 lg:col-span-3 text-center py-16 animate-fade-in">
            <div class="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-r from-gray-100 to-gray-200 flex items-center justify-center">
                <i class="fas fa-map-marker-alt text-3xl text-gray-400"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-700 mb-3">No hay destinos disponibles</h3>
            <p class="text-gray-500 max-w-md mx-auto mb-6">
                Próximamente agregaremos más destinos exclusivos en esta provincia.
            </p>
            <button onclick="closeDestinosSection()" class="px-6 py-3 rounded-full bg-gradient-to-r from-primary-500 to-primary-600 text-white font-medium hover:from-primary-600 hover:to-primary-700 transition-all duration-300">
                Volver a categorías
            </button>
        </div>
    `;
}

// ===== CERRAR SECCIÓN DE DESTINOS =====
function initCloseDestinos() {
    const closeBtn = document.getElementById('cerrar-destinos');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeDestinosSection);
    }
}

function closeDestinosSection() {
    const section = document.querySelector('[data-destinos-section]');
    if (section) {
        animateElement(section, 'fadeOut', () => {
            section.classList.add('hidden');
            
            // Scroll a categorías
            setTimeout(() => {
                document.getElementById('categorias').scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 300);
        });
    }
}

// ===== SCROLL SUAVE =====
function initSmoothScroll() {
    // Interceptar clicks en enlaces internos
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="#"]');
        if (!link) return;
        
        const href = link.getAttribute('href');
        if (href === '#' || href === '#!') return;
        
        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            
            // Cerrar menú móvil si está abierto
            if (AppState.menuOpen) {
                const menuToggle = document.getElementById('mobile-menu-toggle');
                const mobileMenu = document.getElementById('mobile-menu');
                mobileMenu.classList.add('hidden');
                menuToggle.classList.remove('active');
                document.body.style.overflow = '';
                AppState.menuOpen = false;
            }
            
            // Scroll suave
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Actualizar URL sin recargar
            history.pushState(null, null, href);
        }
    });
}

// ===== BACK TO TOP =====
function initBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;
    
    // Mostrar/ocultar botón según scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            backToTopBtn.classList.remove('hidden');
            animateElement(backToTopBtn, 'slideUp');
        } else {
            backToTopBtn.classList.add('hidden');
        }
    });
    
    // Scroll to top
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ===== OPTIMIZACIÓN DE IMÁGENES =====
function initImageOptimization() {
    // Lazy loading nativo con polyfill para navegadores antiguos
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    } else {
        // Polyfill para lazy loading
        import('https://cdn.jsdelivr.net/npm/vanilla-lazyload@17.8.3/dist/lazyload.min.js')
            .then(() => {
                new LazyLoad({
                    elements_selector: "img[loading='lazy']"
                });
            });
    }
    
    // Manejo de errores de imágenes
    document.addEventListener('error', function(e) {
        if (e.target.tagName === 'IMG') {
            console.warn('⚠️ Error cargando imagen:', e.target.src);
            
            // Determinar tipo de fallback
            const fallbackMap = {
                'playas': 'beach',
                'parques': 'park',
                'aventura': 'adventure',
                'termales': 'spa'
            };
            
            let fallbackType = 'beach';
            const card = e.target.closest('[data-category]');
            if (card) {
                const category = card.getAttribute('data-category');
                fallbackType = fallbackMap[category] || 'beach';
            }
            
            const unsplashUrls = {
                'beach': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'park': 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'adventure': 'https://images.unsplash.com/photo-1536152471326-6428c2f4e7e1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80',
                'spa': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'
            };
            
            e.target.src = unsplashUrls[fallbackType];
            e.target.classList.add('image-fallback');
        }
    }, true);
}

// ===== EFECTO CURSOR PERSONALIZADO =====
function initCursorEffect() {
    if (window.matchMedia('(pointer: fine)').matches) {
        const cursorDot = document.querySelector('.cursor-dot');
        const cursorRing = document.querySelector('.cursor-ring');
        
        if (!cursorDot || !cursorRing) return;
        
        let mouseX = 0, mouseY = 0;
        let dotX = 0, dotY = 0;
        let ringX = 0, ringY = 0;
        
        document.addEventListener('mousemove', function(e) {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });
        
        function animateCursor() {
            // Animación suave del dot
            dotX += (mouseX - dotX) * 0.1;
            dotY += (mouseY - dotY) * 0.1;
            
            // Animación más lenta del ring
            ringX += (mouseX - ringX) * 0.05;
            ringY += (mouseY - ringY) * 0.05;
            
            // Aplicar transformaciones
            cursorDot.style.transform = `translate(${dotX}px, ${dotY}px)`;
            cursorRing.style.transform = `translate(${ringX}px, ${ringY}px)`;
            
            requestAnimationFrame(animateCursor);
        }
        
        animateCursor();
        
        // Efectos hover
        const hoverElements = document.querySelectorAll('a, button, .category-card-premium, .province-btn-premium');
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursorDot.style.transform = 'scale(1.5)';
                cursorRing.style.transform = 'scale(1.5)';
            });
            el.addEventListener('mouseleave', () => {
                cursorDot.style.transform = 'scale(1)';
                cursorRing.style.transform = 'scale(1)';
            });
        });
    }
}

// ===== EFECTOS PARALLAX =====
function initParallaxEffects() {
    const hero = document.querySelector('.hero-section');
    if (!hero) return;
    
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    });
}

// ===== INTERSECTION OBSERVERS =====
function initIntersectionObservers() {
    // Observar elementos para animaciones
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Animaciones personalizadas según data-aos
                const aos = entry.target.getAttribute('data-aos');
                if (aos) {
                    entry.target.classList.add(`animate-${aos}`);
                }
            }
        });
    }, observerOptions);
    
    // Observar elementos
    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
}

// ===== LAZY LOADING MEJORADO =====
function initLazyLoading() {
    const lazyLoadObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                lazyLoadObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        lazyLoadObserver.observe(img);
    });
}

// ===== SISTEMA DE NOTIFICACIONES =====
function initNotifications() {
    window.showNotification = function(message, type = 'info') {
        const container = document.getElementById('notifications-container') || createNotificationContainer();
        
        const notification = document.createElement('div');
        notification.className = `notification ${type} animate-slide-up`;
        notification.innerHTML = `
            <div class="flex items-center p-4 rounded-xl bg-white shadow-2xl border-l-4 ${getNotificationBorder(type)}">
                <i class="${getNotificationIcon(type)} text-xl mr-3"></i>
                <div class="flex-1">
                    <p class="text-gray-900 font-medium">${message}</p>
                </div>
                <button class="text-gray-400 hover:text-gray-600 ml-4" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(notification);
        
        // Auto-remover
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.add('animate-fade-out');
                setTimeout(() => notification.remove(), 300);
            }
        }, CONFIG.NOTIFICATION_DURATION);
    };
    
    function createNotificationContainer() {
        const container = document.createElement('div');
        container.id = 'notifications-container';
        container.className = 'fixed top-6 right-6 z-[9999] space-y-3 max-w-sm';
        document.body.appendChild(container);
        return container;
    }
    
    function getNotificationBorder(type) {
        const borders = {
            'info': 'border-blue-500',
            'success': 'border-green-500',
            'warning': 'border-amber-500',
            'error': 'border-red-500'
        };
        return borders[type] || 'border-gray-500';
    }
    
    function getNotificationIcon(type) {
        const icons = {
            'info': 'fas fa-info-circle text-blue-500',
            'success': 'fas fa-check-circle text-green-500',
            'warning': 'fas fa-exclamation-circle text-amber-500',
            'error': 'fas fa-times-circle text-red-500'
        };
        return icons[type] || 'fas fa-info-circle text-gray-500';
    }
}

// ===== HERRAMIENTAS DE DEBUG =====
function initDebugTools() {
    console.group('🔧 Debug Information');
    console.log('App State:', AppState);
    console.log('Destinos Data:', window.destinosData);
    console.log('Config:', CONFIG);
    console.groupEnd();
    
    // Mostrar notificación de debug
    setTimeout(() => {
        showNotification('Modo desarrollo activado', 'info');
    }, 2000);
}

// ===== FUNCIONES DE UTILIDAD =====
function translateProvince(code) {
    const provinces = {
        'guanacaste': 'Guanacaste',
        'limon': 'Limón',
        'puntarenas': 'Puntarenas',
        'alajuela': 'Alajuela',
        'cartago': 'Cartago',
        'heredia': 'Heredia',
        'san-jose': 'San José'
    };
    return provinces[code] || code;
}

function translateCategory(code) {
    const categories = {
        'playas': 'Playas',
        'parques': 'Parques Nacionales',
        'aventura': 'Aventura & Ecoturismo',
        'termales': 'Aguas Termales'
    };
    return categories[code] || code;
}

function animateElement(element, animation, callback) {
    if (!CONFIG.ANIMATIONS) {
        if (callback) callback();
        return;
    }
    
    element.classList.add(`animate-${animation}`);
    
    const onAnimationEnd = () => {
        element.classList.remove(`animate-${animation}`);
        if (callback) callback();
    };
    
    // Detectar cuando termina la animación
    element.addEventListener('animationend', onAnimationEnd, { once: true });
    element.addEventListener('webkitAnimationEnd', onAnimationEnd, { once: true });
}

function trackEvent(eventName, data = {}) {
    if (CONFIG.DEBUG) {
        console.log(`📊 Event: ${eventName}`, data);
    }
    
    // Aquí podrías integrar Google Analytics, Mixpanel, etc.
    // Ejemplo: gtag('event', eventName, data);
}

// ===== POLYFILLS Y FALLBACKS =====
// Polyfill para Element.closest
if (!Element.prototype.closest) {
    Element.prototype.closest = function(s) {
        var el = this;
        do {
            if (el.matches(s)) return el;
            el = el.parentElement || el.parentNode;
        } while (el !== null && el.nodeType === 1);
        return null;
    };
}

// Polyfill para NodeList.forEach
if (window.NodeList && !NodeList.prototype.forEach) {
    NodeList.prototype.forEach = Array.prototype.forEach;
}

// ===== EXPORTAR FUNCIONES GLOBALES =====
window.closeDestinosSection = closeDestinosSection;
window.showNotification = showNotification;

// ===== PERFORMANCE MONITORING =====
window.addEventListener('load', function() {
    // Performance metrics
    if ('performance' in window) {
        const perfData = window.performance.timing;
        const loadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`⏱️  Page loaded in ${loadTime}ms`);
    }
});

// ===== ERROR HANDLING GLOBAL =====
window.addEventListener('error', function(e) {
    console.error('❌ Global error:', e.error);
    showNotification('Ocurrió un error inesperado', 'error');
});

// ===== OFFLINE SUPPORT =====
window.addEventListener('offline', function() {
    showNotification('Sin conexión a internet', 'warning');
});

window.addEventListener('online', function() {
    showNotification('Conexión restablecida', 'success');
});