from flask import Blueprint, render_template, request, jsonify
from app.utils.ia_engine import IAEngine


class IAChatRoute:

    def __init__(self):

        self.bp = Blueprint(
            "ia_chat",
            __name__,
            url_prefix="/ia-chat"
        )

        self.ia = IAEngine()

        # Página HTML
        self.bp.route("/", methods=["GET"])(self.vista)

        # Ruta que responde preguntas
        self.bp.route("/preguntar", methods=["POST"])(self.preguntar)


    def vista(self):

        return render_template("ia_chat.html")


    def preguntar(self):

        data = request.get_json()

        pregunta = data.get("pregunta")

        respuesta = self.ia.responder(pregunta)

        return jsonify({
            "respuesta": respuesta
        })
