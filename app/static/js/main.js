// ===== DATOS DE DESTINOS =====
const destinosPlayas = [
    {
        id: 1,
        nombre: "Playa Conchal",
        provincia: "Guanacaste",
        precio: 65000,
        rating: 4.9,
        thumbnail: "/static/images/destinos/thumbnails/Reserva-Conchal.jpg",
        descripcion: "Arena de conchas blancas cristalinas únicas"
    },
    {
        id: 2,
        nombre: "Playa Tamarindo",
        provincia: "Guanacaste",
        precio: 40000,
        rating: 4.8,
        thumbnail: "/static/images/destinos/thumbnails/Tamarindo-Aerial.jpg",
        descripcion: "Surf y vida nocturna vibrante en la costa del Pacífico"
    },
    {
        id: 3,
        nombre: "Playa Manuel Antonio",
        provincia: "Puntarenas",
        precio: 55000,
        rating: 4.9,
        thumbnail: "/static/images/destinos/thumbnails/playa-manuel-an.jpg",
        descripcion: "Famosa por su parque nacional y biodiversidad"
    },
    {
        id: 4,
        nombre: "Playa Santa Teresa",
        provincia: "Puntarenas",
        precio: 48000,
        rating: 4.7,
        thumbnail: "/static/images/destinos/thumbnails/santatere.400x300.jpg",
        descripcion: "Paraíso del surf con atardeceres espectaculares"
    },
    {
        id: 5,
        nombre: "Playa Punta Uva",
        provincia: "Limón",
        precio: 45000,
        rating: 4.8,
        thumbnail: "/static/images/destinos/thumbnails/aerial-Punta-Uva.jpg",
        descripcion: "Aguas cristalinas ideales para snorkel"
    },
    {
        id: 6,
        nombre: "Playa Cahuita",
        provincia: "Limón",
        precio: 35000,
        rating: 4.7,
        thumbnail: "/static/images/destinos/thumbnails/cahuita.400x300.jpg",
        descripcion: "Arrecife de coral y parque nacional"
    }
];

// ===== VARIABLES GLOBALES =====
let provinciaActual = 'todas';
let destinoSeleccionadoId = null;
let sortBy = 'popularidad';

// ===== DOM ELEMENTS =====
const destinosGrid = document.getElementById('destinosGrid');
const filterButtons = document.querySelectorAll('.filter-btn');
const sortSelect = document.getElementById('sortDestinos');
const navToggle = document.getElementById('navToggle');
const navMenu = document.querySelector('.nav-menu');
const modalOverlay = document.getElementById('modalOverlay');
const modalClose = document.getElementById('modalClose');
const provinciaOptions = document.querySelectorAll('.provincia-option');

// ===== FUNCIONES =====

