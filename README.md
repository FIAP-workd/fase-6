# fase-6

Código referente à Fase 6 do primeiro ano do curso de Ciência da Computação da FIAP.

## SCIC - Sistema de Comunicação Interplanetária da Colônia Aurora Siger

O projeto implementa um protótipo em Python para simular o monitoramento operacional da colônia Aurora Siger. O sistema trabalha com dados simulados de módulos da colônia, calcula indicadores, prioriza alertas, executa buscas por prefixo, analisa consumo elétrico e treina um modelo de previsão de latência.

O ponto de entrada é `codigo_fonte.py`, que instancia a classe central `SCIC` e inicia o menu interativo no terminal.

O relatório técnico que é solicitado pela atividade está localizado em [.docs/relatorio_tecnico.md](.docs/relatorio_tecnico.md)

## Funcionalidades

- Consulta de registros do dataset operacional.
- Análise de indicadores de latência, carga, potência e status.
- Cálculo de erro absoluto e erro relativo.
- Modelo de regressão para prever `latencia_observada`.
- Geração de gráficos em `.dados/graficos_modelo`.
- Gerenciamento de alertas com Heap.
- Busca de módulos por nome completo ou prefixo com Trie.
- Análise de consumo e eletricidade.
- Geração automática do dataset `.dados/dados_aurora_siger.csv` quando necessário.

## Estrutura

```text
fase-6/
├── .dados/
├── .docs/
├── src/
│   ├── _scic/
│   ├── analise/
│   ├── buscador_modulos/
│   ├── consulta_registros/
│   ├── eletricidade/
│   ├── estruturas_baixo_nivel/
│   ├── gerador_dados/
│   ├── gerenciador_alertas/
│   ├── modelo/
│   └── utils.py
├── codigo_fonte.py
├── plano_desenvolvimento.md
├── requirements.txt
└── README.md
```



## Requisitos

- Python 3.10 ou superior
- `pandas>=2.0`
- `matplotlib>=3.7`

## Instalação

```bash
git clone https://github.com/FIAP-workd/fase-6.git
cd fase-6
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Execução

```bash
python codigo_fonte.py
```

Menu principal:

```text
1 - Consultar registros
2 - Analisar indicadores
3 - Modelo de previsão
4 - Gerenciar Alertas
5 - Buscar módulos
6 - Analisar consumo e eletricidade
7 - Sair
```

## Dados

O dataset principal é `.dados/dados_aurora_siger.csv`.

Se o arquivo não existir, o sistema gera os dados automaticamente com a classe `GeradorDados`. Os registros simulam ciclos de monitoramento de módulos como comunicação, energia, laboratório, habitação, médico e administrativo.

Campos principais:

- `id`
- `ciclo`
- `modulo`
- `tipo_modulo`
- `codigo_sensor`
- `tensao`
- `corrente`
- `potencia`
- `carga`
- `latencia_prevista`
- `latencia_observada`
- `status`
- `prioridade`
- `mensagem_alerta`
- `data`

## Modelo de previsão

A opção `3 - Modelo de previsão` treina uma regressão múltipla para estimar `latencia_observada` usando:

- `carga`
- `tensao`
- `corrente`
- `ciclo`

O modelo usa termos lineares, quadráticos e logarítmicos. Após o treinamento, exibe métricas como `MAE`, `MSE`, `RMSE` e `R2`.

Também gera gráficos PNG em `.dados/graficos_modelo`:

- `erros_por_previsao.png`
- `previsao_vs_observado.png`
- `log_carga_vs_latencia.png`
- `carga_vs_tensao_quadratica.png`

## Indicadores

A análise calcula:

- latência observada média;
- latência observada máxima;
- carga média;
- potência média;
- percentual de operação normal;
- percentual de operação crítica;
- percentual de operação em alerta;
- erro absoluto médio;
- erro relativo médio.

## Gerenciamento de alertas

O módulo de alertas utiliza Heap para manter os eventos prioritários no topo da fila.

A prioridade considera:

- status do módulo;
- nível de prioridade;
- ciclo do evento.

Operações disponíveis:

- visualizar próximo alerta;
- adicionar alerta;
- marcar alerta prioritário como solucionado.

## Busca de módulos

A busca usa Trie para localizar módulos por nome completo ou prefixo.

Exemplos de módulos simulados:

- `COM-01`
- `COM-02`
- `COM-03`
- `ENE-01`
- `ENE-02`
- `LAB-01`
- `HAB-01`
- `HAB-02`
- `MED-01`
- `ADM-01`

## Análise de consumo e eletricidade

A análise elétrica calcula:

- tensão média, mínima e máxima;
- corrente média, mínima e máxima;
- potência por `P = V x I`;
- potência média, mínima, máxima e total;
- maiores consumos;
- consumo médio por módulo;
- representação da potência média em decimal, binário e hexadecimal.

## Arquitetura

A classe `SCIC`, em `src/_scic/scic.py`, orquestra o sistema. Ela carrega ou gera os dados, exibe o menu principal e chama os módulos de consulta, indicadores, modelo, alertas, busca e eletricidade.

O arquivo `codigo_fonte.py` funciona apenas como ponto de entrada:

```python
from src._scic import SCIC

if __name__ == '__main__':
    app = SCIC()
    app.run()
```

## Plano de desenvolvimento

O arquivo `plano_desenvolvimento.md` documenta a proposta técnica do SCIC, incluindo objetivo do projeto, arquitetura, estrutura de pastas, geração de dados, análise de indicadores, cálculo de erros, modelo de previsão, Heap, Trie, eletricidade e entregáveis.

## Observações

- O projeto é executado via terminal.
- Os sensores e eventos são simulados.
- O sistema não depende de APIs externas.
- O modelo de regressão foi implementado no próprio projeto.
- Os gráficos são salvos como PNG para funcionar também em ambientes sem interface gráfica.

## Repositório

https://github.com/FIAP-workd/fase-6
```