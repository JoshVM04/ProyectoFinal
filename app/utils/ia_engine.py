from app.utils.knowledge_loader import KnowledgeLoader
from app.utils.external_ia import ExternalAI


class IAEngine:

    def __init__(self):

        self.loader = KnowledgeLoader()
        self.external_ai = ExternalAI()


    def responder(self, pregunta):

        conocimiento = self.loader.cargar_todo()

        prompt = f"""
Usa esta información:

{conocimiento}

Pregunta:
{pregunta}
"""

        respuesta = self.external_ai.preguntar(prompt)

        return respuesta


