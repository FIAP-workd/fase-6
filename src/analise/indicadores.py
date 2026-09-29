import pandas as pd


class Indicadores:
    def _pausar(self):
        input("\nPressione ENTER para continuar...")
    
    def __init__(self, dados):
        self.__dados = dados

    def latencia_observada_media(self):
        """
        Calcula a latência média observada dos dados.
        """
        return self.__dados["latencia_observada"].mean()
    

    def latencia_observada_maxima(self):
        """
        Calcula a latência máxima observada dos dados.
        """
        return self.__dados["latencia_observada"].max()
    

    def carga_media(self):
        """
        Calcula a carga média dos dados.
        """
        return self.__dados["carga"].mean()
    

    def potencia_media(self):
        """
        Calcula a potência média dos dados.
        """
        return self.__dados["potencia"].mean()
    

    def operacao_normal_percentual(self):
        """
        Calcula o percentual de operação normal dos dados.
        """
        total_registros = len(self.__dados)
        operacao_normal = len(self.__dados[self.__dados["status"] == "Normal"])
        return (operacao_normal / total_registros) * 100 if total_registros > 0 else 0
    
    def operacao_critica_percentual(self):
        """
        Calcula o percentual de operação crítica dos dados.
        """
        total_registros = len(self.__dados)
        operacao_critica = len(self.__dados[self.__dados["status"] == "Critico"])
        return (operacao_critica / total_registros) * 100 if total_registros > 0 else 0
    

    def operacao_alerta_percentual(self):
        """
        Calcula o percentual de operação em alerta dos dados.
        """
        total_registros = len(self.__dados)
        operacao_alerta = len(self.__dados[self.__dados["status"] == "Alerta"])
        return (operacao_alerta / total_registros) * 100 if total_registros > 0 else 0

    def calculo_erro_absoluto(self):
        return abs(self.__dados['latencia_observada'] - self.__dados['latencia_prevista'])

    def calculo_erro_relativo(self):
        return self.calculo_erro_absoluto() / self.__dados['latencia_observada']

    def _analise_indicadores(self):
        
        print("\nAnalisando indicadores...\n")
        print(f"Latência observada média: {self.latencia_observada_media():.2f} ms")
        print(f"Latência observada máxima: {self.latencia_observada_maxima():.2f} ms")
        print()
        print(f"Carga média: {self.carga_media():.2f} %")
        print(f"Potência média: {self.potencia_media():.2f} W")
        print()
        print(f"Operação normal: {self.operacao_normal_percentual():.2f} %")
        print(f"Operação crítica: {self.operacao_critica_percentual():.2f} %")
        print(f"Operação em alerta: {self.operacao_alerta_percentual():.2f} %")
        self._pausar()

    def _analise_erros(self):
        print("\nAnalisando erros...\n")
        erro_absoluto = self.calculo_erro_absoluto()
        erro_relativo = self.calculo_erro_relativo()
        print(f"Erro absoluto médio: {erro_absoluto.mean():.2f} ms")
        print(f"Erro relativo médio: {erro_relativo.mean():.2%}")
        self._pausar()

    def run(self):
        """
        Executa a análise dos indicadores e exibe os resultados.
        """
        self._analise_indicadores()
        self._analise_erros()