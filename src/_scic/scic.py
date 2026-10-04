import math
import os
import pandas as pd
from src.gerador_dados import GeradorDados
from src.consulta_registros import Consulta
from src.analise import Indicadores
from src.modelo import Modelo
from src.buscador_modulos import Buscador
from src.gerenciador_alertas import GerenciadorAlertas


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

                    print(erro)

                    self.pausar()


        except InterromperLoop:
            print("Sistema encerrado.")


    def _consultar_registros(self):
        consulta = Consulta(self.__dados)
        consulta.run()


    def _analisar_indicadores(self):
        indicadores = Indicadores(self.__dados)
        indicadores.run()


    def _modelo_previsao(self):
        modelo = Modelo(self.__dados)
        opcoes = {
            "1": lambda: self._treinar_e_exibir_modelo(modelo),
            "2": lambda: self._exibir_previsoes_modelo(modelo),
            "3": lambda: self._exibir_dados_modelo(modelo),
            "4": lambda: self._prever_nova_observacao(modelo),
            "5": lambda: self._exibir_coeficientes_modelo(modelo),
            "6": lambda: self._gerar_graficos_modelo(modelo),
        }
        mensagem = """
---------------------
Modelo de previsão
---------------------
1 - Treinar e avaliar modelo
2 - Exibir previsões de todos os registros
3 - Exibir dados usados pelo modelo
4 - Prever nova observação
5 - Exibir coeficientes do modelo
6 - Gerar gráficos do modelo
7 - Voltar
"""
        while True:
            print(mensagem)
            opcao = input("Digite sua opção: ").strip()
            if opcao == "7":
                return
            acao = opcoes.get(opcao)
            if acao is None:
                print("Opção inválida. Digite um número entre 1 e 7.")
                continue
            try:
                acao()
            except ValueError as erro:
                print(f"Não foi possível executar a previsão: {erro}")
            self.pausar()

    @staticmethod
    def _treinar_e_exibir_modelo(modelo):
        metricas = modelo.treinamento_modelo()
        print("\nModelo treinado com termos lineares, quadráticos e logarítmicos.")
        print(f"Termos usados: {', '.join(modelo.variaveis_modelo)}")
        print("Avaliação no conjunto de teste:")
        for nome, valor in metricas.items():
            print(f"{nome}: {valor:.3f}")

    @staticmethod
    def _exibir_previsoes_modelo(modelo):
        previsoes = modelo.prever_todos_pontos()
        colunas = [
            "id", "ciclo", "modulo", "latencia_observada",
            "latencia_modelo_prevista", "erro_modelo_absoluto",
        ]
        print("\nPrevisões calculadas para todos os registros (amostra inicial):\n")
        print(previsoes[colunas].head(20).to_string(index=False))
        print(f"\nTotal de pontos previstos: {len(previsoes)}")

    @staticmethod
    def _exibir_dados_modelo(modelo):
        colunas = list(Modelo.VARIAVEIS_EXPLICATIVAS) + [Modelo.VARIAVEL_ALVO]
        print("\nDados usados pelo modelo (amostra inicial):\n")
        print(modelo.dados[colunas].head(20).to_string(index=False))
        print(f"\nTotal de registros disponíveis: {len(modelo.dados)}")

    @staticmethod
    def _prever_nova_observacao(modelo):
        print("\nInforme os valores observados para calcular a latência estimada.")
        variaveis = {}
        for variavel in Modelo.VARIAVEIS_EXPLICATIVAS:
            valor = float(input(f"{variavel.capitalize()}: ").strip())
            if not math.isfinite(valor):
                raise ValueError(f"{variavel} deve ser um número finito.")
            variaveis[variavel] = valor
        previsao = modelo.prever_instancia(variaveis)
        print(f"\nLatência prevista: {previsao:.2f} ms")

    @staticmethod
    def _exibir_coeficientes_modelo(modelo):
        print("\nCoeficientes do modelo (com variáveis normalizadas):")
        for nome, valor in modelo.obter_coeficientes().items():
            print(f"{nome}: {valor:.6f}")

    @staticmethod
    def _gerar_graficos_modelo(modelo):
        caminhos = modelo.gerar_graficos()
        print("\nGráficos gerados:")
        for nome, caminho in caminhos.items():
            print(f"- {nome}: {caminho}")

    def _gerenciar_alertas(self):
        alerta = GerenciadorAlertas(self.__dados)
        alerta.run()

    
    def _buscar_modulos(self):
        busca = Buscador(self.__dados)
        busca.run()


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
