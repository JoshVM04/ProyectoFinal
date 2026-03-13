# models/destino.py
"""
Modelo Destino - Representa un destino turístico en Costa Rica
Corresponde a la tabla 'destinos' en la base de datos
"""

class Destino:
    """
    Clase Destino que coincide exactamente con la estructura de la tabla 'destinos'
    Campos: id, título, descripción, provincia, caterogoria_id, imagen, fecha_creación
    """
    
    def __init__(self, id, titulo, descripcion, provincia, caterogoria_id, imagen, fecha_creacion):
        """
        Inicializa una nueva instancia de Destino con los campos de la base de datos
        
        Args:
            id: Identificador único (PRIMARY KEY)
            titulo: Nombre del destino
            descripcion: Descripción detallada
            provincia: Provincia donde se ubica
            caterogoria_id: ID de categoría (1: playas, 2: parques, 3: aventura, 4: termales)
            imagen: Ruta de la imagen principal
            fecha_creacion: Fecha de creación del registro
        """
        # ===== CAMPOS DE LA BASE DE DATOS =====
        # Estos campos mapean directamente a las columnas de la tabla 'destinos'
        self.id = id                       # INT PRIMARY KEY AUTO_INCREMENT
        self.titulo = titulo                 # VARCHAR(200) NOT NULL
        self.descripcion = descripcion       # TEXT
        self.provincia = provincia           # VARCHAR(100)
        self.caterogoria_id = caterogoria_id # INT (FOREIGN KEY a categorias)
        self.imagen = imagen                 # VARCHAR(500)
        self.fecha_creacion = fecha_creacion # TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario para enviar a templates o APIs
        Útil para pasar datos a JSON o a las vistas de Flask
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'provincia': self.provincia,
            'caterogoria_id': self.caterogoria_id,
            'imagen': self.imagen,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d') if self.fecha_creacion else None
        }
    
    def obtener_nombre_categoria(self):
        """
        Devuelve el nombre de la categoría según el ID
        Útil para mostrar en las templates en lugar del número
        """
        categorias = {
            1: "Playas",
            2: "Parques",
            3: "Aventura",
            4: "Termales"
        }
        return categorias.get(self.caterogoria_id, "Desconocido")
    
    def __repr__(self):
        """
        Representación del objeto para debugging
        Se usa cuando se imprime el objeto en consola
        """
        return f"<Destino {self.id}: {self.titulo}>"