import pandas as pd


class Indicadores:
    def __init__(self, dados):
        self.__dados = dados

    def latencia_observada_media(self):
        """
        Calcula a latência média observada dos dados.
        """
        return self.__dados["latencia observada"].mean()
    
