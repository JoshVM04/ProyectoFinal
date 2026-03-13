# routes/destinos.py
"""
Rutas de Destinos - Controlador para manejar peticiones relacionadas con destinos
Misma estructura que IAChatRoutes para mantener consistencia
"""

from flask import Blueprint, render_template, request, jsonify
from app.utils.destino_engine import DestinoEngine

class DestinosRoutes:
    """
    Controlador de destinos - Maneja todas las rutas /destinos/*
    Sigue el mismo patrón que IAChatRoutes para mantener consistencia en el proyecto
    """
    
    def __init__(self, db_connection=None):
        """
        Inicializa el blueprint y el motor de destinos
        
        Args:
            db_connection: Conexión a la base de datos (opcional)
        """
        # ===== CONFIGURACIÓN DEL BLUEPRINT =====
        # Todas las rutas empezarán con /destinos
        self.blueprint = Blueprint(
            "destinos",
            __name__,
            url_prefix="/destinos"
        )
        
        # ===== INICIALIZAR MOTOR =====
        # El motor maneja toda la lógica de negocio
        self.engine = DestinoEngine(db_connection)
        
        # ===== REGISTRAR RUTAS =====
        # Aquí se conectan las URLs con los métodos de la clase
        self.register_routes()
    
    def register_routes(self):
        """
        Registra todas las rutas del controlador
        Cada ruta tiene su propia URL y método HTTP
        """
        
        # Ruta principal: /destinos/
        # Muestra todos los destinos en una lista
        self.blueprint.add_url_rule(
            "/",
            view_func=self.listar_todos
        )
        
        # Ruta de detalle: /destinos/<id>
        # Muestra la información completa de un destino
        self.blueprint.add_url_rule(
            "/<int:destino_id>",
            view_func=self.ver_detalle
        )
        
        # Ruta por categoría: /destinos/categoria/<id>
        # Filtra destinos por categoría (1: playas, 2: parques, etc)
        self.blueprint.add_url_rule(
            "/categoria/<int:categoria_id>",
            view_func=self.por_categoria
        )
        
        # Ruta por provincia: /destinos/provincia/<nombre>
        # Filtra destinos por provincia
        self.blueprint.add_url_rule(
            "/provincia/<string:provincia>",
            view_func=self.por_provincia
        )
        
        # Ruta de búsqueda: /destinos/buscar?q=termino
        # Busca destinos por título o descripción
        self.blueprint.add_url_rule(
            "/buscar",
            view_func=self.buscar,
            methods=["GET"]
        )
        
        # API endpoint: /destinos/api/todos
        # Devuelve todos los destinos en formato JSON
        self.blueprint.add_url_rule(
            "/api/todos",
            view_func=self.api_todos
        )
    
    def listar_todos(self):
        """
        Ruta: /destinos/
        Método: GET
        Template: destinos/lista.html
        Muestra todos los destinos en una página
        """
        # Obtener todos los destinos del motor
        destinos = self.engine.obtener_todos()
        
        # Renderizar template con la lista
        return render_template(
            "destinos/lista.html",
            destinos=self.engine.to_dict_list(destinos),
            titulo="Todos los destinos"
        )
    
    def ver_detalle(self, destino_id):
        """
        Ruta: /destinos/<int:destino_id>
        Método: GET
        Template: destinos/detalle.html (ya lo tienes)
        Muestra la información detallada de un destino específico
        """
        # Buscar el destino por ID
        destino = self.engine.obtener_por_id(destino_id)
        
        # Si no existe, mostrar página 404
        if not destino:
            return render_template("404.html", mensaje="Destino no encontrado"), 404
        
        # Renderizar template de detalle con el destino
        return render_template(
            "destinos/detalle.html",
            destino=destino.to_dict()
        )
    
    def por_categoria(self, categoria_id):
        """
        Ruta: /destinos/categoria/<int:categoria_id>
        Método: GET
        Template: destinos/lista.html
        Filtra destinos por categoría
        """
        # Obtener destinos filtrados por categoría
        destinos = self.engine.obtener_por_categoria(categoria_id)
        
        # Diccionario de nombres de categorías
        categorias = {
            1: "Playas",
            2: "Parques",
            3: "Aventura",
            4: "Termales"
        }
        
        # Renderizar template con los resultados filtrados
        return render_template(
            "destinos/lista.html",
            destinos=self.engine.to_dict_list(destinos),
            titulo=categorias.get(categoria_id, "Categoría")
        )
    
    def por_provincia(self, provincia):
        """
        Ruta: /destinos/provincia/<string:provincia>
        Método: GET
        Template: destinos/lista.html
        Filtra destinos por provincia
        """
        # Obtener destinos filtrados por provincia
        destinos = self.engine.obtener_por_provincia(provincia)
        
        # Renderizar template con los resultados
        return render_template(
            "destinos/lista.html",
            destinos=self.engine.to_dict_list(destinos),
            titulo=f"Destinos en {provincia.title()}"
        )
    
    def buscar(self):
        """
        Ruta: /destinos/buscar?q=termino
        Método: GET
        Template: destinos/buscar.html
        Busca destinos por término en título o descripción
        """
        # Obtener término de búsqueda de la URL
        termino = request.args.get('q', '')
        
        # Si no hay término, mostrar página vacía
        if not termino:
            return render_template("destinos/buscar.html", resultados=[], termino="")
        
        # Realizar la búsqueda
        resultados = self.engine.buscar(termino)
        
        # Renderizar template con resultados
        return render_template(
            "destinos/buscar.html",
            resultados=self.engine.to_dict_list(resultados),
            termino=termino
        )
    
    def api_todos(self):
        """
        Ruta: /destinos/api/todos
        Método: GET
        Respuesta: JSON
        Endpoint para APIs que necesiten los destinos en formato JSON
        """
        # Obtener todos los destinos
        destinos = self.engine.obtener_todos()
        
        # Devolver como JSON
        return jsonify(self.engine.to_dict_list(destinos))