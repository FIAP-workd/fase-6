import os
import pandas as pd
from src.gerador_dados import GeradorDados

class InterromperLoop(Exception):
    """
    Classe de erro para interrupção do fluxo de while por dentro de uma segunda função.
    Essa classe funciona apenas para chamada do fim do código.
    """

    pass


class SCIC:

    def pausar(self):
        input("\nPressione ENTER para continuar...")


    def __init__(self):
        self.gera_dados = GeradorDados()
        self.__path_dados = self.gera_dados.output_path
        # Geração dos arquivos caso não existam.
        if not os.path.exists(self.__path_dados):
            self.gera_dados.gerar()
        self.__dados = pd.read_csv(self.__path_dados, sep=",")
        
        self.message_menu = """
==================================================
     SCIC - SISTEMA DE COMUNICAÇÃO
       INTERPLANETÁRIA DA COLÔNIA
             AURORA SIGER
==================================================

Escolha uma opção:

1 - Consultar registros
2 - Analisar indicadores
3 - Modelo de previsão
4 - Gerenciar Alertas
5 - Buscar módulos
6 - Analisar consumo e eletricidade
7 - Executar análise completa
8 - Informações do sistema
9 - Sair
"""

        self.dict_menu = {
            1: self._consultar_registros,
            2: self._analisar_indicadores,
            3: self._modelo_previsao,
            4: self._gerenciar_alertas,
            5: self._buscar_modulos,
            6: self._analisar_consumo_eletricidade,
            7: self._executar_analise_completa,
            8: self._informacoes_sistema,
            9: self._sair
        }
        
    
    def run(self):
        """
        Executa o menu principal do sistema com todas as execuções necessárias.
        """

        try:
            while True:
                print(self.message_menu)

                opcao = input("Digite sua opção: ").strip()

                try:
                    opcao = int(opcao)
                
                except ValueError:
                    print("Valor Inválido. \nDigite um número inteiro entre 1 e 9.")

                    self.pausar()
                    continue

                acao = self.dict_menu.get(opcao)

                if acao is None:
                    print(
                        "\nOpção inválida. "
                        "Digite um número entre 1 e 9."
                    )

                    self.pausar()
                    continue

                try:
                    acao()

                except InterromperLoop:
                    raise

                except Exception as erro:

                    print(
                        "\nOcorreu um erro inesperado. "
                    )

                    self.pausar()


        except InterromperLoop:
            print("Sistema encerrado.")


    def _consultar_registros(self):
        ...


    def _analisar_indicadores(self):
        ...


    def _modelo_previsao(self):
        ...

    def _gerenciar_alertas(self):
        ...

    
    def _buscar_modulos(self):
        ...


    def _analisar_consumo_eletricidade(self):
        ...

    def _executar_analise_completa(self):
        ...

    def _informacoes_sistema(self):
        ...

    def _sair(self):
        raise InterromperLoop


if __name__ == "__main__":
    scic = SCIC()
    scic.run()
