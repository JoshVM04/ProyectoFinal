from pathlib import Path


class KnowledgeLoader:

    def __init__(self):

        # obtiene la carpeta app automáticamente
        base_dir = Path(__file__).resolve().parent.parent

        # entra a app/data/kwowledge
        self.ruta = base_dir / "data" / "kwowledge"

        print("RUTA USADA:", self.ruta)  # para verificar

        self.contenido = self.cargar()



    def cargar(self):

        conocimiento = ""


        if not self.ruta.exists():

            print("ERROR: carpeta knowledge no encontrada")

            return ""


        for archivo in self.ruta.glob("*.txt"):

            conocimiento += archivo.read_text(encoding="utf-8") + "\n"


        return conocimiento



    def obtener(self):

        return self.contenido