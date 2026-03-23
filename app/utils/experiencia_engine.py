# utils/experiencia_engine.py
"""
Motor de Experiencias - Maneja toda la lógica de negocio relacionada con comentarios
Operaciones: obtener, crear, eliminar comentarios
"""

from datetime import datetime

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
            Lista de diccionarios con los comentarios
        """
        if self.usar_datos_prueba:
            return self._obtener_datos_prueba()
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.rating, c.fecha,
                       u.nombre as usuario_nombre, d.titulo as destino_titulo
                FROM comentarios c
                JOIN usuarios u ON c.usuario_id = u.id
                JOIN destinos d ON c.destino_id = d.id
                ORDER BY c.fecha DESC
            """)
            resultados = cursor.fetchall()
            cursor.close()
            
            # Convertir fecha a string para JSON
            for r in resultados:
                if r['fecha']:
                    r['fecha'] = r['fecha'].strftime('%d/%m/%Y')
            
            return resultados
        except Exception as e:
            print(f" Error en obtener_todos: {e}")
            return []
    
    def obtener_por_destino(self, destino_id):
        """
        Obtiene todos los comentarios de un destino específico
        
        Args:
            destino_id: ID del destino
            
        Returns:
            Lista de diccionarios con los comentarios filtrados
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            return [c for c in todos if c['destino_id'] == destino_id]
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.rating, c.fecha,
                       u.nombre as usuario_nombre
                FROM comentarios c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.destino_id = %s
                ORDER BY c.fecha DESC
            """, (destino_id,))
            resultados = cursor.fetchall()
            cursor.close()
            
            for r in resultados:
                if r['fecha']:
                    r['fecha'] = r['fecha'].strftime('%d/%m/%Y')
            
            return resultados
        except Exception as e:
            print(f" Error en obtener_por_destino: {e}")
            return []
    
    def obtener_por_usuario(self, usuario_id):
        """
        Obtiene todos los comentarios de un usuario específico
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Lista de diccionarios con los comentarios filtrados
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            return [c for c in todos if c['usuario_id'] == usuario_id]
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.rating, c.fecha,
                       d.titulo as destino_titulo
                FROM comentarios c
                JOIN destinos d ON c.destino_id = d.id
                WHERE c.usuario_id = %s
                ORDER BY c.fecha DESC
            """, (usuario_id,))
            resultados = cursor.fetchall()
            cursor.close()
            
            for r in resultados:
                if r['fecha']:
                    r['fecha'] = r['fecha'].strftime('%d/%m/%Y')
            
            return resultados
        except Exception as e:
            print(f" Error en obtener_por_usuario: {e}")
            return []
    
    def crear(self, usuario_id, destino_id, comentario_texto, rating=None):
        """
        Crea un nuevo comentario
        
        Args:
            usuario_id: ID del usuario que comenta
            destino_id: ID del destino comentado
            comentario_texto: Texto del comentario
            rating: Calificación de 1 a 5 (opcional)
            
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
        
        # Validar rating si viene
        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    rating = None
            except:
                rating = None
        
        if self.usar_datos_prueba:
            # ===== MODO PRUEBA (sin BD) =====
            comentarios = self._obtener_datos_prueba()
            nuevo_id = len(comentarios) + 100
            
            nuevo_comentario = {
                'id': nuevo_id,
                'usuario_id': usuario_id,
                'destino_id': destino_id,
                'comentario': comentario_texto,
                'rating': rating,
                'fecha': datetime.now().strftime('%d/%m/%Y'),
                'usuario_nombre': f"Usuario {usuario_id}",
                'destino_titulo': f"Destino {destino_id}"
            }
            
            self.comentarios_prueba.append(nuevo_comentario)
            
            return {
                'exito': True,
                'comentario': nuevo_comentario,
                'mensaje': 'Comentario creado correctamente'
            }
        
        # ===== MODO PRODUCCIÓN (con BD) =====
        try:
            cursor = self.db.cursor()
            
            # Insertar comentario (con rating)
            if rating:
                cursor.execute(
                    "INSERT INTO comentarios (usuario_id, destino_id, comentario, rating, fecha) VALUES (%s, %s, %s, %s, NOW())",
                    (usuario_id, destino_id, comentario_texto, rating)
                )
            else:
                cursor.execute(
                    "INSERT INTO comentarios (usuario_id, destino_id, comentario, fecha) VALUES (%s, %s, %s, NOW())",
                    (usuario_id, destino_id, comentario_texto)
                )
            
            self.db.commit()
            nuevo_id = cursor.lastrowid
            cursor.close()
            
            # Obtener el comentario recién creado con nombres
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, c.usuario_id, c.destino_id, c.comentario, c.rating, c.fecha,
                       u.nombre as usuario_nombre, d.titulo as destino_titulo
                FROM comentarios c
                JOIN usuarios u ON c.usuario_id = u.id
                JOIN destinos d ON c.destino_id = d.id
                WHERE c.id = %s
            """, (nuevo_id,))
            
            comentario = cursor.fetchone()
            cursor.close()
            
            if comentario:
                if comentario['fecha']:
                    comentario['fecha'] = comentario['fecha'].strftime('%d/%m/%Y')
                
                return {
                    'exito': True,
                    'comentario': comentario,
                    'mensaje': 'Comentario creado correctamente'
                }
            
            return {'exito': False, 'error': 'Error al recuperar comentario'}
            
        except Exception as e:
            print(f" Error al crear comentario: {e}")
            self.db.rollback()
            return {'exito': False, 'error': str(e)}
    
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
                if c['id'] == comentario_id:
                    comentario = c
                    break
            
            if not comentario:
                return {'exito': False, 'error': 'Comentario no encontrado'}
            
            # Verificar permisos
            if not es_owner and comentario['usuario_id'] != usuario_id:
                return {'exito': False, 'error': 'No tienes permiso para eliminar este comentario'}
            
            # Eliminar
            self.comentarios_prueba = [c for c in self.comentarios_prueba if c['id'] != comentario_id]
            
            return {'exito': True, 'mensaje': 'Comentario eliminado correctamente'}
        
        # ===== MODO PRODUCCIÓN (con BD) =====
        try:
            cursor = self.db.cursor()
            
            # Verificar permisos si es necesario
            if not es_owner and usuario_id:
                cursor.execute(
                    "SELECT usuario_id FROM comentarios WHERE id = %s",
                    (comentario_id,)
                )
                row = cursor.fetchone()
                if not row:
                    cursor.close()
                    return {'exito': False, 'error': 'Comentario no encontrado'}
                if row[0] != usuario_id:
                    cursor.close()
                    return {'exito': False, 'error': 'No tienes permiso para eliminar este comentario'}
            
            # Eliminar comentario
            cursor.execute("DELETE FROM comentarios WHERE id = %s", (comentario_id,))
            self.db.commit()
            filas_afectadas = cursor.rowcount
            cursor.close()
            
            if filas_afectadas > 0:
                return {'exito': True, 'mensaje': 'Comentario eliminado correctamente'}
            else:
                return {'exito': False, 'error': 'Comentario no encontrado'}
                
        except Exception as e:
            print(f" Error al eliminar comentario: {e}")
            self.db.rollback()
            return {'exito': False, 'error': str(e)}
    
    def _obtener_datos_prueba(self):
        """
        Método privado para inicializar datos de prueba
        Crea algunos comentarios de ejemplo
        """
        if not self.comentarios_prueba:
            from datetime import datetime, timedelta
            
            # Comentario 1
            c1 = {
                'id': 1,
                'usuario_id': 1,
                'destino_id': 1,
                'comentario': "Playa Conchal superó todas mis expectativas. La atención al detalle y calidad del servicio son excepcionales.",
                'rating': 5,
                'fecha': (datetime.now() - timedelta(days=14)).strftime('%d/%m/%Y'),
                'usuario_nombre': "Ana Martínez",
                'destino_titulo': "Playa Conchal"
            }
            
            # Comentario 2
            c2 = {
                'id': 2,
                'usuario_id': 2,
                'destino_id': 5,
                'comentario': "La experiencia en el Parque Nacional Arenal fue increíble. Los guías son expertos y la organización impecable.",
                'rating': 4,
                'fecha': (datetime.now() - timedelta(days=30)).strftime('%d/%m/%Y'),
                'usuario_nombre': "Carlos Rodríguez",
                'destino_titulo': "Volcán Arenal"
            }
            
            # Comentario 3
            c3 = {
                'id': 3,
                'usuario_id': 3,
                'destino_id': 12,
                'comentario': "El rafting en el Río Pacuare fue la mejor aventura de mi vida. Seguridad, profesionalismo y pura adrenalina.",
                'rating': 5,
                'fecha': (datetime.now() - timedelta(days=3)).strftime('%d/%m/%Y'),
                'usuario_nombre': "Sofía González",
                'destino_titulo': "Río Pacuare"
            }
            
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
        
        # Si ya son diccionarios, devolverlos directamente
        if comentarios and isinstance(comentarios[0], dict):
            return comentarios
        
        # Si son objetos, convertirlos
        return [c.to_dict_completo() if hasattr(c, 'to_dict_completo') else c for c in comentarios]