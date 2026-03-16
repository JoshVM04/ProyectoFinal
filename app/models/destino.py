# models/destino.py
class Destino:
    def __init__(self, id=None, titulo=None, descripcion=None, provincia=None, 
                 categoria_id=None, imagen_principal=None, costo_dia=None, 
                 que_incluye=None, fecha_creacion=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.provincia = provincia
        self.categoria_id = categoria_id
        self.imagen_principal = imagen_principal
        self.costo_dia = costo_dia
        self.que_incluye = que_incluye
        self.fecha_creacion = fecha_creacion
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'provincia': self.provincia,
            'categoria_id': self.categoria_id,
            'imagen_principal': self.imagen_principal,
            'costo_dia': self.costo_dia,
            'que_incluye': self.que_incluye,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
    
    def to_dict_completo(self):
        """Versión completa con datos de ejemplo para pruebas"""
        dict_base = self.to_dict()
        dict_base.update({
            'categoria_nombre': self._get_categoria_nombre(),
            'imagenes': [
                self.imagen_principal,
                self.imagen_principal.replace('.jpg', '2.jpg'),
                self.imagen_principal.replace('.jpg', '3.jpg')
            ],
            'actividades': self._get_actividades_ejemplo(),
            'restaurantes': self._get_restaurantes_ejemplo(),
            'hospedajes': self._get_hospedajes_ejemplo(),
            'rentacar': self._get_rentacar_ejemplo()
        })
        return dict_base
    
    def _get_categoria_nombre(self):
        categorias = {1: 'Playas', 2: 'Parques', 3: 'Aventura', 4: 'Termales'}
        return categorias.get(self.categoria_id, '')
    
    def _get_actividades_ejemplo(self):
        return [
            {'nombre': 'Tour guiado', 'descripcion_corta': 'Recorrido por el lugar', 
             'imagen': '/static/img/actividades/tour.jpg', 'link': '#'},
            {'nombre': 'Fotografía', 'descripcion_corta': 'Sesión de fotos profesional', 
             'imagen': '/static/img/actividades/foto.jpg', 'link': '#'}
        ]
    
    def _get_restaurantes_ejemplo(self):
        return [
            {'nombre': 'Restaurante Local', 'tipo_comida': 'Típica costarricense', 
             'imagen': '/static/img/restaurantes/local.jpg', 'link': '#'}
        ]
    
    def _get_hospedajes_ejemplo(self):
        return [
            {'nombre': 'Hotel Principal', 'tipo': 'Hotel', 'precio_noche': 80, 
             'imagen': '/static/img/hospedajes/hotel.jpg', 'link': '#'}
        ]
    
    def _get_rentacar_ejemplo(self):
        return [
            {'nombre': 'Rent a Car Local', 'ubicacion': 'Centro', 'precio_dia': 45, 
             'imagen': '/static/img/rentacar/local.jpg', 'link': '#'}
        ]