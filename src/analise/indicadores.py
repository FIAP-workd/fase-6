import pandas as pd

class Indicadores:
    def __init__(self, path_dados):
        self.__path_dados = path_dados
        if not os.path.exists(self.__path_dados):
            raise FileNotFoundError(f"Path {self.__path_dados} não encontrado.")
        self.__dados = pd.read_csv(self.__path_dados, sep=",")


    def latencia_observada_media(self):
        """
        Calcula a latência média observada dos dados.
        """
        return self.__dados["latencia observada"].mean()
    
    