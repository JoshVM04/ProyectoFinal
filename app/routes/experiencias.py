# routes/experiencias.py
"""
Rutas de Experiencias - Controlador para manejar comentarios y reseñas
Misma estructura que IAChatRoutes para mantener consistencia
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.utils.experiencia_engine import ExperienciaEngine
from app.utils.destino_engine import DestinoEngine

class ExperienciasRoutes:
    """
    Controlador de experiencias - Maneja todas las rutas /experiencias/*
    Sigue el mismo patrón que IAChatRoutes y DestinosRoutes
    """
    
    def __init__(self, db_connection=None):
        """
        Inicializa el blueprint y los motores necesarios
        
        Args:
            db_connection: Conexión a la base de datos (opcional)
        """
        # ===== CONFIGURACIÓN DEL BLUEPRINT =====
        # Todas las rutas empezarán con /experiencias
        self.blueprint = Blueprint(
            "experiencias",
            __name__,
            url_prefix="/experiencias"
        )
        
        # ===== INICIALIZAR MOTORES =====
        # Motor de experiencias para comentarios
        self.engine = ExperienciaEngine(db_connection)
        # Motor de destinos para obtener lista de destinos en el formulario
        self.destino_engine = DestinoEngine(db_connection)
        
        # ===== REGISTRAR RUTAS =====
        self.register_routes()
    
    def register_routes(self):
        """
        Registra todas las rutas del controlador
        """
        
        # Ruta principal: /experiencias/
        # Muestra todos los comentarios
        self.blueprint.add_url_rule(
            "/",
            view_func=self.listar_todos
        )
        
        # Ruta para crear comentario: /experiencias/crear
        # Procesa el formulario de nuevo comentario
        self.blueprint.add_url_rule(
            "/crear",
            view_func=self.crear,
            methods=["POST"]
        )
        
        # Ruta para eliminar comentario: /experiencias/eliminar/<id>
        # Solo para el autor o el owner
        self.blueprint.add_url_rule(
            "/eliminar/<int:comentario_id>",
            view_func=self.eliminar,
            methods=["POST"]
        )
        
        # Ruta para ver comentarios de un destino: /experiencias/destino/<id>
        self.blueprint.add_url_rule(
            "/destino/<int:destino_id>",
            view_func=self.por_destino
        )
        
        # API endpoint: /experiencias/api/todos
        # Devuelve todos los comentarios en JSON
        self.blueprint.add_url_rule(
            "/api/todos",
            view_func=self.api_todos
        )
    
    def listar_todos(self):
        """
        Ruta: /experiencias/
        Método: GET
        Template: experiencias.html
        Muestra todos los comentarios
        """
        # Obtener todos los comentarios
        comentarios = self.engine.obtener_todos()
        
        # Obtener destinos para el formulario (si el usuario está logueado)
        destinos = []
        if 'usuario_id' in session:
            destinos = self.destino_engine.obtener_todos()
        
        return render_template(
            "experiencias.html",
            experiencias=self.engine.to_dict_list(comentarios),
            destinos=self.destino_engine.to_dict_list(destinos)
        )
    
    def por_destino(self, destino_id):
        """
        Ruta: /experiencias/destino/<int:destino_id>
        Método: GET
        Template: experiencias.html (filtrado)
        Muestra comentarios de un destino específico
        """
        # Obtener comentarios filtrados por destino
        comentarios = self.engine.obtener_por_destino(destino_id)
        
        # Obtener información del destino para el título
        destino = self.destino_engine.obtener_por_id(destino_id)
        titulo_destino = destino.titulo if destino else f"Destino {destino_id}"
        
        return render_template(
            "experiencias.html",
            experiencias=self.engine.to_dict_list(comentarios),
            filtro_destino=titulo_destino,
            destino_id=destino_id
        )
    
    def crear(self):
        """
        Ruta: /experiencias/crear
        Método: POST
        Procesa la creación de un nuevo comentario
        """
        # Verificar que el usuario está logueado
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        # Obtener datos del formulario
        destino_id = request.form.get('destino_id')
        comentario_texto = request.form.get('comentario')
        
        # Validar datos
        if not destino_id or not comentario_texto:
            return redirect(url_for('experiencias.listar_todos', error="Todos los campos son requeridos"))
        
        # Crear comentario
        resultado = self.engine.crear(
            usuario_id=session['usuario_id'],
            destino_id=int(destino_id),
            comentario_texto=comentario_texto
        )
        
        if resultado['exito']:
            # Redirigir a la página de experiencias con mensaje de éxito
            return redirect(url_for('experiencias.listar_todos', success=1))
        else:
            # Redirigir con error
            return redirect(url_for('experiencias.listar_todos', error=resultado['error']))
    
    def eliminar(self, comentario_id):
        """
        Ruta: /experiencias/eliminar/<int:comentario_id>
        Método: POST
        Elimina un comentario (solo autor o owner)
        """
        # Verificar que el usuario está logueado
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        # Verificar si el usuario es owner (por ahora no tenemos campo role)
        # TODO: Implementar sistema de roles
        es_owner = False  # Por defecto, no es owner
        
        # Intentar eliminar
        resultado = self.engine.eliminar(
            comentario_id=comentario_id,
            usuario_id=session['usuario_id'],
            es_owner=es_owner
        )
        
        if resultado['exito']:
            return redirect(url_for('experiencias.listar_todos', success="Comentario eliminado"))
        else:
            return redirect(url_for('experiencias.listar_todos', error=resultado['error']))
    
    def api_todos(self):
        """
        Ruta: /experiencias/api/todos
        Método: GET
        Respuesta: JSON
        Endpoint para APIs que necesiten los comentarios en formato JSON
        """
        comentarios = self.engine.obtener_todos()
        return jsonify(self.engine.to_dict_list(comentarios))