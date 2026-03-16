// ===== NÓMADA - SISTEMA PREMIUM CON ANIMACIONES =====

// Configuración global
const CONFIG = {
    DEBUG: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
    ANIMATIONS: true,
    PARTICLES_COUNT: 30,
    NOTIFICATION_DURATION: 4000
};

// Estado de la aplicación
const AppState = {
    currentCategory: null,
    currentProvince: null,
    particlesInitialized: false
};

// ===== FUNCIONES GLOBALES (definidas primero) =====
window.closeDestinosSection = function() {
    const section = document.getElementById('destinos-provincia');
    if (section) {
        addAnimation(section, 'fadeOut', () => {
            section.classList.add('hidden');
            const categorias = document.getElementById('categorias');
            if (categorias) {
                categorias.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
};

window.showNotification = function(message, type = 'info') {
    const container = document.getElementById('notifications-container') || createNotificationContainer();
    
    const notification = document.createElement('div');
    notification.className = `notification ${type} animate-slide-up`;
    notification.innerHTML = `
        <div class="flex items-center p-3 rounded-lg bg-white shadow-lg border-l-4 ${getNotificationBorder(type)} hover:scale-105 transition-transform">
            <i class="${getNotificationIcon(type)} text-base mr-2"></i>
            <span class="text-sm text-gray-700">${message}</span>
            <button class="ml-3 text-gray-400 hover:text-gray-600 hover:rotate-90 transition-transform" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times text-xs"></i>
            </button>
        </div>
    `;
    
    container.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            addAnimation(notification, 'fadeOut', () => notification.remove());
        }
    }, CONFIG.NOTIFICATION_DURATION);
};

// ===== FUNCIONES AUXILIARES =====
function closeAllDropdowns() {
    document.querySelectorAll('.province-dropdown').forEach(dropdown => {
        dropdown.classList.add('hidden');
        const icon = dropdown.closest('.category-card')?.querySelector('.province-toggle i');
        if (icon) icon.className = 'fas fa-chevron-down';
    });
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.id = 'notifications-container';
    container.className = 'fixed top-4 right-4 z-[9999] space-y-2 max-w-sm';
    document.body.appendChild(container);
    return container;
}

function getNotificationBorder(type) {
    return {
        'info': 'border-primary-500',
        'success': 'border-secondary-500',
        'warning': 'border-amber-500',
        'error': 'border-red-500'
    }[type] || 'border-primary-500';
}

function getNotificationIcon(type) {
    return {
        'info': 'fas fa-info-circle text-primary-500',
        'success': 'fas fa-check-circle text-secondary-500',
        'warning': 'fas fa-exclamation-circle text-amber-500',
        'error': 'fas fa-times-circle text-red-500'
    }[type] || 'fas fa-info-circle text-primary-500';
}

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌿 Nómada - Sistema premium iniciado');
    
    initParticles();
    initCategoryInteractions();
    initProvinceSelection();
    initCloseDestinos();
    initSmoothScroll();
    initBackToTop();
    initImageOptimization();
    initNotifications();
    initHoverEffects();
    
    if (CONFIG.DEBUG) {
        console.log('🔧 Modo desarrollo activado');
    }
});

// ===== PARTÍCULAS =====
function initParticles() {
    const particlesContainer = document.getElementById('hero-particles');
    if (!particlesContainer || AppState.particlesInitialized) return;
    
    for (let i = 0; i < CONFIG.PARTICLES_COUNT; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        
        const colors = ['#1A3B4F', '#4A7C59', '#FFFFFF'];
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.animationDuration = `${Math.random() * 10 + 15}s`;
        
        particlesContainer.appendChild(particle);
    }
    
    AppState.particlesInitialized = true;
}

