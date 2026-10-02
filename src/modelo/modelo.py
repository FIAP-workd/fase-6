"""Modelo de regressão para a latência dos módulos da Aurora Siger.

O módulo usa apenas a biblioteca padrão (além do ``pandas``, já usado pelo
projeto).  Isso mantém a demonstração do modelo executável no ambiente do
projeto sem exigir uma dependência externa de aprendizado de máquina.
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping
from typing import Any

import pandas as pd


class Modelo:
    """Regressão linear múltipla para estimar ``latencia_observada``.

    As variáveis explicativas seguem o plano de desenvolvimento: carga,
    tensão, corrente e ciclo. A potência não é incluída, pois ela é derivada
    de tensão e corrente e introduziria redundância matemática no ajuste.
    """

    VARIAVEIS_EXPLICATIVAS = ("carga", "tensao", "corrente", "ciclo")
    VARIAVEL_ALVO = "latencia_observada"

    def __init__(
        self,
        dados: pd.DataFrame,
        percentual_teste: float = 0.2,
        seed: int = 42,
    ) -> None:
        if not 0 < percentual_teste < 1:
            raise ValueError("percentual_teste deve estar entre 0 e 1.")

        self.dados = dados.copy()
        self.percentual_teste = percentual_teste
        self.seed = seed
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
        if len(self.dados) < len(self.VARIAVEIS_EXPLICATIVAS) + 2:
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

        if len(indices_treino) < len(self.VARIAVEIS_EXPLICATIVAS) + 1:
            raise ValueError("Não há registros de treino suficientes para a regressão.")

        treino = self.dados.iloc[indices_treino]
        self._calcular_normalizacao(treino)
        matriz = [self._linha_normalizada(linha) for _, linha in treino.iterrows()]
        alvo = [float(valor) for valor in treino[self.VARIAVEL_ALVO]]
        parametros = self._resolver_minimos_quadrados(matriz, alvo)

        self.intercepto = parametros[0]
        self.coeficientes = dict(zip(self.VARIAVEIS_EXPLICATIVAS, parametros[1:]))
        self.prever_todos_pontos()

        observados = self.dados.iloc[indices_teste][self.VARIAVEL_ALVO].tolist()
        previstos = self.previsoes.iloc[indices_teste]["latencia_modelo_prevista"].tolist()
        self.metricas = self._calcular_metricas(observados, previstos)
        return self.metricas.copy()

    def _calcular_normalizacao(self, treino: pd.DataFrame) -> None:
        for variavel in self.VARIAVEIS_EXPLICATIVAS:
            media = float(treino[variavel].mean())
            escala = float(treino[variavel].std(ddof=0))
            self._medias[variavel] = media
            self._escalas[variavel] = escala if escala > 0 else 1.0

    def _linha_normalizada(self, registro: Mapping[str, Any]) -> list[float]:
        return [1.0] + [
            (float(registro[variavel]) - self._medias[variavel])
            / self._escalas[variavel]
            for variavel in self.VARIAVEIS_EXPLICATIVAS
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
