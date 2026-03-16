# utils/destino_engine.py
"""
Motor de Destinos - Versión para la base de datos SIMPLE
"""

class DestinoEngine:
    def __init__(self, db_connection=None):
        self.db = db_connection
        print(f"🔄 DestinoEngine inicializado. db: {self.db}")
    
    def obtener_por_id(self, destino_id):
        """Obtiene un destino específico por su ID"""
        print(f"🔍 Buscando destino ID: {destino_id}")
        
        if not self.db:
            print("❌ No hay conexión a la base de datos")
            return None
        
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Consulta simple sin JOIN para evitar errores
            cursor.execute("SELECT * FROM destinos WHERE id = %s", (destino_id,))
            destino = cursor.fetchone()
            cursor.close()
            
            if destino:
                print(f"✅ Destino encontrado: {destino['titulo']}")
                print(f"📸 Imagen: {destino.get('imagen')}")
                
                # Agregar campo categoria_nombre manualmente
                if destino['caterogoria_id'] == 1:
                    destino['categoria_nombre'] = 'Playas'
                elif destino['caterogoria_id'] == 2:
                    destino['categoria_nombre'] = 'Parques'
                elif destino['caterogoria_id'] == 3:
                    destino['categoria_nombre'] = 'Aventura'
                elif destino['caterogoria_id'] == 4:
                    destino['categoria_nombre'] = 'Termales'
                else:
                    destino['categoria_nombre'] = 'Otro'
                
                # Campo imagenes vacío para el template
                destino['imagenes'] = []
            else:
                print(f"❌ No se encontró destino con ID {destino_id}")
            
            return destino
            
        except Exception as e:
            print(f"❌ ERROR en obtener_por_id: {e}")
            return None
    
    def obtener_todos(self):
        """Obtiene todos los destinos"""
        if not self.db:
            return []
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM destinos")
            destinos = cursor.fetchall()
            cursor.close()
            
            # Agregar categoria_nombre a cada destino
            for d in destinos:
                if d['caterogoria_id'] == 1:
                    d['categoria_nombre'] = 'Playas'
                elif d['caterogoria_id'] == 2:
                    d['categoria_nombre'] = 'Parques'
                elif d['caterogoria_id'] == 3:
                    d['categoria_nombre'] = 'Aventura'
                elif d['caterogoria_id'] == 4:
                    d['categoria_nombre'] = 'Termales'
                else:
                    d['categoria_nombre'] = 'Otro'
            
            print(f"📋 Total destinos encontrados: {len(destinos)}")
            return destinos
        except Exception as e:
            print(f"❌ ERROR en obtener_todos: {e}")
            return []
    
    def obtener_por_categoria(self, categoria_id):
        """Filtra destinos por categoría"""
        if not self.db:
            return []
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM destinos WHERE caterogoria_id = %s", (categoria_id,))
            destinos = cursor.fetchall()
            cursor.close()
            return destinos
        except Exception as e:
            print(f"❌ ERROR en obtener_por_categoria: {e}")
            return []
    
    def obtener_por_provincia(self, provincia):
        """Filtra destinos por provincia"""
        if not self.db:
            return []
        
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM destinos WHERE provincia = %s", (provincia,))
            destinos = cursor.fetchall()
            cursor.close()
            return destinos
        except Exception as e:
            print(f"❌ ERROR en obtener_por_provincia: {e}")
            return []
    
    def buscar(self, termino):
        """Busca destinos por título o descripción"""
        if not self.db:
            return []
        
        try:
            cursor = self.db.cursor(dictionary=True)
            query = "SELECT * FROM destinos WHERE LOWER(titulo) LIKE %s OR LOWER(descripcion) LIKE %s"
            param = f"%{termino.lower()}%"
            cursor.execute(query, (param, param))
            destinos = cursor.fetchall()
            cursor.close()
            return destinos
        except Exception as e:
            print(f"❌ ERROR en buscar: {e}")
            return []