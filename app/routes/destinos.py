# routes/destinos.py
"""
Rutas de Destinos - Controlador para manejar peticiones relacionadas con destinos
"""

from flask import Blueprint, render_template, request, jsonify
from app.utils.destino_engine import DestinoEngine

class DestinosRoutes:
    
    def __init__(self, db_connection=None):
        """
        Inicializa el blueprint y el motor de destinos
        
        Args:
            db_connection: Conexión a la base de datos (obligatoria)
        """
        print(f"🔄 Inicializando DestinosRoutes con db: {db_connection}")
        
        # ===== CONFIGURACIÓN DEL BLUEPRINT =====
        self.blueprint = Blueprint(
            "destinos",
            __name__,
            url_prefix="/destinos"
        )
        
        # ===== INICIALIZAR MOTOR CON LA CONEXIÓN =====
        self.engine = DestinoEngine(db_connection)
        
        # ===== REGISTRAR RUTAS =====
        self.register_routes()
    
    def register_routes(self):
        self.blueprint.add_url_rule("/", view_func=self.listar_todos)
        self.blueprint.add_url_rule("/<int:destino_id>", view_func=self.ver_detalle)
        self.blueprint.add_url_rule("/categoria/<int:categoria_id>", view_func=self.por_categoria)
        self.blueprint.add_url_rule("/provincia/<string:provincia>", view_func=self.por_provincia)
        self.blueprint.add_url_rule("/buscar", view_func=self.buscar, methods=["GET"])
        self.blueprint.add_url_rule("/api/todos", view_func=self.api_todos)
        self.blueprint.add_url_rule("/api/<int:destino_id>", view_func=self.api_detalle)
    
    def listar_todos(self):
        destinos = self.engine.obtener_todos()
        return render_template("destinos/lista.html", destinos=destinos, titulo="Todos los destinos")
    
    def ver_detalle(self, destino_id):
        print(f"🔍 Buscando destino ID: {destino_id}")
        destino = self.engine.obtener_por_id(destino_id)
        
        if not destino:
            print("❌ Destino NO encontrado")
            return "Destino no encontrado", 404
        
        print(f"✅ Destino encontrado: {destino.get('titulo')}")
        return render_template("destinos/detalle.html", destino=destino)
    
    def por_categoria(self, categoria_id):
        destinos = self.engine.obtener_por_categoria(categoria_id)
        categorias = {1: "Playas", 2: "Parques", 3: "Aventura", 4: "Termales"}
        return render_template("destinos/lista.html", destinos=destinos, titulo=categorias.get(categoria_id, "Categoría"))
    
    def por_provincia(self, provincia):
        destinos = self.engine.obtener_por_provincia(provincia)
        return render_template("destinos/lista.html", destinos=destinos, titulo=f"Destinos en {provincia.title()}")
    
    def buscar(self):
        termino = request.args.get('q', '')
        if not termino:
            return render_template("destinos/buscar.html", resultados=[], termino="")
        resultados = self.engine.buscar(termino)
        return render_template("destinos/buscar.html", resultados=resultados, termino=termino)
    
    def api_todos(self):
        return jsonify(self.engine.obtener_todos())
    
    def api_detalle(self, destino_id):
        destino = self.engine.obtener_por_id(destino_id)
        if not destino:
            return jsonify({'error': 'Destino no encontrado'}), 404
        return jsonify(destino)