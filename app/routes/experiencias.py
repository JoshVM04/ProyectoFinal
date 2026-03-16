# routes/experiencias.py
"""
Rutas de Experiencias - Controlador para manejar comentarios y reseñas
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.utils.experiencia_engine import ExperienciaEngine
from app.utils.destino_engine import DestinoEngine

class ExperienciasRoutes:
    
    def __init__(self, db_connection=None):
        """
        Inicializa el blueprint y los motores necesarios
        
        Args:
            db_connection: Conexión a la base de datos (opcional)
        """
        # ===== CONFIGURACIÓN DEL BLUEPRINT =====
        self.blueprint = Blueprint(
            "experiencias",
            __name__,
            url_prefix="/experiencias"
        )
        
        # ===== INICIALIZAR MOTORES =====
        self.engine = ExperienciaEngine(db_connection)
        self.destino_engine = DestinoEngine(db_connection)
        
        # ===== REGISTRAR RUTAS =====
        self.register_routes()
    
    def register_routes(self):
        """Registra todas las rutas del controlador"""
        
        self.blueprint.add_url_rule("/", view_func=self.listar_todos)
        self.blueprint.add_url_rule("/crear", view_func=self.crear, methods=["POST"])
        self.blueprint.add_url_rule("/eliminar/<int:comentario_id>", view_func=self.eliminar, methods=["POST"])
        self.blueprint.add_url_rule("/destino/<int:destino_id>", view_func=self.por_destino)
        self.blueprint.add_url_rule("/api/todos", view_func=self.api_todos)
    
    def listar_todos(self):
        """
        Ruta: /experiencias/
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
            experiencias=comentarios,  # ← SIN to_dict_list
            destinos=destinos           # ← SIN to_dict_list
        )
    
    def por_destino(self, destino_id):
        """
        Ruta: /experiencias/destino/<int:destino_id>
        Muestra comentarios de un destino específico
        """
        comentarios = self.engine.obtener_por_destino(destino_id)
        
        destino = self.destino_engine.obtener_por_id(destino_id)
        titulo_destino = destino['titulo'] if destino else f"Destino {destino_id}"
        
        return render_template(
            "experiencias.html",
            experiencias=comentarios,  # ← SIN to_dict_list
            filtro_destino=titulo_destino,
            destino_id=destino_id
        )
    
    def crear(self):
        """
        Ruta: /experiencias/crear
        Procesa la creación de un nuevo comentario
        """
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        destino_id = request.form.get('destino_id')
        comentario_texto = request.form.get('comentario')
        
        if not destino_id or not comentario_texto:
            return redirect(url_for('experiencias.listar_todos', error="Todos los campos son requeridos"))
        
        resultado = self.engine.crear(
            usuario_id=session['usuario_id'],
            destino_id=int(destino_id),
            comentario_texto=comentario_texto
        )
        
        if resultado['exito']:
            return redirect(url_for('experiencias.listar_todos', success=1))
        else:
            return redirect(url_for('experiencias.listar_todos', error=resultado['error']))
    
    def eliminar(self, comentario_id):
        """
        Ruta: /experiencias/eliminar/<int:comentario_id>
        Elimina un comentario (solo autor)
        """
        if 'usuario_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        
        resultado = self.engine.eliminar(
            comentario_id=comentario_id,
            usuario_id=session['usuario_id']
        )
        
        if resultado['exito']:
            return redirect(url_for('experiencias.listar_todos', success="Comentario eliminado"))
        else:
            return redirect(url_for('experiencias.listar_todos', error=resultado['error']))
    
    def api_todos(self):
        """
        Ruta: /experiencias/api/todos
        Respuesta: JSON
        """
        comentarios = self.engine.obtener_todos()
        return jsonify(comentarios)  # ← SIN to_dict_list