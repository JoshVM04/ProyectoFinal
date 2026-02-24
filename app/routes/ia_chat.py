from flask import Blueprint, render_template, request, jsonify
from app.utils.ia_engine import IAEngine


class IAChatRoutes:

    def __init__(self):

        self.blueprint = Blueprint(
            "ia_chat",
            __name__,
            url_prefix="/ia-chat"
        )

        self.engine = IAEngine()

        self.register_routes()


    def register_routes(self):

        self.blueprint.add_url_rule(
            "/",
            view_func=self.vista_chat
        )

        self.blueprint.add_url_rule(
            "/chat",
            view_func=self.chat,
            methods=["POST"]
        )


    def vista_chat(self):

        return render_template("ia_chat.html")


    def chat(self):

        data = request.get_json()

        pregunta = data.get("pregunta")

        respuesta = self.engine.generar_respuesta(pregunta)

        return jsonify({
            "respuesta": respuesta
        })