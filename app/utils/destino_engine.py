# utils/destino_engine.py
"""
Motor de Destinos - Maneja toda la lógica de negocio relacionada con destinos
Operaciones: obtener, filtrar, buscar, etc.
"""

from app.models.destino import Destino

class DestinoEngine:
    """
    Clase que encapsula todas las operaciones relacionadas con destinos
    Actúa como intermediario entre las rutas y la base de datos
    """
    
    def __init__(self, db_connection=None):
        """
        Inicializa el motor de destinos
        
        Args:
            db_connection: Conexión a la base de datos (opcional, para pruebas)
        """
        self.db = db_connection
        # Si no hay conexión, usamos datos quemados para pruebas
        self.usar_datos_prueba = db_connection is None
    
    def obtener_todos(self):
        """
        Obtiene todos los destinos de la base de datos
        
        Returns:
            Lista de objetos Destino
        """
        if self.usar_datos_prueba:
            return self._obtener_datos_prueba()
        
        # ===== CONSULTA SQL =====
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.*, c.nombre as categoria_nombre 
            FROM destinos d
            LEFT JOIN categorias c ON d.categoria_id = c.id
            ORDER BY d.titulo
        """)
        resultados = cursor.fetchall()
        cursor.close()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                provincia=row['provincia'],
                categoria_id=row['categoria_id'],
                imagen_principal=row['imagen_principal'],
                costo_dia=row['costo_dia'],
                que_incluye=row['que_incluye'],
                fecha_creacion=row['fecha_creacion']
            )
            destinos.append(destino)
        
        return destinos
    
    def obtener_por_id(self, destino_id):
        """
        Obtiene un destino específico por su ID con todas sus relaciones
        
        Args:
            destino_id: ID del destino a buscar
            
        Returns:
            Diccionario con todos los datos del destino o None si no existe
        """
        if self.usar_datos_prueba:
            destinos = self._obtener_datos_prueba()
            for d in destinos:
                if d.id == destino_id:
                    return d.to_dict_completo()
            return None
        
        cursor = self.db.cursor(dictionary=True)
        
        # 1. Obtener datos básicos del destino
        cursor.execute("""
            SELECT d.*, c.nombre as categoria_nombre 
            FROM destinos d
            LEFT JOIN categorias c ON d.categoria_id = c.id
            WHERE d.id = %s
        """, (destino_id,))
        destino = cursor.fetchone()
        
        if not destino:
            cursor.close()
            return None
        
        # 2. Obtener imágenes adicionales
        cursor.execute(
            "SELECT imagen FROM imagenes_destino WHERE destino_id = %s",
            (destino_id,)
        )
        imagenes = cursor.fetchall()
        destino['imagenes'] = [img['imagen'] for img in imagenes]
        
        # 3. Obtener actividades
        cursor.execute(
            "SELECT * FROM actividades WHERE destino_id = %s",
            (destino_id,)
        )
        destino['actividades'] = cursor.fetchall()
        
        # 4. Obtener restaurantes
        cursor.execute(
            "SELECT * FROM restaurantes WHERE destino_id = %s",
            (destino_id,)
        )
        destino['restaurantes'] = cursor.fetchall()
        
        # 5. Obtener hospedajes
        cursor.execute(
            "SELECT * FROM hospedajes WHERE destino_id = %s",
            (destino_id,)
        )
        destino['hospedajes'] = cursor.fetchall()
        
        # 6. Obtener renta de carros
        cursor.execute(
            "SELECT * FROM rentacar WHERE destino_id = %s",
            (destino_id,)
        )
        destino['rentacar'] = cursor.fetchall()
        
        cursor.close()
        return destino
    
    def obtener_por_categoria(self, categoria_id):
        """
        Filtra destinos por categoría
        
        Args:
            categoria_id: ID de categoría (1-4)
            
        Returns:
            Lista de objetos Destino filtrados
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            return [d for d in todos if d.categoria_id == categoria_id]
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.*, c.nombre as categoria_nombre 
            FROM destinos d
            LEFT JOIN categorias c ON d.categoria_id = c.id
            WHERE d.categoria_id = %s
            ORDER BY d.titulo
        """, (categoria_id,))
        resultados = cursor.fetchall()
        cursor.close()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                provincia=row['provincia'],
                categoria_id=row['categoria_id'],
                imagen_principal=row['imagen_principal'],
                costo_dia=row['costo_dia'],
                que_incluye=row['que_incluye'],
                fecha_creacion=row['fecha_creacion']
            )
            destinos.append(destino)
        
        return destinos
    
    def obtener_por_provincia(self, provincia):
        """
        Filtra destinos por provincia
        
        Args:
            provincia: Nombre de la provincia
            
        Returns:
            Lista de objetos Destino filtrados
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            return [d for d in todos if d.provincia.lower() == provincia.lower()]
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT d.*, c.nombre as categoria_nombre 
            FROM destinos d
            LEFT JOIN categorias c ON d.categoria_id = c.id
            WHERE d.provincia = %s
            ORDER BY d.titulo
        """, (provincia,))
        resultados = cursor.fetchall()
        cursor.close()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                provincia=row['provincia'],
                categoria_id=row['categoria_id'],
                imagen_principal=row['imagen_principal'],
                costo_dia=row['costo_dia'],
                que_incluye=row['que_incluye'],
                fecha_creacion=row['fecha_creacion']
            )
            destinos.append(destino)
        
        return destinos
    
    def buscar(self, termino):
        """
        Busca destinos por título o descripción
        
        Args:
            termino: Palabra o frase a buscar
            
        Returns:
            Lista de objetos Destino que coinciden
        """
        if self.usar_datos_prueba:
            todos = self._obtener_datos_prueba()
            termino = termino.lower()
            resultados = []
            for d in todos:
                if (termino in d.titulo.lower() or 
                    termino in d.descripcion.lower()):
                    resultados.append(d)
            return resultados
        
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT d.*, c.nombre as categoria_nombre 
            FROM destinos d
            LEFT JOIN categorias c ON d.categoria_id = c.id
            WHERE LOWER(d.titulo) LIKE %s OR LOWER(d.descripcion) LIKE %s
            ORDER BY d.titulo
        """
        param = f"%{termino.lower()}%"
        cursor.execute(query, (param, param))
        resultados = cursor.fetchall()
        cursor.close()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                provincia=row['provincia'],
                categoria_id=row['categoria_id'],
                imagen_principal=row['imagen_principal'],
                costo_dia=row['costo_dia'],
                que_incluye=row['que_incluye'],
                fecha_creacion=row['fecha_creacion']
            )
            destinos.append(destino)
        
        return destinos
    
    def _obtener_datos_prueba(self):
        """
        Método privado para pruebas sin BD
        Retorna una lista de destinos quemados
        """
        from datetime import datetime
        
        return [
            Destino(1, "Playa Conchal", "Playa de arena blanca de conchas", 
                   "Guanacaste", 1, "img/playas/conchal3.jpg", 65000, "Entrada gratuita", datetime.now()),
            Destino(2, "Playa Manuel Antonio", "Playas dentro del parque nacional", 
                   "Puntarenas", 1, "img/playas/manuelantonio.webp", 40000, "Entrada al parque", datetime.now()),
            Destino(3, "Playa Punta Uva", "Aguas cristalinas", 
                   "Limón", 1, "img/playas/puntauva.jpg", 35000, "Acceso libre", datetime.now()),
            Destino(4, "Playa Cahuita", "Arrecife de coral", 
                   "Limón", 1, "img/playas/cahuita2.jpg", 38000, "Donación sugerida", datetime.now()),
            Destino(5, "Parque Nacional Volcán Arenal", "Volcán activo", 
                   "Alajuela", 2, "img/parques/Parquearenal1.jpg", 32000, "Entrada al parque", datetime.now()),
            Destino(6, "Rincón de la Vieja", "Volcanes y géiseres", 
                   "Guanacaste", 2, "img/parques/rincondelavieja1.jpg", 28000, "Entrada al parque", datetime.now()),
            Destino(7, "Tortuguero", "Canales y tortugas", 
                   "Limón", 2, "img/parques/tortuguero1.jpg", 35000, "Entrada al parque", datetime.now()),
            Destino(8, "Corcovado", "Biodiversidad única", 
                   "Puntarenas", 2, "img/parques/corcovado1.jpg", 42000, "Entrada al parque", datetime.now()),
            Destino(9, "La Fortuna", "Canyoning y aventura", 
                   "Alajuela", 3, "img/aventura/lafortuna1.jpg", 55000, "Acceso a cataratas", datetime.now()),
            Destino(10, "Monteverde", "Canopy y bosque nuboso", 
                    "Puntarenas", 3, "img/aventura/monteverde1.jpg", 45000, "Entrada a reserva", datetime.now()),
            Destino(11, "Jacó", "Surf y vida nocturna", 
                    "Puntarenas", 3, "img/aventura/jaco1.jpg", 38000, "Acceso a playa", datetime.now()),
            Destino(12, "Río Pacuare", "Rafting clase III-IV", 
                    "Limón", 3, "img/aventura/pacuare1.jpg", 65000, "Tour completo", datetime.now()),
            Destino(13, "Tabacón", "Aguas termales de lujo", 
                    "Alajuela", 4, "img/termales/Tabacon3.jpg", 60000, "Acceso a termales", datetime.now()),
            Destino(14, "Termales Baldi", "Aguas termales", 
                    "Alajuela", 4, "img/termales/baldi2.jpg", 35000, "Acceso a piscinas", datetime.now()),
            Destino(15, "Termales de Orosi", "Aguas termales tradicionales", 
                    "Cartago", 4, "img/termales/orosi.jpg", 30000, "Acceso a pozas", datetime.now()),
            Destino(16, "Termales Río Negro", "Aguas termales naturales", 
                    "Guanacaste", 4, "img/termales/rionegro.jpg", 28000, "Acceso a pozas", datetime.now()),
        ]
    
    def to_dict_list(self, destinos=None):
        """
        Convierte una lista de objetos Destino a lista de diccionarios
        
        Args:
            destinos: Lista de Destino (opcional, usa todos si no se especifica)
            
        Returns:
            Lista de diccionarios para JSON/templates
        """
        if destinos is None:
            destinos = self.obtener_todos()
        return [d.to_dict() for d in destinos]