from flask import Blueprint, request, jsonify
from app.utils.ia_engine import IAEngine


class IAChatRoute:

    def __init__(self):

        self.bp = Blueprint(
            'ia_chat',
            __name__,
            url_prefix="/ia"
        )

        self.engine = IAEngine()

        self.bp.route("/chat", methods=["POST"])(self.chat)


    def chat(self):

        data = request.get_json()

        pregunta = data.get("pregunta")

        respuesta = self.engine.generar_respuesta(pregunta)

        return jsonify({
            "respuesta": respuesta
        })