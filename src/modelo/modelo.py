"""Modelo de regressão para a latência dos módulos da Aurora Siger.

O módulo usa apenas a biblioteca padrão (além do ``pandas``, já usado pelo
projeto).  Isso mantém a demonstração do modelo executável no ambiente do
projeto sem exigir uma dependência externa de aprendizado de máquina.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Modelo:
    """Regressão múltipla com termos não lineares para ``latencia_observada``.

    As variáveis explicativas seguem o plano de desenvolvimento: carga,
    tensão, corrente e ciclo. A potência não é incluída, pois ela é derivada
    de tensão e corrente e introduziria redundância matemática no ajuste.
    """

    VARIAVEIS_EXPLICATIVAS = ("carga", "tensao", "corrente", "ciclo")
    VARIAVEL_ALVO = "latencia_observada"
    TRANSFORMACOES_DISPONIVEIS = ("quadratico", "logaritmico")

    def __init__(
        self,
        dados: pd.DataFrame,
        percentual_teste: float = 0.2,
        seed: int = 42,
        transformacoes: tuple[str, ...] = ("quadratico", "logaritmico"),
    ) -> None:
        if not 0 < percentual_teste < 1:
            raise ValueError("percentual_teste deve estar entre 0 e 1.")

        self.dados = dados.copy()
        self.percentual_teste = percentual_teste
        self.seed = seed
        self.transformacoes = tuple(transformacoes)
        transformacoes_invalidas = (
            set(self.transformacoes) - set(self.TRANSFORMACOES_DISPONIVEIS)
        )
        if transformacoes_invalidas:
            nomes = ", ".join(sorted(transformacoes_invalidas))
            raise ValueError(f"Transformações não suportadas: {nomes}.")
        self.variaveis_modelo = self._criar_variaveis_modelo()
        self.coeficientes: dict[str, float] | None = None
        self.intercepto: float | None = None
        self.metricas: dict[str, float] | None = None
        self.previsoes: pd.DataFrame | None = None
        self._medias: dict[str, float] = {}
        self._escalas: dict[str, float] = {}

        self._validar_dados()

    def _validar_dados(self) -> None:
        colunas_necessarias = set(self.VARIAVEIS_EXPLICATIVAS) | {
            self.VARIAVEL_ALVO
        }
        faltantes = colunas_necessarias - set(self.dados.columns)
        if faltantes:
            nomes = ", ".join(sorted(faltantes))
            raise ValueError(f"Dados sem as colunas obrigatórias: {nomes}.")

        colunas_numericas = list(self.VARIAVEIS_EXPLICATIVAS) + [
            self.VARIAVEL_ALVO
        ]
        dados_numericos = self.dados[colunas_numericas].apply(
            pd.to_numeric, errors="coerce"
        )
        if dados_numericos.isna().any().any():
            raise ValueError("As variáveis do modelo devem ser numéricas e preenchidas.")
        variaveis_explicativas = dados_numericos[list(self.VARIAVEIS_EXPLICATIVAS)]
        if "logaritmico" in self.transformacoes and (variaveis_explicativas <= 0).any().any():
            raise ValueError(
                "A transformação logarítmica exige variáveis explicativas maiores que zero."
            )
        if len(self.dados) < len(self.variaveis_modelo) + 2:
            raise ValueError("Não há registros suficientes para treinar o modelo.")

        self.dados[colunas_numericas] = dados_numericos

    def treinamento_modelo(self) -> dict[str, float]:
        """Treina o modelo e retorna as métricas calculadas no conjunto de teste."""
        indices = list(range(len(self.dados)))
        random.Random(self.seed).shuffle(indices)
        tamanho_teste = max(1, round(len(indices) * self.percentual_teste))
        tamanho_teste = min(tamanho_teste, len(indices) - 1)
        indices_teste = indices[:tamanho_teste]
        indices_treino = indices[tamanho_teste:]

        if len(indices_treino) < len(self.variaveis_modelo) + 1:
            raise ValueError("Não há registros de treino suficientes para a regressão.")

        treino = self.dados.iloc[indices_treino]
        self._calcular_normalizacao(treino)
        matriz = [self._linha_normalizada(linha) for _, linha in treino.iterrows()]
        alvo = [float(valor) for valor in treino[self.VARIAVEL_ALVO]]
        parametros = self._resolver_minimos_quadrados(matriz, alvo)

        self.intercepto = parametros[0]
        self.coeficientes = dict(zip(self.variaveis_modelo, parametros[1:]))
        self.prever_todos_pontos()

        observados = self.dados.iloc[indices_teste][self.VARIAVEL_ALVO].tolist()
        previstos = self.previsoes.iloc[indices_teste]["latencia_modelo_prevista"].tolist()
        self.metricas = self._calcular_metricas(observados, previstos)
        return self.metricas.copy()

    def _calcular_normalizacao(self, treino: pd.DataFrame) -> None:
        for variavel in self.variaveis_modelo:
            valores = [
                self._valor_termo(registro, variavel)
                for _, registro in treino.iterrows()
            ]
            media = sum(valores) / len(valores)
            escala = math.sqrt(
                sum((valor - media) ** 2 for valor in valores) / len(valores)
            )
            self._medias[variavel] = media
            self._escalas[variavel] = escala if escala > 0 else 1.0

    def _criar_variaveis_modelo(self) -> tuple[str, ...]:
        variaveis = list(self.VARIAVEIS_EXPLICATIVAS)
        if "quadratico" in self.transformacoes:
            variaveis.extend(f"{variavel}_quadrado" for variavel in self.VARIAVEIS_EXPLICATIVAS)
        if "logaritmico" in self.transformacoes:
            variaveis.extend(f"log_{variavel}" for variavel in self.VARIAVEIS_EXPLICATIVAS)
        return tuple(variaveis)

    @staticmethod
    def _valor_termo(registro: Mapping[str, Any], termo: str) -> float:
        if termo.startswith("log_"):
            return math.log(float(registro[termo.removeprefix("log_")]))
        if termo.endswith("_quadrado"):
            return float(registro[termo.removesuffix("_quadrado")]) ** 2
        return float(registro[termo])

    def _linha_normalizada(self, registro: Mapping[str, Any]) -> list[float]:
        return [1.0] + [
            (self._valor_termo(registro, variavel) - self._medias[variavel])
            / self._escalas[variavel]
            for variavel in self.variaveis_modelo
        ]

    @staticmethod
    def _resolver_minimos_quadrados(matriz: list[list[float]], alvo: list[float]) -> list[float]:
        """Resolve a equação normal por eliminação de Gauss-Jordan."""
        tamanho = len(matriz[0])
        sistema = [[0.0] * (tamanho + 1) for _ in range(tamanho)]
        for linha, valor_alvo in zip(matriz, alvo):
            for coluna in range(tamanho):
                sistema[coluna][-1] += linha[coluna] * valor_alvo
                for coluna_2 in range(tamanho):
                    sistema[coluna][coluna_2] += linha[coluna] * linha[coluna_2]

        for coluna in range(tamanho):
            pivo = max(range(coluna, tamanho), key=lambda linha: abs(sistema[linha][coluna]))
            if abs(sistema[pivo][coluna]) < 1e-12:
                raise ValueError("As variáveis não permitem ajustar uma regressão estável.")
            sistema[coluna], sistema[pivo] = sistema[pivo], sistema[coluna]
            divisor = sistema[coluna][coluna]
            sistema[coluna] = [valor / divisor for valor in sistema[coluna]]
            for linha in range(tamanho):
                if linha == coluna:
                    continue
                fator = sistema[linha][coluna]
                sistema[linha] = [
                    valor - fator * referencia
                    for valor, referencia in zip(sistema[linha], sistema[coluna])
                ]
        return [linha[-1] for linha in sistema]

    def prever_instancia(self, variaveis: Mapping[str, Any]) -> float:
        """Prevê a latência para uma nova observação das variáveis operacionais."""
        if self.coeficientes is None or self.intercepto is None:
            self.treinamento_modelo()

        # ``Series`` do pandas itera sobre os valores, e não sobre os nomes
        # das colunas. Usar ``keys()`` garante que tanto um dicionário quanto
        # uma linha do DataFrame sejam validados pelas chaves corretas.
        faltantes = set(self.VARIAVEIS_EXPLICATIVAS) - set(variaveis.keys())
        if faltantes:
            raise ValueError(f"Variáveis ausentes: {', '.join(sorted(faltantes))}.")

        linha = self._linha_normalizada(variaveis)
        resultado = self.intercepto + sum(
            coeficiente * valor
            for coeficiente, valor in zip(self.coeficientes.values(), linha[1:])
        )
        if not math.isfinite(resultado):
            raise ValueError("A previsão calculada não é um número válido.")
        return resultado

    def prever_todos_pontos(self) -> pd.DataFrame:
        """Adiciona a previsão do modelo e o erro para cada registro disponível."""
        if self.coeficientes is None:
            self.treinamento_modelo()
            return self.previsoes.copy()

        resultado = self.dados.copy()
        resultado["latencia_modelo_prevista"] = [
            self.prever_instancia(registro)
            for _, registro in resultado.iterrows()
        ]
        resultado["erro_modelo_absoluto"] = (
            resultado[self.VARIAVEL_ALVO] - resultado["latencia_modelo_prevista"]
        ).abs()
        self.previsoes = resultado
        return resultado.copy()

    def gerar_graficos(self, diretorio_saida: str | Path = ".dados/graficos_modelo") -> dict[str, Path]:
        """Gera gráficos de diagnóstico e retorna os caminhos dos arquivos PNG.

        Os gráficos são salvos em arquivo, em vez de abertos em uma janela, para
        que a funcionalidade também opere no terminal e em ambientes sem tela.
        """
        previsoes = self.prever_todos_pontos()
        diretorio = Path(diretorio_saida)
        diretorio.mkdir(parents=True, exist_ok=True)

        observados = previsoes[self.VARIAVEL_ALVO].tolist()
        previstos = previsoes["latencia_modelo_prevista"].tolist()
        erros = [observado - previsto for observado, previsto in zip(observados, previstos)]
        caminhos = {
            "erros_previstos": diretorio / "erros_por_previsao.png",
            "previsao": diretorio / "previsao_vs_observado.png",
            "log_linear_carga": diretorio / "log_carga_vs_latencia.png",
            "quadratica_carga_tensao": diretorio / "carga_vs_tensao_quadratica.png",
        }

        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.scatter(previstos, erros, alpha=0.35, s=14, color="#d95f02")
        eixo.axhline(0, color="black", linewidth=1)
        eixo.set(
            title="Erros residuais por latência prevista",
            xlabel="Latência prevista (ms)",
            ylabel="Erro: observado - previsto (ms)",
        )
        self._salvar_grafico(figura, caminhos["erros_previstos"])

        figura, eixo = plt.subplots(figsize=(7, 7))
        eixo.scatter(observados, previstos, alpha=0.35, s=14, color="#1b9e77")
        limite_inferior = min(observados + previstos)
        limite_superior = max(observados + previstos)
        eixo.plot([limite_inferior, limite_superior], [limite_inferior, limite_superior], "--", color="black", label="Previsão ideal")
        eixo.set(
            title="Latência prevista versus observada",
            xlabel="Latência observada (ms)",
            ylabel="Latência prevista (ms)",
        )
        eixo.legend()
        self._salvar_grafico(figura, caminhos["previsao"])

        cargas = self.dados["carga"].tolist()
        log_cargas = [math.log(carga) for carga in cargas]
        intercepto, inclinacao = self._ajustar_reta(log_cargas, observados)
        pontos_log = self._pontos_ordenados(log_cargas)
        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.scatter(log_cargas, observados, alpha=0.3, s=14, color="#7570b3")
        eixo.plot(
            pontos_log,
            [intercepto + inclinacao * ponto for ponto in pontos_log],
            color="#e7298a",
            label="Ajuste log-linear",
        )
        eixo.set(
            title="Relação log-linear entre carga e latência observada",
            xlabel="log(carga)",
            ylabel="Latência observada (ms)",
        )
        eixo.legend()
        self._salvar_grafico(figura, caminhos["log_linear_carga"])

        tensoes = self.dados["tensao"].tolist()
        parametros = self._resolver_minimos_quadrados(
            [[1.0, carga, carga ** 2] for carga in cargas], tensoes
        )
        pontos_carga = self._pontos_ordenados(cargas)
        figura, eixo = plt.subplots(figsize=(9, 5))
        eixo.scatter(cargas, tensoes, alpha=0.3, s=14, color="#66a61e")
        eixo.plot(
            pontos_carga,
            [
                parametros[0] + parametros[1] * ponto + parametros[2] * ponto ** 2
                for ponto in pontos_carga
            ],
            color="#e7298a",
            label="Ajuste quadrático",
        )
        eixo.set(
            title="Relação quadrática entre carga e tensão",
            xlabel="Carga (%)",
            ylabel="Tensão (V)",
        )
        eixo.legend()
        self._salvar_grafico(figura, caminhos["quadratica_carga_tensao"])
        return caminhos

    @staticmethod
    def _salvar_grafico(figura: Any, caminho: Path) -> None:
        figura.tight_layout()
        figura.savefig(caminho, dpi=150)
        plt.close(figura)

    @staticmethod
    def _ajustar_reta(x: list[float], y: list[float]) -> tuple[float, float]:
        media_x = sum(x) / len(x)
        media_y = sum(y) / len(y)
        denominador = sum((valor - media_x) ** 2 for valor in x)
        inclinacao = (
            sum((valor_x - media_x) * (valor_y - media_y) for valor_x, valor_y in zip(x, y))
            / denominador
            if denominador
            else 0.0
        )
        return media_y - inclinacao * media_x, inclinacao

    @staticmethod
    def _pontos_ordenados(valores: list[float], quantidade: int = 200) -> list[float]:
        minimo, maximo = min(valores), max(valores)
        if minimo == maximo:
            return [minimo]
        passo = (maximo - minimo) / (quantidade - 1)
        return [minimo + passo * indice for indice in range(quantidade)]

    @staticmethod
    def _calcular_metricas(observados: list[float], previstos: list[float]) -> dict[str, float]:
        erros = [observado - previsto for observado, previsto in zip(observados, previstos)]
        mae = sum(abs(erro) for erro in erros) / len(erros)
        mse = sum(erro ** 2 for erro in erros) / len(erros)
        media_observados = sum(observados) / len(observados)
        soma_total = sum((valor - media_observados) ** 2 for valor in observados)
        r2 = 1.0 - (sum(erro ** 2 for erro in erros) / soma_total) if soma_total else 0.0
        return {"MAE": mae, "MSE": mse, "RMSE": math.sqrt(mse), "R2": r2}

    def obter_coeficientes(self) -> dict[str, float]:
        """Retorna o intercepto e os coeficientes do modelo já treinado."""
        if self.coeficientes is None or self.intercepto is None:
            self.treinamento_modelo()
        return {"intercepto": self.intercepto, **self.coeficientes}
