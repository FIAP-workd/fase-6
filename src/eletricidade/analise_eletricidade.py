import pandas as pd


class AnaliseEletricidade:
    """
    Realiza a análise dos dados elétricos dos módulos da Aurora Siger.

    A classe recebe os dados simulados do SCIC e calcula indicadores
    relacionados à tensão, corrente e potência elétrica.
    """

    def __init__(self, dados):
        """
        Inicializa a análise.

        Parameters
        ----------
        dados : pandas.DataFrame
            Dados simulados contendo, no mínimo:
            - modulo
            - tensao
            - corrente
        """

        self.dados = self._preparar_dados(dados)
        self.resultados = {}

    # ==========================================================
    # PREPARAÇÃO DOS DADOS
    # ==========================================================

    def _preparar_dados(self, dados):
        """
        Converte os dados recebidos para DataFrame e valida
        as colunas necessárias.
        """

        if isinstance(dados, pd.DataFrame):
            df = dados.copy()

        elif isinstance(dados, list):
            df = pd.DataFrame(dados)

        else:
            raise TypeError(
                "Os dados devem ser um pandas.DataFrame "
                "ou uma lista de dicionários."
            )

        colunas_obrigatorias = {
            "tensao",
            "corrente"
        }

        colunas_ausentes = colunas_obrigatorias - set(df.columns)

        if colunas_ausentes:
            raise ValueError(
                f"Colunas obrigatórias ausentes: {colunas_ausentes}"
            )

        return df

    # ==========================================================
    # CÁLCULO DA POTÊNCIA
    # ==========================================================

    def _calcular_potencia(self):
        """
        Calcula a potência elétrica utilizando:

            P = V × I

        Onde:
            P = potência
            V = tensão
            I = corrente
        """

        self.dados["potencia_calculada"] = (
            self.dados["tensao"] *
            self.dados["corrente"]
        )

    # ==========================================================
    # INDICADORES GERAIS
    # ==========================================================

    def _calcular_indicadores(self):
        """
        Calcula os principais indicadores elétricos.
        """

        indicadores = {
            "tensao_media": self.dados["tensao"].mean(),
            "tensao_minima": self.dados["tensao"].min(),
            "tensao_maxima": self.dados["tensao"].max(),

            "corrente_media": self.dados["corrente"].mean(),
            "corrente_minima": self.dados["corrente"].min(),
            "corrente_maxima": self.dados["corrente"].max(),

            "potencia_media": self.dados["potencia_calculada"].mean(),
            "potencia_minima": self.dados["potencia_calculada"].min(),
            "potencia_maxima": self.dados["potencia_calculada"].max(),

            "potencia_total": self.dados["potencia_calculada"].sum()
        }

        self.resultados["indicadores"] = indicadores

    # ==========================================================
    # ANÁLISE POR MÓDULO
    # ==========================================================

    def _analisar_modulos(self):
        """
        Calcula o consumo médio e máximo por módulo.

        Caso a coluna 'modulo' não exista, a análise por módulo
        não será realizada.
        """

        if "modulo" not in self.dados.columns:
            self.resultados["por_modulo"] = None
            return

        analise = (
            self.dados
            .groupby("modulo")
            .agg(
                potencia_media=("potencia_calculada", "mean"),
                potencia_maxima=("potencia_calculada", "max"),
                tensao_media=("tensao", "mean"),
                corrente_media=("corrente", "mean")
            )
            .sort_values(
                by="potencia_media",
                ascending=False
            )
        )

        self.resultados["por_modulo"] = analise

    # ==========================================================
    # MAIORES CONSUMOS
    # ==========================================================

    def _identificar_maiores_consumos(self, quantidade=5):
        """
        Identifica os registros com maior potência elétrica.
        """

        maiores = (
            self.dados
            .sort_values(
                by="potencia_calculada",
                ascending=False
            )
            .head(quantidade)
        )

        self.resultados["maiores_consumos"] = maiores

    # ==========================================================
    # CONVERSÃO DE BASE
    # ==========================================================

    def _converter_base(self):
        """
        Realiza uma conversão simples de potência para
        representação inteira em decimal, binário e hexadecimal.

        A conversão tem finalidade demonstrativa para a parte
        de organização de computadores e representação de dados.
        """

        potencia_media = self.resultados["indicadores"]["potencia_media"]

        valor_decimal = int(round(potencia_media))

        conversao = {
            "decimal": valor_decimal,
            "binario": bin(valor_decimal),
            "hexadecimal": hex(valor_decimal)
        }

        self.resultados["conversao_base"] = conversao

    # ==========================================================
    # EXIBIÇÃO DOS RESULTADOS
    # ==========================================================

    def _exibir_resultados(self):
        """
        Exibe os resultados da análise no terminal.
        """

        indicadores = self.resultados["indicadores"]

        print("\n" + "=" * 60)
        print("        ANÁLISE DE CONSUMO E ELETRICIDADE")
        print("=" * 60)

        print("\n--- TENSÃO ---")
        print(f"Tensão média : {indicadores['tensao_media']:.2f} V")
        print(f"Tensão mínima: {indicadores['tensao_minima']:.2f} V")
        print(f"Tensão máxima: {indicadores['tensao_maxima']:.2f} V")

        print("\n--- CORRENTE ---")
        print(f"Corrente média : {indicadores['corrente_media']:.2f} A")
        print(f"Corrente mínima: {indicadores['corrente_minima']:.2f} A")
        print(f"Corrente máxima: {indicadores['corrente_maxima']:.2f} A")

        print("\n--- POTÊNCIA ---")
        print(f"Potência média : {indicadores['potencia_media']:.2f} W")
        print(f"Potência mínima: {indicadores['potencia_minima']:.2f} W")
        print(f"Potência máxima: {indicadores['potencia_maxima']:.2f} W")
        print(f"Potência total : {indicadores['potencia_total']:.2f} W")

        self._pausar()
        conversao = self.resultados["conversao_base"]

        print("\n--- REPRESENTAÇÃO DE DADOS ---")
        print(f"Decimal      : {conversao['decimal']}")
        print(f"Binário      : {conversao['binario']}")
        print(f"Hexadecimal  : {conversao['hexadecimal']}")

        self._pausar()
        maiores = self.resultados["maiores_consumos"]

        print("\n--- MAIORES CONSUMOS ---")

        colunas = [
            coluna
            for coluna in [
                "modulo",
                "tensao",
                "corrente",
                "potencia_calculada"
            ]
            if coluna in maiores.columns
        ]

        print(
            maiores[colunas]
            .to_string(index=False)
        )

        self._pausar()
        if self.resultados["por_modulo"] is not None:

            print("\n--- CONSUMO MÉDIO POR MÓDULO ---")

            print(
                self.resultados["por_modulo"]
                .to_string()
            )
            self._pausar()

        print("\n" + "=" * 60)

    # ==========================================================
    # EXECUÇÃO PRINCIPAL
    # ==========================================================

    def run(self):
        """
        Executa automaticamente todas as etapas da análise elétrica.

        Retorna
        -------
        dict
            Dicionário contendo todos os resultados calculados.
        """

        self._calcular_potencia()
        self._calcular_indicadores()
        self._analisar_modulos()
        self._identificar_maiores_consumos()
        self._converter_base()
        self._exibir_resultados()

        return self.resultados

    def _pausar(self):
        input("Pressione ENTER para continuar")


if __name__ == '__main__':
    a = AnaliseEletricidade(pd.read_csv(r"C:\Users\luis\Desktop\faculdade\fase-6\.dados\dados_aurora_siger.csv"))
    k = a.run()
    # print(k)