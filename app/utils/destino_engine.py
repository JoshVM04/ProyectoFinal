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
        # SELECT * FROM destinos ORDER BY titulo
        cursor = self.db.cursor()
        cursor.execute("SELECT id, titulo, descripcion, provincia, caterogoria_id, imagen, fecha_creacion FROM destinos ORDER BY titulo")
        resultados = cursor.fetchall()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row[0],
                titulo=row[1],
                descripcion=row[2],
                provincia=row[3],
                caterogoria_id=row[4],
                imagen=row[5],
                fecha_creacion=row[6]
            )
            destinos.append(destino)
        
        return destinos
    
    def obtener_por_id(self, destino_id):
        """
        Obtiene un destino específico por su ID
        
        Args:
            destino_id: ID del destino a buscar
            
        Returns:
            Objeto Destino o None si no existe
        """
        if self.usar_datos_prueba:
            destinos = self._obtener_datos_prueba()
            for d in destinos:
                if d.id == destino_id:
                    return d
            return None
        
        # ===== CONSULTA SQL =====
        # SELECT * FROM destinos WHERE id = ?
        cursor = self.db.cursor()
        cursor.execute("SELECT id, titulo, descripcion, provincia, caterogoria_id, imagen, fecha_creacion FROM destinos WHERE id = %s", (destino_id,))
        row = cursor.fetchone()
        
        if row:
            return Destino(
                id=row[0],
                titulo=row[1],
                descripcion=row[2],
                provincia=row[3],
                caterogoria_id=row[4],
                imagen=row[5],
                fecha_creacion=row[6]
            )
        return None
    
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
            return [d for d in todos if d.caterogoria_id == categoria_id]
        
        # ===== CONSULTA SQL =====
        # SELECT * FROM destinos WHERE caterogoria_id = ?
        cursor = self.db.cursor()
        cursor.execute("SELECT id, titulo, descripcion, provincia, caterogoria_id, imagen, fecha_creacion FROM destinos WHERE caterogoria_id = %s", (categoria_id,))
        resultados = cursor.fetchall()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row[0],
                titulo=row[1],
                descripcion=row[2],
                provincia=row[3],
                caterogoria_id=row[4],
                imagen=row[5],
                fecha_creacion=row[6]
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
        
        # ===== CONSULTA SQL =====
        # SELECT * FROM destinos WHERE provincia = ?
        cursor = self.db.cursor()
        cursor.execute("SELECT id, titulo, descripcion, provincia, caterogoria_id, imagen, fecha_creacion FROM destinos WHERE provincia = %s", (provincia,))
        resultados = cursor.fetchall()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row[0],
                titulo=row[1],
                descripcion=row[2],
                provincia=row[3],
                caterogoria_id=row[4],
                imagen=row[5],
                fecha_creacion=row[6]
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
        
        # ===== CONSULTA SQL =====
        # SELECT * FROM destinos WHERE LOWER(titulo) LIKE ? OR LOWER(descripcion) LIKE ?
        cursor = self.db.cursor()
        query = "SELECT id, titulo, descripcion, provincia, caterogoria_id, imagen, fecha_creacion FROM destinos WHERE LOWER(titulo) LIKE %s OR LOWER(descripcion) LIKE %s"
        param = f"%{termino.lower()}%"
        cursor.execute(query, (param, param))
        resultados = cursor.fetchall()
        
        destinos = []
        for row in resultados:
            destino = Destino(
                id=row[0],
                titulo=row[1],
                descripcion=row[2],
                provincia=row[3],
                caterogoria_id=row[4],
                imagen=row[5],
                fecha_creacion=row[6]
            )
            destinos.append(destino)
        
        return destinos
    
    def _obtener_datos_prueba(self):
        """
        Método privado para pruebas sin BD
        Retorna una lista de destinos quemados basados en tu JSON
        """
        from datetime import datetime
        
        return [
            Destino(1, "Playa Conchal", "Playa de arena blanca de conchas", 
                   "Guanacaste", 1, "/static/images/playa-conchal.jpg", datetime.now()),
            Destino(2, "Playa Tamarindo", "Surf y vida nocturna", 
                   "Guanacaste", 1, "/static/images/tamarindo.jpg", datetime.now()),
            Destino(3, "Playa Punta Uva", "Aguas cristalinas", 
                   "Limón", 1, "/static/images/punta-uva.jpg", datetime.now()),
            Destino(4, "Playa Cahuita", "Arrecife de coral", 
                   "Limón", 1, "/static/images/cahuita.jpg", datetime.now()),
            Destino(5, "Volcán Arenal", "Volcán activo", 
                   "Alajuela", 2, "/static/images/arenal.jpg", datetime.now()),
            Destino(6, "Rincón de la Vieja", "Volcanes y géiseres", 
                   "Guanacaste", 2, "/static/images/rincon.jpg", datetime.now()),
            Destino(7, "Tortuguero", "Canales y tortugas", 
                   "Limón", 2, "/static/images/tortuguero.jpg", datetime.now()),
            Destino(8, "Corcovado", "Biodiversidad única", 
                   "Puntarenas", 2, "/static/images/corcovado.jpg", datetime.now()),
            Destino(9, "La Fortuna", "Canyoning", 
                   "Alajuela", 3, "/static/images/fortuna.jpg", datetime.now()),
            Destino(10, "Monteverde", "Canopy", 
                    "Puntarenas", 3, "/static/images/monteverde.jpg", datetime.now()),
            Destino(11, "Jacó", "Surf", 
                    "Puntarenas", 3, "/static/images/jaco.jpg", datetime.now()),
            Destino(12, "Río Pacuare", "Rafting", 
                    "Cartago", 3, "/static/images/pacuare.jpg", datetime.now()),
            Destino(13, "Tabacón", "Aguas termales de lujo", 
                    "Alajuela", 4, "/static/images/tabacon.jpg", datetime.now()),
            Destino(14, "Baldi", "Aguas termales", 
                    "Alajuela", 4, "/static/images/baldi.jpg", datetime.now()),
            Destino(15, "Orosi", "Aguas termales tradicionales", 
                    "Cartago", 4, "/static/images/orosi.jpg", datetime.now()),
            Destino(16, "Río Negro", "Aguas termales naturales", 
                    "Guanacaste", 4, "/static/images/rio-negro.jpg", datetime.now()),
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