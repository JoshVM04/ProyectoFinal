import os


class KnowledgeLoader:

    def __init__(self):

        # Ruta base del knowledge
        self.base_path = "app/data/knowledge_base"


    def cargar_todo(self):

        conocimiento = ""

        # Recorre TODAS las carpetas y archivos
        for root, dirs, files in os.walk(self.base_path):

            for file in files:

                if file.endswith(".txt"):

                    ruta_archivo = os.path.join(root, file)

                    try:

                        with open(ruta_archivo, "r", encoding="utf-8") as f:

                            contenido = f.read()

                            conocimiento += "\n\n"
                            conocimiento += f"========== {file} ==========\n"
                            conocimiento += contenido

                    except Exception as e:

                        print(f"Error leyendo {file}: {e}")

        return conocimiento
