# utils/destino_engine.py
"""
Motor de Destinos - Versión COMPLETA con todas las tablas relacionadas
"""

from app.models.destino import Destino

class DestinoEngine:
    def __init__(self, db_connection=None):
        self.db = db_connection
        self.usar_datos_prueba = db_connection is None
    
    def obtener_por_id(self, destino_id):
        """Obtiene un destino con TODA su información relacionada"""
        if self.usar_datos_prueba:
            return self._obtener_datos_prueba(destino_id)
        
        cursor = self.db.connection.cursor()
        
        # ===== 1. DATOS BÁSICOS DEL DESTINO + CATEGORÍA =====
        query_destino = """
            SELECT 
                d.id, d.titulo, d.descripcion_corta, d.descripcion_larga,
                d.provincia, d.canton, d.distancia_sanjose, d.tiempo_viaje,
                d.categoria_id, c.nombre as categoria_nombre, c.icono,
                d.imagen_principal, d.costo_promedio_dia, d.que_incluye,
                d.clima, d.temperatura_promedio, d.mejor_epoca,
                d.idioma, d.moneda, d.tipo_cambiario, d.electricidad, d.propina_recomendada
            FROM destinos d
            JOIN categorias c ON d.categoria_id = c.id
            WHERE d.id = %s
        """
        cursor.execute(query_destino, (destino_id,))
        destino_data = cursor.fetchone()
        
        if not destino_data:
            return None
        
        # ===== 2. IMÁGENES DE GALERÍA =====
        query_imagenes = """
            SELECT id, imagen, titulo, es_principal
            FROM imagenes_destino
            WHERE destino_id = %s
            ORDER BY es_principal DESC, id ASC
        """
        cursor.execute(query_imagenes, (destino_id,))
        imagenes = cursor.fetchall()
        
        # ===== 3. ACTIVIDADES =====
        query_actividades = """
            SELECT id, nombre, descripcion_corta, descripcion_larga,
                   duracion_horas, dificultad, precio_desde, imagen, link, recomendado
            FROM actividades
            WHERE destino_id = %s
            ORDER BY recomendado DESC, precio_desde ASC
        """
        cursor.execute(query_actividades, (destino_id,))
        actividades = cursor.fetchall()
        
        # ===== 4. RESTAURANTES =====
        query_restaurantes = """
            SELECT id, nombre, tipo_comida, especialidad, rango_precios,
                   horario, telefono, direccion, imagen, link, puntuacion
            FROM restaurantes
            WHERE destino_id = %s
            ORDER BY puntuacion DESC
        """
        cursor.execute(query_restaurantes, (destino_id,))
        restaurantes = cursor.fetchall()
        
        # ===== 5. HOSPEDAJES =====
        query_hospedajes = """
            SELECT id, nombre, tipo, categoria, precio_noche_desde, precio_noche_hasta,
                   servicios, telefono, direccion, imagen, link, puntuacion
            FROM hospedajes
            WHERE destino_id = %s
            ORDER BY puntuacion DESC
        """
        cursor.execute(query_hospedajes, (destino_id,))
        hospedajes = cursor.fetchall()
        
        # ===== 6. RENTA DE CARROS =====
        query_rentacar = """
            SELECT id, nombre, ubicacion, direccion, telefono,
                   precio_dia_desde, precio_dia_hasta, tipo_vehiculos,
                   seguro_incluido, kilometraje_libre, imagen, link
            FROM rentacar
            WHERE destino_id = %s
        """
        cursor.execute(query_rentacar, (destino_id,))
        rentacar = cursor.fetchall()
        
        # ===== 7. CONSTRUIR OBJETO COMPLETO =====
        destino = {
            # Datos básicos
            'id': destino_data[0],
            'titulo': destino_data[1],
            'descripcion_corta': destino_data[2],
            'descripcion': destino_data[3],  # descripcion_larga
            'provincia': destino_data[4],
            'canton': destino_data[5],
            'distancia_sanjose': destino_data[6],
            'tiempo_viaje': destino_data[7],
            'categoria_id': destino_data[8],
            'categoria_nombre': destino_data[9],
            'categoria_icono': destino_data[10],
            'imagen_principal': destino_data[11],
            'costo_dia': destino_data[12],  # costo_promedio_dia
            'que_incluye': destino_data[13],
            'clima': destino_data[14],
            'temperatura_promedio': destino_data[15],
            'mejor_epoca': destino_data[16],
            'idioma': destino_data[17],
            'moneda': destino_data[18],
            'tipo_cambiario': destino_data[19],
            'electricidad': destino_data[20],
            'propina_recomendada': destino_data[21],
            
            # Imágenes de galería
            'imagenes': [
                {
                    'id': img[0],
                    'url': img[1],
                    'titulo': img[2],
                    'es_principal': bool(img[3])
                } for img in imagenes
            ],
            
            # Actividades
            'actividades': [
                {
                    'id': act[0],
                    'nombre': act[1],
                    'descripcion_corta': act[2],
                    'descripcion_larga': act[3],
                    'duracion_horas': act[4],
                    'dificultad': act[5],
                    'precio_desde': act[6],
                    'imagen': act[7],
                    'link': act[8],
                    'recomendado': bool(act[9])
                } for act in actividades
            ],
            
            # Restaurantes
            'restaurantes': [
                {
                    'id': res[0],
                    'nombre': res[1],
                    'tipo_comida': res[2],
                    'especialidad': res[3],
                    'rango_precios': res[4],
                    'horario': res[5],
                    'telefono': res[6],
                    'direccion': res[7],
                    'imagen': res[8],
                    'link': res[9],
                    'puntuacion': float(res[10]) if res[10] else None
                } for res in restaurantes
            ],
            
            # Hospedajes
            'hospedajes': [
                {
                    'id': hos[0],
                    'nombre': hos[1],
                    'tipo': hos[2],
                    'categoria': hos[3],
                    'precio_noche_desde': hos[4],
                    'precio_noche_hasta': hos[5],
                    'servicios': hos[6],
                    'telefono': hos[7],
                    'direccion': hos[8],
                    'imagen': hos[9],
                    'link': hos[10],
                    'puntuacion': float(hos[11]) if hos[11] else None
                } for hos in hospedajes
            ],
            
            # Renta de carros
            'rentacar': [
                {
                    'id': ren[0],
                    'nombre': ren[1],
                    'ubicacion': ren[2],
                    'direccion': ren[3],
                    'telefono': ren[4],
                    'precio_dia_desde': ren[5],
                    'precio_dia_hasta': ren[6],
                    'tipo_vehiculos': ren[7],
                    'seguro_incluido': bool(ren[8]),
                    'kilometraje_libre': bool(ren[9]),
                    'imagen': ren[10],
                    'link': ren[11]
                } for ren in rentacar
            ]
        }
        
        # Si no hay imágenes, usar la principal repetida
        if not destino['imagenes']:
            destino['imagenes'] = [
                {'url': destino['imagen_principal'], 'titulo': 'Vista principal', 'es_principal': True},
                {'url': destino['imagen_principal'], 'titulo': 'Vista adicional', 'es_principal': False},
                {'url': destino['imagen_principal'], 'titulo': 'Vista adicional', 'es_principal': False}
            ]
        
        return destino
    
    def obtener_todos(self):
        """Obtiene lista básica de destinos (para listados)"""
        if self.usar_datos_prueba:
            return []
        
        cursor = self.db.connection.cursor()
        query = """
            SELECT 
                d.id, d.titulo, d.descripcion_corta, d.provincia,
                d.categoria_id, c.nombre as categoria_nombre,
                d.imagen_principal, d.costo_promedio_dia
            FROM destinos d
            JOIN categorias c ON d.categoria_id = c.id
            ORDER BY d.id
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        destinos = []
        for row in resultados:
            destinos.append({
                'id': row[0],
                'titulo': row[1],
                'descripcion_corta': row[2],
                'provincia': row[3],
                'categoria_id': row[4],
                'categoria_nombre': row[5],
                'imagen_principal': row[6],
                'costo_dia': row[7]
            })
        
        return destinos