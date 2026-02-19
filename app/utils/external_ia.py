from openai import OpenAI


class ExternalAI:


    def __init__(self):

        self.client = OpenAI(

            api_key="sk-6daf9ac195c14347920fffdce67a8641",

            base_url="https://api.deepseek.com"

        )


    def preguntar(self, pregunta):

        response = self.client.chat.completions.create(

            model="deepseek-chat",

            messages=[

                {

                    "role": "system",

                    "content": "Eres una guía turística experta en Costa Rica"

                },

                {

                    "role": "user",

                    "content": pregunta

                }

            ]

        )


        return response.choices[0].message.content
