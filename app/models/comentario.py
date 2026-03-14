# models/comentario.py
"""
Modelo Comentario - Representa una experiencia/reseña de un usuario sobre un destino
Corresponde a la tabla 'comentarios' en la base de datos
"""

from datetime import datetime

class Comentario:
    """
    Clase Comentario que coincide exactamente con la estructura de la tabla 'comentarios'
    Campos: id, usuario_id, destino_id, comentario, fecha
    """
    
    def __init__(self, id, usuario_id, destino_id, comentario, fecha=None):
        """
        Inicializa una nueva instancia de Comentario con los campos de la base de datos
        
        Args:
            id: Identificador único (PRIMARY KEY)
            usuario_id: ID del usuario que comenta (FOREIGN KEY a usuarios)
            destino_id: ID del destino comentado (FOREIGN KEY a destinos)
            comentario: Texto del comentario/experiencia
            fecha: Fecha del comentario (TIMESTAMP)
        """
        # ===== CAMPOS DE LA BASE DE DATOS =====
        # Estos campos mapean directamente a las columnas de la tabla 'comentarios'
        self.id = id                       # INT PRIMARY KEY AUTO_INCREMENT
        self.usuario_id = usuario_id         # INT NOT NULL (FOREIGN KEY)
        self.destino_id = destino_id         # INT NOT NULL (FOREIGN KEY)
        self.comentario = comentario         # TEXT NOT NULL
        self.fecha = fecha or datetime.now() # TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        
        # ===== CAMPOS ADICIONALES (NO EN BD) =====
        # Se llenan después con JOINs para mostrar en templates
        self._usuario_nombre = None
        self._destino_titulo = None
    
    def set_usuario_nombre(self, nombre):
        """
        Establece el nombre del usuario (después de un JOIN)
        
        Args:
            nombre: Nombre del usuario
        """
        self._usuario_nombre = nombre
    
    def set_destino_titulo(self, titulo):
        """
        Establece el título del destino (después de un JOIN)
        
        Args:
            titulo: Título del destino
        """
        self._destino_titulo = titulo
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario para enviar a templates o APIs
        """
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'destino_id': self.destino_id,
            'comentario': self.comentario,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M') if self.fecha else None
        }
    
    def to_dict_completo(self):
        """
        Versión completa con nombres de usuario y destino (después de JOIN)
        """
        data = self.to_dict()
        data['usuario_nombre'] = self._usuario_nombre or f"Usuario {self.usuario_id}"
        data['destino_titulo'] = self._destino_titulo or f"Destino {self.destino_id}"
        return data
    
    def __repr__(self):
        """
        Representación del objeto para debugging
        """
        return f"<Comentario {self.id}: Usuario {self.usuario_id} → Destino {self.destino_id}>"