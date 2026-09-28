from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ConfigModulo:
    """Configuração nominal de um módulo da Aurora Siger."""

    modulo: str
    tipo_modulo: str
    criticidade: str
    tensao_nominal: float
    corrente_nominal: float
    latencia_base_ms: float
    prioridade_base: str


class GeradorDados:
    """
    Gera um universo coerente de dados para a estrutura Aurora Siger.

    Os dados não são gerados como variáveis independentes:
    - potência depende de tensão e corrente;
    - corrente/tensão/carga possuem variação controlada;
    - latência depende da latência base, carga, ruído e anomalias;
    - status/prioridade/mensagem são derivados do estado do módulo;
    - os módulos possuem perfis operacionais diferentes.
    """

    CAMPOS = [
        "id",
        "ciclo",
        "modulo",
        "tipo_modulo",
        "codigo_sensor",
        "tensao",
        "corrente",
        "potencia",
        "carga",
        "latencia_prevista",
        "latencia_observada",
        "status",
        "prioridade",
        "mensagem_alerta",
        "data",
    ]

    def __init__(
        self,
        quantidade_ciclos: int = 1000,
        intervalo_minutos: int = 10,
        seed: int = 42,
    ):
        # ================================================================
        # ALTERE AQUI O CAMINHO DO DATASET DE SAÍDA
        # ================================================================
        self._output_path = Path(".dados/dados_aurora_siger.csv")

        self.quantidade_ciclos = quantidade_ciclos
        self.intervalo_minutos = intervalo_minutos
        self.seed = seed

        self._rng = random.Random(seed)

        # Cada módulo possui um perfil próprio.
        # Esses parâmetros são a base para gerar relações coerentes.
        self.modulos: Dict[str, ConfigModulo] = {
            "COM-01": ConfigModulo(
                "COM-01", "Comunicacao", "Critica",
                48.0, 8.0, 120.0, "Alta"
            ),
            "COM-02": ConfigModulo(
                "COM-02", "Comunicacao", "Critica",
                48.0, 7.5, 150.0, "Alta"
            ),
            "COM-03": ConfigModulo(
                "COM-03", "Comunicacao", "Media",
                24.0, 5.0, 180.0, "Media"
            ),
            "ENE-01": ConfigModulo(
                "ENE-01", "Energia", "Critica",
                220.0, 18.0, 220.0, "Alta"
            ),
            "ENE-02": ConfigModulo(
                "ENE-02", "Energia", "Alta",
                220.0, 14.0, 240.0, "Alta"
            ),
            "LAB-01": ConfigModulo(
                "LAB-01", "Laboratorio", "Alta",
                110.0, 10.0, 260.0, "Media"
            ),
            "HAB-01": ConfigModulo(
                "HAB-01", "Habitacao", "Alta",
                110.0, 8.0, 280.0, "Media"
            ),
            "HAB-02": ConfigModulo(
                "HAB-02", "Habitacao", "Media",
                110.0, 7.0, 300.0, "Media"
            ),
            "MED-01": ConfigModulo(
                "MED-01", "Medico", "Critica",
                110.0, 6.0, 170.0, "Alta"
            ),
            "ADM-01": ConfigModulo(
                "ADM-01", "Administrativo", "Baixa",
                110.0, 4.0, 350.0, "Baixa"
            ),
        }

        self.data_inicio = datetime(2040, 1, 1, 0, 0, 0)


    @property
    def output_path(self) -> Path:
        return self._output_path


    def gerar(self) -> Path:
        """Gera o dataset completo e retorna o caminho do arquivo."""
        registros = self._gerar_registros()
        self._validar_registros(registros)
        self._salvar_csv(registros)
        return self.output_path

    def _gerar_registros(self) -> List[dict]:
        registros: List[dict] = []
        contador_id = 1

        # O estado anterior permite criar continuidade temporal.
        estado_anterior = {
            modulo: {
                "carga": self._rng.uniform(25.0, 55.0),
            }
            for modulo in self.modulos
        }

        for ciclo in range(1, self.quantidade_ciclos + 1):
            data = self.data_inicio + timedelta(
                minutes=(ciclo - 1) * self.intervalo_minutos
            )

            # Uma variável ambiental comum cria correlação entre módulos
            # no mesmo ciclo sem tornar os dados idênticos.
            fator_sistema = self._fator_sistema(ciclo)

            for modulo_nome, config in self.modulos.items():
                estado = estado_anterior[modulo_nome]

                carga = self._gerar_carga(
                    carga_anterior=estado["carga"],
                    fator_sistema=fator_sistema,
                )
                estado["carga"] = carga

                anomalia = self._sortear_anomalia()

                tensao = self._gerar_tensao(config, carga, anomalia)
                corrente = self._gerar_corrente(config, carga, anomalia)

                # Regra física principal:
                # potência = tensão * corrente
                potencia = tensao * corrente

                latencia_prevista = self._gerar_latencia_prevista(
                    config=config,
                    carga=carga,
                )

                latencia_observada = self._gerar_latencia_observada(
                    config=config,
                    carga=carga,
                    latencia_prevista=latencia_prevista,
                    anomalia=anomalia,
                )

                status, prioridade, mensagem = self._classificar_estado(
                    config=config,
                    carga=carga,
                    tensao=tensao,
                    corrente=corrente,
                    latencia_observada=latencia_observada,
                    anomalia=anomalia,
                )

                registros.append(
                    {
                        "id": contador_id,
                        "ciclo": ciclo,
                        "modulo": modulo_nome,
                        "tipo_modulo": config.tipo_modulo,
                        "codigo_sensor": f"SNS-{modulo_nome}",
                        "tensao": round(tensao, 3),
                        "corrente": round(corrente, 3),
                        "potencia": round(potencia, 3),
                        "carga": round(carga, 3),
                        "latencia_prevista": round(latencia_prevista, 3),
                        "latencia_observada": round(latencia_observada, 3),
                        "status": status,
                        "prioridade": prioridade,
                        "mensagem_alerta": mensagem,
                        "data": data.isoformat(sep=" "),
                    }
                )

                contador_id += 1

        return registros

    def _fator_sistema(self, ciclo: int) -> float:
        """
        Representa uma condição global da estação.

        Combina sazonalidade suave e ruído pequeno para evitar
        comportamento completamente aleatório.
        """
        sazonalidade = 8.0 * math.sin(ciclo / 35.0)
        ruido = self._rng.gauss(0.0, 2.0)
        return sazonalidade + ruido

    def _gerar_carga(self, carga_anterior: float, fator_sistema: float) -> float:
        """
        Gera carga com dependência temporal.

        A carga atual depende parcialmente da carga anterior,
        de uma condição global da estação e de um pequeno ruído.
        """
        tendencia = self._rng.gauss(0.0, 4.0)
        nova_carga = (
            0.82 * carga_anterior
            + 0.12 * (50.0 + fator_sistema)
            + 0.06 * (50.0 + tendencia)
        )

        return max(0.0, min(100.0, nova_carga))

    def _sortear_anomalia(self) -> Optional[str]:
        """
        Aproximadamente 5% dos registros recebem uma anomalia.

        O sorteio possui pesos para produzir diferentes situações.
        """
        sorteio = self._rng.random()

        if sorteio >= 0.05:
            return None

        tipos = [
            "latencia_alta",
            "carga_alta",
            "queda_tensao",
            "corrente_alta",
            "comunicacao_degradada",
        ]

        return self._rng.choice(tipos)

    def _gerar_tensao(
        self,
        config: ConfigModulo,
        carga: float,
        anomalia: Optional[str],
    ) -> float:
        """
        Tensão nominal com pequena variação.

        Cargas muito altas podem produzir uma pequena queda natural.
        A anomalia de queda de tensão aumenta esse efeito.
        """
        queda_por_carga = max(0.0, carga - 75.0) * 0.04
        ruido = self._rng.gauss(0.0, config.tensao_nominal * 0.01)

        tensao = config.tensao_nominal - queda_por_carga + ruido

        if anomalia == "queda_tensao":
            tensao *= self._rng.uniform(0.72, 0.90)

        return max(0.0, tensao)

    def _gerar_corrente(
        self,
        config: ConfigModulo,
        carga: float,
        anomalia: Optional[str],
    ) -> float:
        """
        Corrente relacionada à carga operacional do módulo.
        """
        proporcao_carga = 0.35 + (0.65 * carga / 100.0)
        ruido = self._rng.gauss(0.0, config.corrente_nominal * 0.025)

        corrente = config.corrente_nominal * proporcao_carga + ruido

        if anomalia == "corrente_alta":
            corrente *= self._rng.uniform(1.25, 1.55)

        return max(0.01, corrente)

    def _gerar_latencia_prevista(
        self,
        config: ConfigModulo,
        carga: float,
    ) -> float:
        """
        Latência esperada aumenta suavemente com a carga.
        """
        efeito_carga = 0.70 * carga
        return config.latencia_base_ms + efeito_carga

    def _gerar_latencia_observada(
        self,
        config: ConfigModulo,
        carga: float,
        latencia_prevista: float,
        anomalia: Optional[str],
    ) -> float:
        """
        Latência observada = base + efeito da carga + ruído + anomalia.
        """
        ruido = self._rng.gauss(0.0, 12.0)

        latencia = latencia_prevista + ruido

        if anomalia == "latencia_alta":
            latencia *= self._rng.uniform(1.8, 3.0)

        elif anomalia == "comunicacao_degradada":
            latencia *= self._rng.uniform(1.4, 2.2)

        elif anomalia == "carga_alta":
            # A anomalia de carga também afeta a comunicação.
            latencia += self._rng.uniform(80.0, 180.0)

        return max(1.0, latencia)

    def _classificar_estado(
        self,
        config: ConfigModulo,
        carga: float,
        tensao: float,
        corrente: float,
        latencia_observada: float,
        anomalia: Optional[str],
    ) -> tuple[str, str, str]:
        """
        Determina status, prioridade e mensagem a partir das medições.
        """
        alertas = []

        limite_latencia = config.latencia_base_ms + 0.70 * 100.0

        if latencia_observada > limite_latencia * 1.7:
            alertas.append("latência muito alta")

        if carga >= 90.0:
            alertas.append("carga elevada")

        if tensao < config.tensao_nominal * 0.85:
            alertas.append("queda de tensão")

        if corrente > config.corrente_nominal * 1.20:
            alertas.append("corrente acima do nominal")

        if anomalia == "comunicacao_degradada":
            alertas.append("comunicação degradada")

        if not alertas:
            return "Normal", "Nenhuma", "Sem alertas"

        # Um módulo crítico recebe prioridade maior quando existe problema.
        if config.criticidade == "Critica":
            prioridade = "Critica"
        elif config.criticidade == "Alta":
            prioridade = "Alta"
        else:
            prioridade = "Media"

        if len(alertas) >= 2:
            status = "Critico"
        else:
            status = "Alerta"

        mensagem = "; ".join(alertas).capitalize()

        return status, prioridade, mensagem

    def _validar_registros(self, registros: List[dict]) -> None:
        """Valida regras mínimas de consistência antes de salvar."""
        if not registros:
            raise ValueError("Nenhum registro foi gerado.")

        for registro in registros:
            tensao = float(registro["tensao"])
            corrente = float(registro["corrente"])
            potencia = float(registro["potencia"])
            carga = float(registro["carga"])

            # Regra física: P = V * I.
            potencia_calculada = round(tensao * corrente, 3)

            if not math.isclose(
                potencia,
                potencia_calculada,
                rel_tol=0.1,
                abs_tol=0.1,
            ):
                raise ValueError(
                    f"Potência inconsistente no registro {registro['id']}."
                )

            if not 0.0 <= carga <= 100.0:
                raise ValueError(
                    f"Carga fora do intervalo no registro {registro['id']}."
                )

            if float(registro["latencia_observada"]) <= 0:
                raise ValueError(
                    f"Latência inválida no registro {registro['id']}."
                )

        quantidade_anomalias = sum(
            1
            for registro in registros
            if registro["status"] != "Normal"
        )

        proporcao = quantidade_anomalias / len(registros)

        # A validação não exige exatamente 5%, pois o sorteio é probabilístico.
        # Apenas impede uma geração sem qualquer ocorrência ou exageradamente
        # anormal para o cenário proposto.
        if proporcao > 0.15:
            raise ValueError(
                f"Quantidade de anomalias acima do esperado: "
                f"{proporcao:.2%}."
            )

    def _salvar_csv(self, registros: List[dict]) -> None:
        """Salva os registros no CSV definido em self.output_path."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with self.output_path.open(
            mode="w",
            newline="",
            encoding="utf-8",
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=self.CAMPOS,
            )
            escritor.writeheader()
            escritor.writerows(registros)


if __name__ == "__main__":
    gerador = GeradorDados(
        quantidade_ciclos=1000,
        intervalo_minutos=10,
        seed=42,
    )

    caminho = gerador.gerar()
    print(f"Dataset gerado com sucesso em: {caminho}")