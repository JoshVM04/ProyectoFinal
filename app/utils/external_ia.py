from openai import OpenAI


class ExternalAI:


    def __init__(self):

        self.client = OpenAI(

            api_key="sk-6daf9ac195c14347920fffdce67a8641",

            base_url="https://api.deepseek.com"

        )



    def preguntar(self, pregunta, contexto):


        respuesta = self.client.chat.completions.create(

            model="deepseek-chat",

            messages=[

                {
                    "role": "system",
                    "content": f"""
                    Eres Nómada, guía turístico de Costa Rica.

                    Usa este conocimiento:

                    {contexto}

                    """
                },

                {
                    "role": "user",
                    "content": pregunta
                }

            ]

        )


        return respuesta.choices[0].message.content