// Renderizar destinos en el grid
function renderDestinos(destinos) {
    if (!destinosGrid) return;
    
    destinosGrid.innerHTML = '';
    
    // Ordenar según selección
    const destinosOrdenados = [...destinos].sort((a, b) => {
        switch(sortBy) {
            case 'rating':
                return b.rating - a.rating;
            case 'precio-asc':
                return a.precio - b.precio;
            case 'precio-desc':
                return b.precio - a.precio;
            default:
                return 0; // Mantener orden original para popularidad
        }
    });
    
    destinosOrdenados.forEach(destino => {
        const destinoCard = document.createElement('div');
        destinoCard.className = 'destino-card';
        destinoCard.innerHTML = `
            <div class="destino-image">
                <img src="${destino.thumbnail}" alt="${destino.nombre}" 
                     onerror="this.src='https://via.placeholder.com/400x300/3B82F6/FFFFFF?text=${encodeURIComponent(destino.nombre)}'">
                <div class="destino-badge">${destino.provincia}</div>
                <div class="destino-rating">
                    <i class="fas fa-star"></i> ${destino.rating}
                </div>
            </div>
            <div class="destino-content">
                <h3 class="destino-title">${destino.nombre}</h3>
                <p class="destino-desc">${destino.descripcion}</p>
                <div class="destino-footer">
                    <span class="destino-price">€${destino.precio.toLocaleString('es-ES')}</span>
                    <div class="destino-actions">
                        <button class="btn btn-outline btn-provincia" 
                                data-destino-id="${destino.id}">
                            <i class="fas fa-exchange-alt"></i> Cambiar Provincia
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        destinosGrid.appendChild(destinoCard);
    });
    
    // Agregar eventos a los botones "Cambiar Provincia"
    document.querySelectorAll('.btn-provincia').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const destinoId = parseInt(e.currentTarget.getAttribute('data-destino-id'));
            abrirModalCambiarProvincia(destinoId);
        });
    });
}

// Filtrar destinos por provincia
function filtrarDestinos(provincia) {
    provinciaActual = provincia;
    
    let destinosFiltrados = destinosPlayas;
    
    if (provincia !== 'todas') {
        destinosFiltrados = destinosPlayas.filter(destino => 
            destino.provincia.toLowerCase() === provincia
        );
    }
    
    // Actualizar botones activos
    filterButtons.forEach(btn => {
        if (btn.getAttribute('data-provincia') === provincia) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    
    renderDestinos(destinosFiltrados);
}

// Abrir modal para cambiar provincia
function abrirModalCambiarProvincia(destinoId) {
    destinoSeleccionadoId = destinoId;
    const destino = destinosPlayas.find(d => d.id === destinoId);
    
    if (!destino || !modalOverlay) return;
    
    document.getElementById('modalDestinoNombre').textContent = destino.nombre;
    modalOverlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// Cerrar modal
function cerrarModal() {
    if (!modalOverlay) return;
    
    modalOverlay.style.display = 'none';
    document.body.style.overflow = 'auto';
    destinoSeleccionadoId = null;
}

// Cambiar provincia de un destino
function cambiarProvinciaDestino(provincia) {
    if (!destinoSeleccionadoId) return;
    
    const destinoIndex = destinosPlayas.findIndex(d => d.id === destinoSeleccionadoId);
    
    if (destinoIndex !== -1) {
        destinosPlayas[destinoIndex].provincia = provincia;
        
        // Si el filtro actual no es 'todas' y no coincide, recargar
        if (provinciaActual !== 'todas' && provincia.toLowerCase() !== provinciaActual) {
            filtrarDestinos(provinciaActual);
        } else {
            renderDestinos(provinciaActual === 'todas' ? destinosPlayas : 
                destinosPlayas.filter(d => d.provincia.toLowerCase() === provinciaActual));
        }
        
        // Mostrar notificación
        mostrarNotificacion(`Provincia cambiada a ${provincia}`, 'success');
    }
    
    cerrarModal();
}

// Mostrar notificación
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion notificacion-${tipo}`;
    notificacion.innerHTML = `
        <i class="fas fa-${tipo === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${mensaje}</span>
    `;
    
    // Estilos para la notificación
    notificacion.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${tipo === 'success' ? '#2E8B57' : '#1E90FF'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notificacion);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        notificacion.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notificacion.parentNode) {
                notificacion.parentNode.removeChild(notificacion);
            }
        }, 300);
    }, 3000);
}

// ===== EVENT LISTENERS =====

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    // Renderizar destinos iniciales
    renderDestinos(destinosPlayas);
    
    // Eventos para filtros de provincia
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const provincia = btn.getAttribute('data-provincia');
            filtrarDestinos(provincia);
        });
    });
    
    // Evento para ordenar
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            sortBy = e.target.value;
            filtrarDestinos(provinciaActual);
        });
    }
    
    // Toggle menú móvil
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', (e) => {
        if (navMenu && navToggle && 
            !navMenu.contains(e.target) && 
            !navToggle.contains(e.target)) {
            navMenu.classList.remove('active');
        }
    });
    
    // Eventos para el modal
    if (modalClose) {
        modalClose.addEventListener('click', cerrarModal);
    }
    
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                cerrarModal();
            }
        });
    }
    
    // Eventos para opciones de provincia en el modal
    provinciaOptions.forEach(option => {
        option.addEventListener('click', () => {
            const provincia = option.getAttribute('data-provincia');
            cambiarProvinciaDestino(provincia);
        });
    });
    
    // Cerrar modal con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            cerrarModal();
        }
    });
    
    // Evento para categorías
    document.querySelectorAll('.categoria-card').forEach(card => {
        card.addEventListener('click', () => {
            const categoria = card.getAttribute('data-categoria');
            mostrarNotificacion(`Mostrando destinos de ${categoria}`, 'info');
            // Aquí iría la lógica para cargar destinos de esa categoría
        });
    });
});

// ===== ANIMACIONES CSS DINÁMICAS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notificacion-success {
        background: var(--verde-bosque) !important;
    }
    
    .notificacion-info {
        background: var(--azul-oceano) !important;
    }
`;
document.head.appendChild(style);