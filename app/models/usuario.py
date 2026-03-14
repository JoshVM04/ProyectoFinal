# models/usuario.py
"""
Modelo Usuario - Representa un usuario del sistema
Corresponde a la tabla 'usuarios' en la base de datos
"""

import hashlib
from datetime import datetime

class Usuario:
    """
    Clase Usuario que coincide exactamente con la estructura de la tabla 'usuarios'
    Campos: id, nombre, email, contra, fecha_registro
    """
    
    def __init__(self, id, nombre, email, contra, fecha_registro=None):
        """
        Inicializa una nueva instancia de Usuario con los campos de la base de datos
        
        Args:
            id: Identificador único (PRIMARY KEY)
            nombre: Nombre completo del usuario
            email: Correo electrónico (UNIQUE)
            contra: Contraseña (se almacena hasheada)
            fecha_registro: Fecha de registro (TIMESTAMP)
        """
        # ===== CAMPOS DE LA BASE DE DATOS =====
        # Estos campos mapean directamente a las columnas de la tabla 'usuarios'
        self.id = id                       # INT PRIMARY KEY AUTO_INCREMENT
        self.nombre = nombre                 # VARCHAR(100) NOT NULL
        self.email = email                   # VARCHAR(100) UNIQUE NOT NULL
        self.contra = contra                 # VARCHAR(255) NOT NULL (hash)
        self.fecha_registro = fecha_registro or datetime.now()  # TIMESTAMP
    
    def verificar_contra(self, contra_plana):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado
        
        Args:
            contra_plana: Contraseña sin hashear ingresada por el usuario
            
        Returns:
            bool: True si coincide, False si no
        """
        # Hashear la contraseña ingresada y comparar con el hash almacenado
        hash_ingresado = hashlib.sha256(contra_plana.encode()).hexdigest()
        return self.contra == hash_ingresado
    
    def cambiar_contra(self, contra_nueva):
        """
        Cambia la contraseña del usuario (ya debe venir hasheada desde el engine)
        
        Args:
            contra_nueva: Nueva contraseña (ya hasheada)
        """
        self.contra = contra_nueva
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario para enviar a templates o APIs
        NUNCA incluir la contraseña en el diccionario por seguridad
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M') if self.fecha_registro else None
        }
    
    def __repr__(self):
        """
        Representación del objeto para debugging
        Se usa cuando se imprime el objeto en consola
        """
        return f"<Usuario {self.id}: {self.email}>"