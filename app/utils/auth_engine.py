# utils/auth_engine.py
"""
Motor de Autenticación - Maneja toda la lógica de negocio relacionada con usuarios
Operaciones: registro, login, verificación, etc.
"""

import hashlib
from datetime import datetime
from app.models.usuario import Usuario

class AuthEngine:
    """
    Clase que encapsula todas las operaciones relacionadas con autenticación
    Actúa como intermediario entre las rutas y la base de datos
    """
    
    def __init__(self, db_connection=None):
        """
        Inicializa el motor de autenticación
        
        Args:
            db_connection: Conexión a la base de datos (opcional, para pruebas)
        """
        self.db = db_connection
        # Si no hay conexión, usamos datos quemados para pruebas
        self.usar_datos_prueba = db_connection is None
        self.usuarios_prueba = []  # Se llena en _obtener_datos_prueba si es necesario
    
    def _hash_contra(self, contra_plana):
        """
        Hashea una contraseña usando SHA-256
        
        Args:
            contra_plana: Contraseña sin hashear
            
        Returns:
            str: Contraseña hasheada
        """
        return hashlib.sha256(contra_plana.encode()).hexdigest()
    
    def registrar(self, nombre, email, contra):
        """
        Registra un nuevo usuario en el sistema
        
        Args:
            nombre: Nombre completo del usuario
            email: Correo electrónico
            contra: Contraseña (sin hashear)
            
        Returns:
            dict: Resultado con éxito o error
        """
        # ===== VALIDACIONES BÁSICAS =====
        if not nombre or len(nombre) < 2:
            return {'exito': False, 'error': 'El nombre debe tener al menos 2 caracteres'}
        
        if not email or '@' not in email or '.' not in email:
            return {'exito': False, 'error': 'Email no válido'}
        
        if not contra or len(contra) < 6:
            return {'exito': False, 'error': 'La contraseña debe tener al menos 6 caracteres'}
        
        if self.usar_datos_prueba:
            # ===== MODO PRUEBA (sin BD) =====
            # Verificar si el email ya existe
            for u in self.usuarios_prueba:
                if u.email == email:
                    return {'exito': False, 'error': 'El email ya está registrado'}
            
            # Crear nuevo usuario
            nuevo_id = len(self.usuarios_prueba) + 1
            contra_hash = self._hash_contra(contra)
            nuevo_usuario = Usuario(nuevo_id, nombre, email, contra_hash, datetime.now())
            self.usuarios_prueba.append(nuevo_usuario)
            
            return {
                'exito': True, 
                'usuario': nuevo_usuario.to_dict(),
                'mensaje': 'Usuario registrado correctamente'
            }
        
        # ===== MODO PRODUCCIÓN (con BD) =====
        try:
            cursor = self.db.cursor()
            
            # Verificar si el email ya existe
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                return {'exito': False, 'error': 'El email ya está registrado'}
            
            # Insertar nuevo usuario
            contra_hash = self._hash_contra(contra)
            cursor.execute(
                "INSERT INTO usuarios (nombre, email, contra, fecha_registro) VALUES (%s, %s, %s, %s)",
                (nombre, email, contra_hash, datetime.now())
            )
            self.db.commit()
            
            nuevo_id = cursor.lastrowid
            cursor.close()
            
            nuevo_usuario = Usuario(nuevo_id, nombre, email, contra_hash, datetime.now())
            
            return {
                'exito': True,
                'usuario': nuevo_usuario.to_dict(),
                'mensaje': 'Usuario registrado correctamente'
            }
            
        except Exception as e:
            print(f"❌ Error en registro: {e}")
            return {'exito': False, 'error': 'Error al registrar usuario'}
    
    def login(self, email, contra):
        """
        Inicia sesión verificando credenciales
        
        Args:
            email: Correo electrónico
            contra: Contraseña (sin hashear)
            
        Returns:
            dict: Resultado con éxito o error y datos del usuario
        """
        # ===== VALIDACIONES BÁSICAS =====
        if not email or not contra:
            return {'exito': False, 'error': 'Email y contraseña son requeridos'}
        
        if self.usar_datos_prueba:
            # ===== MODO PRUEBA (sin BD) =====
            # Buscar usuario por email
            usuario = None
            for u in self.usuarios_prueba:
                if u.email == email:
                    usuario = u
                    break
            
            if not usuario:
                return {'exito': False, 'error': 'Email no registrado'}
            
            # Verificar contraseña
            contra_hash = self._hash_contra(contra)
            if usuario.contra == contra_hash:
                return {
                    'exito': True,
                    'usuario': usuario.to_dict(),
                    'mensaje': 'Login exitoso'
                }
            else:
                return {'exito': False, 'error': 'Contraseña incorrecta'}
        
        # ===== MODO PRODUCCIÓN (con BD) =====
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Buscar usuario por email
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            
            if not user:
                return {'exito': False, 'error': 'Email no registrado'}
            
            # Verificar contraseña
            contra_hash = self._hash_contra(contra)
            
            if user['contra'] == contra_hash:
                # Login exitoso
                return {
                    'exito': True,
                    'usuario': {
                        'id': user['id'],
                        'nombre': user['nombre'],
                        'email': user['email'],
                        'rol': user.get('rol', 'usuario')
                    }
                }
            else:
                return {'exito': False, 'error': 'Contraseña incorrecta'}
                
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return {'exito': False, 'error': 'Error al iniciar sesión'}
    
    def obtener_por_id(self, usuario_id):
        """
        Obtiene un usuario por su ID
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Usuario o None si no existe
        """
        if self.usar_datos_prueba:
            for u in self.usuarios_prueba:
                if u.id == usuario_id:
                    return u
            return None
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                return {
                    'id': user['id'],
                    'nombre': user['nombre'],
                    'email': user['email'],
                    'rol': user.get('rol', 'usuario')
                }
            return None
            
        except Exception as e:
            print(f"❌ Error al obtener usuario: {e}")
            return None
    
    def _obtener_datos_prueba(self):
        """
        Método privado para inicializar datos de prueba
        Solo se usa si no hay conexión a BD
        """
        if not self.usuarios_prueba:
            # Crear usuario de prueba por defecto
            contra_hash = self._hash_contra("123456")
            self.usuarios_prueba.append(
                Usuario(1, "Usuario Prueba", "test@test.com", contra_hash, datetime.now())
            )
        return self.usuarios_prueba