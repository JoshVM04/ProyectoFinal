from app.utils.knowledge_loader import KnowledgeLoader

from app.utils.external_ia import ExternalAI


class IAEngine:


    def __init__(self):

        self.knowledge = KnowledgeLoader()

        self.external = ExternalAI()



    def generar_respuesta(self, pregunta):


        contexto = self.knowledge.obtener()

        respuesta = self.external.preguntar(

            pregunta,

            contexto

        )

        return respuesta