// ===== INTERACCIONES DE CATEGORÍAS =====
function initCategoryInteractions() {
    document.addEventListener('click', function(e) {
        const toggleBtn = e.target.closest('.province-toggle');
        
        if (toggleBtn) {
            e.preventDefault();
            e.stopPropagation();
            
            const card = toggleBtn.closest('.category-card');
            const dropdown = card.querySelector('.province-dropdown');
            const icon = toggleBtn.querySelector('i');
            
            document.querySelectorAll('.province-dropdown').forEach(d => {
                if (d !== dropdown) {
                    d.classList.add('hidden');
                    const otherIcon = d.closest('.category-card')?.querySelector('.province-toggle i');
                    if (otherIcon) otherIcon.className = 'fas fa-chevron-down';
                }
            });
            
            const isHidden = dropdown.classList.toggle('hidden');
            
            if (isHidden) {
                icon.className = 'fas fa-chevron-down';
            } else {
                icon.className = 'fas fa-chevron-up';
                addAnimation(dropdown, 'slideDown');
            }
        }
    });
    
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.category-card') && !e.target.closest('.province-dropdown')) {
            closeAllDropdowns();
        }
    });
}

// ===== SELECCIÓN DE PROVINCIAS =====
function initProvinceSelection() {
    document.addEventListener('click', function(e) {
        const provinceBtn = e.target.closest('.province-btn');
        
        if (provinceBtn) {
            e.preventDefault();
            e.stopPropagation();
            
            const category = provinceBtn.getAttribute('data-category');
            const province = provinceBtn.getAttribute('data-province');
            
            AppState.currentCategory = category;
            AppState.currentProvince = province;
            
            showDestinosForProvince(category, province);
            closeAllDropdowns();
        }
    });
}

