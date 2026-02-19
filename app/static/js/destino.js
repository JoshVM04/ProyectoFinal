// static/js/destino.js
// Funciones visuales: Lightbox + animaciones

document.addEventListener('DOMContentLoaded', function() {
    
    // ===========================================
    // 1. LIGHTBOX - Ver imágenes en grande
    // ===========================================
    const galeriaImagenes = document.querySelectorAll('.galeria-grid img');
    
    galeriaImagenes.forEach(img => {
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Crear overlay
            const overlay = document.createElement('div');
            overlay.className = 'lightbox-overlay';
            
            // Contenedor de la imagen
            const lightboxContainer = document.createElement('div');
            lightboxContainer.className = 'lightbox-container';
            
            // Imagen grande
            const largeImg = document.createElement('img');
            largeImg.src = this.src;
            largeImg.alt = this.alt;
            largeImg.className = 'lightbox-imagen';
            
            // Botón cerrar
            const closeBtn = document.createElement('span');
            closeBtn.className = 'lightbox-cerrar';
            closeBtn.innerHTML = '&times;';
            
            // Botones anterior/siguiente (opcional)
            if (galeriaImagenes.length > 1) {
                const prevBtn = document.createElement('span');
                prevBtn.className = 'lightbox-nav lightbox-prev';
                prevBtn.innerHTML = '&#10094;';
                
                const nextBtn = document.createElement('span');
                nextBtn.className = 'lightbox-nav lightbox-next';
                nextBtn.innerHTML = '&#10095;';
                
                lightboxContainer.appendChild(prevBtn);
                lightboxContainer.appendChild(nextBtn);
                
                // Obtener índice de la imagen actual
                const imagenesArray = Array.from(galeriaImagenes);
                let currentIndex = imagenesArray.indexOf(this);
                
                // Función para cambiar imagen
                function cambiarImagen(nuevaIndex) {
                    if (nuevaIndex < 0) nuevaIndex = imagenesArray.length - 1;
                    if (nuevaIndex >= imagenesArray.length) nuevaIndex = 0;
                    
                    largeImg.src = imagenesArray[nuevaIndex].src;
                    largeImg.alt = imagenesArray[nuevaIndex].alt;
                    currentIndex = nuevaIndex;
                    
                    // Animación de fade
                    largeImg.style.animation = 'none';
                    largeImg.offsetHeight;
                    largeImg.style.animation = 'fadeIn 0.3s';
                }
                
                prevBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    cambiarImagen(currentIndex - 1);
                });
                
                nextBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    cambiarImagen(currentIndex + 1);
                });
            }
            
            // Armar lightbox
            lightboxContainer.appendChild(largeImg);
            lightboxContainer.appendChild(closeBtn);
            overlay.appendChild(lightboxContainer);
            document.body.appendChild(overlay);
            
            // Mostrar con animación
            setTimeout(() => overlay.classList.add('active'), 10);
            
            // Cerrar al hacer click en overlay o botón cerrar
            overlay.addEventListener('click', function() {
                this.classList.remove('active');
                setTimeout(() => this.remove(), 300);
            });
            
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                overlay.classList.remove('active');
                setTimeout(() => overlay.remove(), 300);
            });
            
            // Evitar que click en container cierre
            lightboxContainer.addEventListener('click', (e) => e.stopPropagation());
        });
    });

    // ===========================================
    // 2. ANIMACIÓN AL HACER SCROLL (fade in)
    // ===========================================
    const secciones = document.querySelectorAll('.seccion-links');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.2,
        rootMargin: '0px'
    });
    
    secciones.forEach(seccion => {
        seccion.classList.add('fade-section');
        observer.observe(seccion);
    });

    // ===========================================
    // 3. ANIMACIÓN DE PRECIO (contador opcional)
    // ===========================================
    const precioElement = document.querySelector('.valor');
    if (precioElement) {
        const precioFinal = parseInt(precioElement.textContent);
        let precioActual = 0;
        const duracion = 1000; // 1 segundo
        const incremento = precioFinal / (duracion / 16); // 60fps
        
        function animarPrecio() {
            precioActual += incremento;
            if (precioActual < precioFinal) {
                precioElement.textContent = Math.floor(precioActual);
                requestAnimationFrame(animarPrecio);
            } else {
                precioElement.textContent = precioFinal;
            }
        }
        
        // Iniciar animación cuando sea visible
        const precioObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animarPrecio();
                    precioObserver.unobserve(entry.target);
                }
            });
        });
        
        precioObserver.observe(precioElement);
    }

    // ===========================================
    // 4. EFECTO HOVER SUAVE EN LINKS
    // ===========================================
    const links = document.querySelectorAll('.link-item');
    
    links.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });

});