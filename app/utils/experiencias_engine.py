# utils/experiencia_engine.py
"""
Motor de Experiencias - Maneja toda la lógica de negocio relacionada con comentarios
Operaciones: obtener, crear, eliminar comentarios
"""

from datetime import datetime
from app.models.comentario import Comentario

class ExperienciaEngine:
    """
    Clase que encapsula todas las operaciones relacionadas con experiencias/comentarios
    Actúa como intermediario entre las rutas y la base de datos
    """
    
    def __init__(self, db_connection=None):
        """
        Inicializa el motor de experiencias
        
        Args:
            db_connection: Conexión a la base de datos (opcional, para pruebas)
        """
        self.db = db_connection
        # Si no hay conexión, usamos datos quemados para pruebas
        self.usar_datos_prueba = db_connection is None
        self.comentarios_prueba = []  # Se llena en _obtener_datos_prueba si es necesario
    
    def obtener_todos(self):
        """
        Obtiene todos los comentarios con información de usuario y destino
        
        Returns:
            Lista de objetos Comentario con nombres cargados
        """
        if self.usar_datos_prueba:
            return self._obtener_datos_prueba()
        
        # ===== CONSULTA SQL CON JOINS =====
        # SELECT c.*, u.nombre as usuario_nombre, d.titulo as destino_titulo
        # FROM comentarios c
        # JOIN usuarios u ON c.usuario_id = u.id
        # JOIN destinos d ON c.destino_id = d.id
        # ORDER BY c.fecha DESC
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.fecha,
                   u.nombre as usuario_nombre, d.titulo as destino_titulo
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            JOIN destinos d ON c.destino_id = d.id
            ORDER BY c.fecha DESC
        """)
        resultados = cursor.fetchall()
        
        comentarios = []
        for row in resultados:
            comentario = Comentario(
                id=row[0],
                usuario_id=row[1],
                destino_id=row[2],
                comentario=row[3],
                fecha=row[4]
            )
            # Agregar nombres de los JOINs
            comentario.set_usuario_nombre(row[5])
            comentario.set_destino_titulo(row[6])
            comentarios.append(comentario)
        
        return comentarios
    
    def obtener_por_destino(self, destino_id):
        """
        Obtiene todos los comentarios de un destino específico
        
        Args:
            destino_id: ID del destino
            
        Returns:
            Lista de objetos Comentario filtrados
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            return [c for c in todos if c.destino_id == destino_id]
        
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.fecha,
                   u.nombre as usuario_nombre, d.titulo as destino_titulo
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            JOIN destinos d ON c.destino_id = d.id
            WHERE c.destino_id = %s
            ORDER BY c.fecha DESC
        """, (destino_id,))
        resultados = cursor.fetchall()
        
        comentarios = []
        for row in resultados:
            comentario = Comentario(
                id=row[0],
                usuario_id=row[1],
                destino_id=row[2],
                comentario=row[3],
                fecha=row[4]
            )
            comentario.set_usuario_nombre(row[5])
            comentario.set_destino_titulo(row[6])
            comentarios.append(comentario)
        
        return comentarios
    
    def obtener_por_usuario(self, usuario_id):
        """
        Obtiene todos los comentarios de un usuario específico
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Lista de objetos Comentario filtrados
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            return [c for c in todos if c.usuario_id == usuario_id]
        
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.fecha,
                   u.nombre as usuario_nombre, d.titulo as destino_titulo
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            JOIN destinos d ON c.destino_id = d.id
            WHERE c.usuario_id = %s
            ORDER BY c.fecha DESC
        """, (usuario_id,))
        resultados = cursor.fetchall()
        
        comentarios = []
        for row in resultados:
            comentario = Comentario(
                id=row[0],
                usuario_id=row[1],
                destino_id=row[2],
                comentario=row[3],
                fecha=row[4]
            )
            comentario.set_usuario_nombre(row[5])
            comentario.set_destino_titulo(row[6])
            comentarios.append(comentario)
        
        return comentarios
    
    def crear(self, usuario_id, destino_id, comentario_texto):
        """
        Crea un nuevo comentario
        
        Args:
            usuario_id: ID del usuario que comenta
            destino_id: ID del destino comentado
            comentario_texto: Texto del comentario
            
        Returns:
            dict: Resultado con éxito o error y el comentario creado
        """
        # ===== VALIDACIONES BÁSICAS =====
        if not comentario_texto or len(comentario_texto.strip()) < 5:
            return {'exito': False, 'error': 'El comentario debe tener al menos 5 caracteres'}
        
        if not usuario_id:
            return {'exito': False, 'error': 'Usuario no válido'}
        
        if not destino_id:
            return {'exito': False, 'error': 'Destino no válido'}
        
        if self.usar_datos_prueba:
            # ===== MODO PRUEBA (sin BD) =====
            nuevo_id = len(self._obtener_datos_prueba()) + 100
            nuevo_comentario = Comentario(
                id=nuevo_id,
                usuario_id=usuario_id,
                destino_id=destino_id,
                comentario=comentario_texto,
                fecha=datetime.now()
            )
            
            # Buscar nombres para los campos adicionales
            # En modo prueba, usar nombres genéricos
            nuevo_comentario.set_usuario_nombre(f"Usuario {usuario_id}")
            nuevo_comentario.set_destino_titulo(f"Destino {destino_id}")
            
            self.comentarios_prueba.append(nuevo_comentario)
            
            return {
                'exito': True,
                'comentario': nuevo_comentario.to_dict_completo(),
                'mensaje': 'Comentario creado correctamente'
            }
        
        # ===== MODO PRODUCCIÓN (con BD) =====
        cursor = self.db.cursor()
        
        # Insertar comentario
        cursor.execute(
            "INSERT INTO comentarios (usuario_id, destino_id, comentario, fecha) VALUES (%s, %s, %s, %s)",
            (usuario_id, destino_id, comentario_texto, datetime.now())
        )
        self.db.commit()
        
        nuevo_id = cursor.lastrowid
        
        # Obtener el comentario recién creado con nombres
        cursor.execute("""
            SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.fecha,
                   u.nombre as usuario_nombre, d.titulo as destino_titulo
            FROM comentarios c
            JOIN usuarios u ON c.usuario_id = u.id
            JOIN destinos d ON c.destino_id = d.id
            WHERE c.id = %s
        """, (nuevo_id,))
        
        row = cursor.fetchone()
        
        if row:
            comentario = Comentario(
                id=row[0],
                usuario_id=row[1],
                destino_id=row[2],
                comentario=row[3],
                fecha=row[4]
            )
            comentario.set_usuario_nombre(row[5])
            comentario.set_destino_titulo(row[6])
            
            return {
                'exito': True,
                'comentario': comentario.to_dict_completo(),
                'mensaje': 'Comentario creado correctamente'
            }
        
        return {'exito': False, 'error': 'Error al crear comentario'}
    
    def eliminar(self, comentario_id, usuario_id=None, es_owner=False):
        """
        Elimina un comentario (solo el autor o el owner)
        
        Args:
            comentario_id: ID del comentario a eliminar
            usuario_id: ID del usuario que intenta eliminar (opcional)
            es_owner: True si el usuario es owner del sistema
            
        Returns:
            dict: Resultado con éxito o error
        """
        if self.usar_datos_prueba:
            # Buscar comentario
            comentario = None
            for c in self.comentarios_prueba:
                if c.id == comentario_id:
                    comentario = c
                    break
            
            if not comentario:
                return {'exito': False, 'error': 'Comentario no encontrado'}
            
            # Verificar permisos
            if not es_owner and comentario.usuario_id != usuario_id:
                return {'exito': False, 'error': 'No tienes permiso para eliminar este comentario'}
            
            # Eliminar
            self.comentarios_prueba = [c for c in self.comentarios_prueba if c.id != comentario_id]
            
            return {'exito': True, 'mensaje': 'Comentario eliminado correctamente'}
        
        # ===== MODO PRODUCCIÓN (con BD) =====
        cursor = self.db.cursor()
        
        # Verificar permisos si es necesario
        if not es_owner and usuario_id:
            cursor.execute(
                "SELECT usuario_id FROM comentarios WHERE id = %s",
                (comentario_id,)
            )
            row = cursor.fetchone()
            if not row:
                return {'exito': False, 'error': 'Comentario no encontrado'}
            if row[0] != usuario_id:
                return {'exito': False, 'error': 'No tienes permiso para eliminar este comentario'}
        
        # Eliminar comentario
        cursor.execute("DELETE FROM comentarios WHERE id = %s", (comentario_id,))
        self.db.commit()
        
        if cursor.rowcount > 0:
            return {'exito': True, 'mensaje': 'Comentario eliminado correctamente'}
        else:
            return {'exito': False, 'error': 'Comentario no encontrado'}
    
    def _obtener_datos_prueba(self):
        """
        Método privado para inicializar datos de prueba
        Crea algunos comentarios de ejemplo
        """
        if not self.comentarios_prueba:
            from datetime import datetime, timedelta
            
            # Comentario 1
            c1 = Comentario(1, 1, 1, "Playa Conchal superó todas mis expectativas. La atención al detalle y calidad del servicio son excepcionales.", datetime.now() - timedelta(days=14))
            c1.set_usuario_nombre("Ana Martínez")
            c1.set_destino_titulo("Playa Conchal")
            
            # Comentario 2
            c2 = Comentario(2, 2, 5, "La experiencia en el Parque Nacional Arenal fue increíble. Los guías son expertos y la organización impecable.", datetime.now() - timedelta(days=30))
            c2.set_usuario_nombre("Carlos Rodríguez")
            c2.set_destino_titulo("Volcán Arenal")
            
            # Comentario 3
            c3 = Comentario(3, 3, 12, "El rafting en el Río Pacuare fue la mejor aventura de mi vida. Seguridad, profesionalismo y pura adrenalina.", datetime.now() - timedelta(days=3))
            c3.set_usuario_nombre("Sofía González")
            c3.set_destino_titulo("Río Pacuare")
            
            self.comentarios_prueba = [c1, c2, c3]
        
        return self.comentarios_prueba
    
    def to_dict_list(self, comentarios=None):
        """
        Convierte una lista de objetos Comentario a lista de diccionarios
        
        Args:
            comentarios: Lista de Comentario (opcional, usa todos si no se especifica)
            
        Returns:
            Lista de diccionarios para JSON/templates
        """
        if comentarios is None:
            comentarios = self.obtener_todos()
        return [c.to_dict_completo() for c in comentarios]