// ===== MOSTRAR DESTINOS POR PROVINCIA =====
function showDestinosForProvince(category, province) {
    const section = document.getElementById('destinos-provincia');
    const grid = document.getElementById('grid-destinos');
    const title = document.getElementById('titulo-provincia');
    const description = document.getElementById('descripcion-provincia');
    
    if (!section || !grid || !title || !description) return;
    
    const destinos = window.destinosData?.[category]?.[province] || [];
    const nombreProvincia = translateProvince(province);
    const nombreCategoria = translateCategory(category);
    
    title.textContent = `${nombreCategoria} en ${nombreProvincia}`;
    description.textContent = `${destinos.length} experiencias disponibles`;
    
    grid.innerHTML = '';
    
    if (destinos.length === 0) {
        grid.innerHTML = createEmptyState();
    } else {
        destinos.forEach((destino, index) => {
            const card = createDestinoCard(destino, index);
            grid.appendChild(card);
            addAnimation(card, 'fadeIn');
        });
    }
    
    section.classList.remove('hidden');
    addAnimation(section, 'slideUp');
    
    setTimeout(() => {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// ===== CREAR CARD DE DESTINO =====
function createDestinoCard(destino, index) {
    const precioFormateado = new Intl.NumberFormat('es-CR', {
        style: 'currency',
        currency: 'CRC',
        minimumFractionDigits: 0
    }).format(destino.precio);
    
    const card = document.createElement('div');
    card.className = 'category-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    card.innerHTML = `
        <div class="relative h-48 overflow-hidden">
            <img src="${destino.imagen}" 
                 alt="${destino.nombre}"
                 class="w-full h-full object-cover hover:scale-110 transition-transform duration-700"
                 loading="lazy"
                 onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop'">
            <div class="absolute inset-0 bg-gradient-to-t from-black/30"></div>
            
            ${destino.destacado ? `
            <div class="absolute top-3 left-3">
                <span class="px-2 py-1 rounded-full bg-secondary-500 text-white text-xs font-medium animate-pulse">Destacado</span>
            </div>
            ` : ''}
            
            <div class="absolute top-3 right-3 bg-white/90 px-2 py-1 rounded-full flex items-center shadow-sm hover:scale-110 transition-transform">
                <i class="fas fa-star text-amber-400 mr-1 text-xs"></i>
                <span class="text-gray-700 font-semibold text-xs">${destino.rating}</span>
            </div>
        </div>
        
        <div class="p-4">
            <h3 class="font-semibold text-gray-800 mb-1 hover:text-primary-500 transition-colors">${destino.nombre}</h3>
            <p class="text-gray-500 text-xs mb-3">${destino.descripcion}</p>
            
            <div class="flex items-center justify-between pt-2 border-t border-gray-100">
                <div>
                    <span class="font-bold text-primary-600 text-base">${precioFormateado}</span>
                    <span class="text-gray-400 text-xs ml-1">/ persona</span>
                </div>
                
                <a href="/destinos/${destino.id}" 
                   class="inline-block px-3 py-1.5 rounded-full bg-primary-500 text-white text-xs font-medium hover:bg-primary-600 transition-all duration-300 shadow-sm hover:shadow-md hover:scale-105">
                    Ver detalles
                </a>
            </div>
        </div>
    `;
    
    return card;
}

// ===== ESTADO VACÍO =====
function createEmptyState() {
    return `
        <div class="col-span-full text-center py-10 animate-fade-in">
            <i class="fas fa-map-marker-alt text-3xl text-gray-300 mb-3 animate-bounce"></i>
            <h3 class="text-lg font-medium text-gray-700 mb-2">No hay destinos disponibles</h3>
            <p class="text-sm text-gray-500 mb-4">Próximamente agregaremos más experiencias.</p>
            <button onclick="window.closeDestinosSection()" class="px-4 py-2 rounded-full bg-primary-500 text-white text-sm hover:bg-primary-600 transition-all duration-300 hover:scale-105">
                Volver a categorías
            </button>
        </div>
    `;
}

// ===== CERRAR SECCIÓN DE DESTINOS =====
function initCloseDestinos() {
    const closeBtn = document.getElementById('cerrar-destinos');
    if (closeBtn) {
        closeBtn.addEventListener('click', window.closeDestinosSection);
    }
}

// ===== SCROLL SUAVE =====
function initSmoothScroll() {
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="#"]');
        if (!link) return;
        
        const href = link.getAttribute('href');
        if (href === '#' || href === '#!') return;
        
        const target = document.querySelector(href);
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
}

// ===== BACK TO TOP =====
function initBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            backToTopBtn.classList.remove('hidden');
            backToTopBtn.classList.add('flex', 'animate-bounce');
        } else {
            backToTopBtn.classList.add('hidden');
            backToTopBtn.classList.remove('flex', 'animate-bounce');
        }
    });
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===== OPTIMIZACIÓN DE IMÁGENES =====
function initImageOptimization() {
    document.addEventListener('error', function(e) {
        if (e.target.tagName === 'IMG') {
            e.target.src = 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=300&fit=crop';
        }
    }, true);
}

// ===== NOTIFICACIONES =====
function initNotifications() {
    // La función showNotification ya está definida globalmente
}

// ===== EFECTOS HOVER =====
function initHoverEffects() {
    document.querySelectorAll('.category-card, .testimonial-card, .stat-card').forEach(el => {
        el.addEventListener('mouseenter', () => {
            el.classList.add('hover-scale');
        });
        el.addEventListener('mouseleave', () => {
            el.classList.remove('hover-scale');
        });
    });
}

// ===== ANIMACIONES =====
function addAnimation(element, animation, callback) {
    if (!CONFIG.ANIMATIONS) {
        if (callback) callback();
        return;
    }
    
    element.classList.add(`animate-${animation}`);
    
    const onAnimationEnd = () => {
        element.classList.remove(`animate-${animation}`);
        if (callback) callback();
    };
    
    element.addEventListener('animationend', onAnimationEnd, { once: true });
    element.addEventListener('webkitAnimationEnd', onAnimationEnd, { once: true });
}

// ===== TRADUCCIONES =====
function translateProvince(code) {
    const map = {
        'guanacaste': 'Guanacaste',
        'limon': 'Limón',
        'puntarenas': 'Puntarenas',
        'alajuela': 'Alajuela',
        'cartago': 'Cartago'
    };
    return map[code] || code;
}

function translateCategory(code) {
    const map = {
        'playas': 'Playas',
        'parques': 'Parques Nacionales',
        'aventura': 'Aventura',
        'termales': 'Aguas Termales'
    };
    return map[code] || code;
}

// ===== POLYFILLS =====
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