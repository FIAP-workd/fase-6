# SCIC — Plano de Arquitetura, Desenvolvimento e Integração

> **Sistema de Comunicação Interplanetária da Colônia (SCIC)**
>
> Documento de organização técnica para dividir o desenvolvimento entre os integrantes da equipe e manter uma arquitetura única e integrada.

---

## 1. Objetivo do projeto

O SCIC será um protótipo em Python para simular o monitoramento operacional e de comunicação da colônia Aurora Siger.

O sistema deverá:

- organizar dados operacionais e de comunicação;
- carregar e registrar dados simulados;
- calcular indicadores;
- calcular erros entre valores previstos e observados;
- executar uma previsão simples;
- avaliar o desempenho da previsão;
- priorizar alertas críticos;
- realizar buscas eficientes por prefixo;
- demonstrar conceitos de organização e arquitetura de computadores;
- relacionar os dados a conceitos de eletricidade;
- apresentar uma análise de gestão inteligente da comunicação;
- permitir que todas essas funcionalidades sejam executadas por meio de uma classe central `SCIC`.

O projeto **não precisa implementar sensores físicos, APIs externas, hardware real, dashboards web ou redes neurais profundas**. Os sensores e os demais dispositivos serão simulados.

---

# 2. Princípio arquitetural

A regra principal do projeto será:

> **O `main.py` apenas inicia o sistema. Toda a lógica deverá estar encapsulada na classe `SCIC`.**

O fluxo geral será:

```text
main.py
   |
   v
SCIC()
   |
   +--> Carregamento/Geração de dados
   |
   +--> Análise dos indicadores
   |
   +--> Cálculo de erros
   |
   +--> Modelo de previsão
   |
   +--> Heap de alertas
   |
   +--> Trie de busca
   |
   +--> Cálculos elétricos
   |
   +--> Relatórios/resultados
   |
   v
Terminal
```

A equipe deve evitar que o `main.py` contenha regras de negócio.

---

# 3. Estrutura de pastas

A estrutura proposta é:

```text
SCIC/
│
├── README.md
├── main.py
│
├── .dados/
│   ├── dados_aurora_siger.csv
│   └── dados_processados.csv
│
├── .docs/
│   ├── link_video.txt
│   └── relatorio_tecnico.pdf
│
├── src/
│   ├── __init__.py
│   │
│   ├── scic/
│   │   ├── __init__.py
│   │   └── scic.py
│   │
│   ├── dados/
│   │   ├── __init__.py
│   │   └── gerador_dados.py
│   │
│   ├── analise/
│   │   ├── __init__.py
│   │   ├── indicadores.py
│   │   └── erros.py
│   │
│   ├── modelo/
│   │   ├── __init__.py
│   │   └── previsao.py
│   │
│   ├── estruturas/
│   │   ├── __init__.py
│   │   ├── heap.py
│   │   └── trie.py
│   │
│   ├── estruturas_baixo_nivel/
│   │   ├── __init__.py
│   │   ├── heap.py
│   │   ├── trie.py
│   │   ├── no_heap.py
│   │   └── no_trie.py
│   │
│   ├── eletricidade/
│   │   ├── __init__.py
│   │   └── calculos.py
│   │
│   └── interface/
│       ├── __init__.py
│       └── menu.py
│
└── requirements.txt
```

## 3.1 Regra sobre a pasta raiz

Na raiz do projeto devem existir somente:

```text
SCIC/
├── README.md
└── main.py
```

Todos os demais arquivos devem ficar organizados em subpastas.

---

# 4. Responsabilidade de cada pasta

## `.dados/`

Responsável exclusivamente pelos arquivos de dados utilizados pelo sistema.

### Arquivos

#### `dados_aurora_siger.csv`

Dataset principal do projeto.

É o arquivo que será lido pelo SCIC.

#### `dados_processados.csv`

Arquivo opcional para armazenar dados derivados ou resultados processados.

Exemplo:

- erros calculados;
- classificação de status;
- indicadores derivados.

A equipe deve evitar alterar o dataset original sem necessidade.

---

## `.docs/`

Documentação e entregáveis finais.

```text
.docs/
├── link_video.txt
└── relatorio_tecnico.pdf
```

### `link_video.txt`

Conterá somente o link do vídeo final.

O vídeo será produzido e apresentado manualmente pela equipe.

### `relatorio_tecnico.pdf`

Relatório final contendo:

- contexto;
- descrição dos dados;
- indicadores;
- análise dos erros;
- modelo de previsão;
- métricas;
- Heap;
- Trie;
- organização de computadores;
- eletricidade;
- comunicação inteligente;
- aspectos sociais/culturais/sustentabilidade;
- conclusões;
- exemplos de execução.

---

# 5. `main.py`

O `main.py` deve ser extremamente simples.

Responsabilidade:

1. importar a classe `SCIC`;
2. criar uma instância;
3. iniciar a execução.

Exemplo conceitual:

```python
from src.scic.scic import SCIC


def main():
    sistema = SCIC()
    sistema.executar()


if __name__ == "__main__":
    main()
```

Não colocar no `main.py`:

- cálculo de indicadores;
- código de ML;
- implementação de Heap;
- implementação de Trie;
- leitura detalhada de CSV;
- regras de negócio;
- cálculos elétricos.

Tudo isso pertence às classes/módulos internos.

---

# 6. Classe central `SCIC`

Arquivo:

```text
src/scic/scic.py
```

A classe `SCIC` será o **orquestrador do sistema**.

Ela não deve necessariamente implementar todos os algoritmos internamente.

Sua função é coordenar os módulos.

Estrutura conceitual:

```python
class SCIC:

    def __init__(self):
        # inicializar componentes
        pass

    def carregar_dados(self):
        pass

    def gerar_dados(self):
        pass

    def calcular_indicadores(self):
        pass

    def calcular_erros(self):
        pass

    def executar_previsao(self):
        pass

    def avaliar_modelo(self):
        pass

    def priorizar_alertas(self):
        pass

    def buscar_por_prefixo(self):
        pass

    def calcular_eletricidade(self):
        pass

    def executar(self):
        pass
```

A implementação final pode ser dividida em métodos menores.

---

# 7. Fluxo completo da classe `SCIC`

O método principal será:

```python
sistema.executar()
```

Fluxo esperado:

```text
SCIC.executar()
       |
       v
Carregar dados
       |
       v
Validar dados
       |
       v
Calcular indicadores
       |
       v
Calcular erros
       |
       v
Executar previsão
       |
       v
Avaliar modelo
       |
       v
Criar/priorizar alertas
       |
       v
Construir Trie
       |
       v
Executar cálculos elétricos
       |
       v
Apresentar resultados
```

O sistema também poderá disponibilizar métodos individuais para o menu.

---

# 8. Geração dos dados

Arquivo:

```text
src/dados/gerador_dados.py
```

A geração de dados deve criar um **universo coerente da Aurora Siger**.

Não devemos gerar valores completamente aleatórios e independentes.

Os dados precisam possuir relações entre si.

---

## 8.1 Exemplo de entidades

Podemos utilizar módulos como:

```text
COM-01
COM-02
COM-03
ENE-01
ENE-02
LAB-01
HAB-01
HAB-02
MED-01
ADM-01
```

Tipos:

```text
Comunicacao
Energia
Laboratorio
Habitacao
Medico
Administrativo
```

Cada módulo poderá possuir:

- criticidade;
- sensor;
- tensão;
- corrente;
- potência;
- carga;
- latência prevista;
- latência observada;
- status;
- prioridade;
- mensagem de alerta.

---

# 9. Estrutura do dataset

Dataset principal:

```text
.dados/dados_aurora_siger.csv
```

Campos sugeridos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único do registro |
| `ciclo` | Ciclo de monitoramento |
| `modulo` | Nome/código do módulo |
| `tipo_modulo` | Categoria do módulo |
| `codigo_sensor` | Código do sensor |
| `tensao` | Tensão elétrica |
| `corrente` | Corrente elétrica |
| `potencia` | Potência calculada |
| `carga` | Carga operacional |
| `latencia_prevista` | Latência esperada |
| `latencia_observada` | Latência medida |
| `status` | Estado operacional |
| `prioridade` | Prioridade do alerta |
| `mensagem_alerta` | Descrição do alerta |
| `data` | Data/ciclo de registro |

---

# 10. Regras para geração dos dados

Os valores devem possuir relações.

## 10.1 Potência

A potência será calculada por:

```text
P = V × I
```

Portanto:

```python
potencia = tensao * corrente
```

Não gerar potência independentemente de tensão e corrente.

---

## 10.2 Latência observada

A latência observada poderá ser baseada em:

```text
latência observada
=
latência base
+
efeito da carga
+
ruído
+
eventual anomalia
```

Isso permitirá que exista uma relação que posteriormente possa ser explorada pelo modelo de previsão.

---

## 10.3 Carga

A carga pode variar entre:

```text
0% a 100%
```

Quanto maior a carga, maior poderá ser a tendência de aumento da latência.

Não é necessário criar uma relação perfeitamente linear.

---

## 10.4 Anomalias

Devemos inserir uma quantidade controlada de anomalias.

Exemplo:

```text
~5% dos registros → situação anormal
```

Possíveis situações:

- latência muito alta;
- carga elevada;
- queda de tensão;
- aumento de corrente;
- módulo crítico com comunicação degradada.

Isso permitirá demonstrar o Heap de forma realista.

---

# 11. Análise de dados

Pasta:

```text
src/analise/
```

Arquivos:

```text
indicadores.py
erros.py
```

---

# 12. Indicadores

Arquivo:

```text
src/analise/indicadores.py
```

Responsável por calcular indicadores operacionais.

Exemplos:

- latência média;
- latência máxima;
- latência mínima;
- carga média;
- potência média;
- quantidade de alertas;
- quantidade de módulos críticos;
- percentual de registros problemáticos.

Exemplo conceitual:

```python
class Indicadores:

    def calcular_latencia_media(self, dados):
        pass

    def calcular_carga_media(self, dados):
        pass

    def contar_alertas(self, dados):
        pass
```

---

# 13. Cálculo de erros

Arquivo:

```text
src/analise/erros.py
```

Devemos calcular:

## Erro absoluto

```text
erro_absoluto =
|observado - previsto|
```

## Erro relativo

```text
erro_relativo =
|observado - previsto| / |observado|
```

Quando necessário, apresentar o erro relativo em percentual:

```text
erro_relativo_percentual =
erro_relativo × 100
```

Também devemos tratar situações em que o denominador seja zero.

---

# 14. Modelo de previsão

Pasta:

```text
src/modelo/
```

Arquivo:

```text
previsao.py
```

Objetivo:

Criar uma previsão simples relacionada à operação do SCIC.

A sugestão principal é prever:

```text
latencia_observada
```

a partir de variáveis como:

```text
carga
tensao
corrente
potencia
```

---

## 14.1 Modelo
Pasta:

src/modelo/

Arquivos:

previsao.py
metricas.py

---

## 14.1 Objetivo do modelo

O SCIC utilizará um modelo de regressão para estimar a latência
observada de comunicação dos módulos da colônia Aurora Siger.

O objetivo é verificar se características operacionais e elétricas
dos módulos possuem relação suficiente com a latência de comunicação
para permitir uma estimativa razoável desse indicador.

O problema será tratado como um problema de regressão supervisionada,
pois a variável que desejamos prever é numérica e possui valores
contínuos.

---

## 14.2 Tipo de modelo

Será utilizada uma regressão linear múltipla.

A regressão linear múltipla permite estimar uma variável dependente
a partir de duas ou mais variáveis explicativas.

A estrutura geral do modelo será:

latencia_observada =
β0 +
β1 × carga +
β2 × tensao +
β3 × corrente +
β4 × ciclo +
ε

Onde:

- β0 representa o intercepto;
- β1, β2, β3 e β4 representam os coeficientes estimados pelo modelo;
- ε representa o erro/resíduo da previsão.

---

## 14.3 Variável dependente

A variável dependente, também chamada de variável resposta ou
variável alvo, será:

latencia_observada

Essa variável representa a latência efetivamente observada na
comunicação de determinado módulo durante determinado ciclo.

Unidade:

milissegundos (ms).

O modelo tentará estimar esse valor a partir das características
operacionais disponíveis.

---

## 14.4 Variáveis explicativas

As variáveis explicativas utilizadas inicialmente serão:

### carga

Representa o nível de utilização operacional do módulo.

Uma maior carga pode representar maior demanda sobre os recursos
do módulo e, consequentemente, potencial aumento da latência.

### tensao

Representa a tensão elétrica de operação do módulo.

Essa variável permite investigar se alterações nas condições elétricas
estão associadas a alterações na latência de comunicação.

### corrente

Representa a corrente elétrica utilizada pelo módulo.

Assim como a tensão, pode fornecer informações sobre as condições
operacionais do equipamento.

### ciclo

Representa o momento/ciclo da operação.

A inclusão dessa variável permite ao modelo capturar possíveis
variações temporais existentes nos dados simulados.

---

## 14.5 Variável potência

A variável potência também estará presente nos dados do SCIC e será
utilizada nos indicadores elétricos.

Ela será calculada pela relação:

potencia = tensao × corrente

Por ser diretamente derivada de tensão e corrente, a potência não
será utilizada simultaneamente com essas duas variáveis no modelo
principal, evitando introduzir uma relação matemática redundante
entre variáveis explicativas.

A potência poderá, entretanto, ser utilizada em uma versão alternativa
do modelo para comparação.

---

## 14.6 Separação entre X e y

Para treinamento do modelo:

X = [
    carga,
    tensao,
    corrente,
    ciclo
]

y = latencia_observada

Onde:

- X contém as variáveis explicativas;
- y contém a variável que o modelo deve explicar/predizer.

---

## 14.7 Treinamento

Os dados serão separados em conjunto de treinamento e conjunto de
teste.

O modelo será ajustado utilizando os dados de treinamento e,
posteriormente, utilizado para gerar previsões para os dados de teste.

A comparação entre:

latencia_observada

e

latencia_prevista

permitirá avaliar a capacidade de previsão do modelo.

---

## 14.8 Avaliação do modelo

O desempenho do modelo será avaliado utilizando:

- MAE — Mean Absolute Error;
- MSE — Mean Squared Error;
- RMSE — Root Mean Squared Error;
- R² — Coeficiente de determinação.

Essas métricas serão utilizadas para avaliar o quanto as previsões
do modelo se aproximam dos valores observados.

A interpretação dos resultados será realizada posteriormente no
relatório técnico.

---

# 15. Avaliação do modelo

Devemos separar:

```text
treinamento
```

de:

```text
teste
```

E calcular:

- MAE;
- MSE;
- RMSE;
- R².

O relatório não deve simplesmente mostrar os valores.

É necessário explicar o significado deles.

Exemplo:

```text
MAE menor → menor erro médio absoluto.
RMSE maior penalização para erros grandes.
R² → proporção da variabilidade explicada pelo modelo.
```

---

# 16. Heap — prioridade de alertas

A Heap será utilizada para responder:

> "Qual alerta deve ser tratado primeiro?"

Pasta principal:

```text
src/estruturas/
```

Implementação de baixo nível:

```text
src/estruturas_baixo_nivel/
```

---

# 17. Separação da Heap

Queremos demonstrar duas coisas:

1. uso da estrutura no sistema;
2. implementação da estrutura em baixo nível.

Por isso:

```text
src/estruturas_baixo_nivel/heap.py
```

deve conter a implementação da Heap sem depender de uma implementação pronta de biblioteca que esconda o algoritmo.

A camada:

```text
src/estruturas/heap.py
```

pode funcionar como uma camada de integração/adaptação entre a Heap e o SCIC.

---

# 18. Funcionamento da Heap

Cada alerta deverá possuir uma prioridade.

Exemplo conceitual:

```text
prioridade =
criticidade
+
gravidade
+
impacto
+
atraso
```

Quanto maior a prioridade, mais urgente o alerta.

Exemplo:

```text
CRÍTICO → prioridade 100
ALTO     → prioridade 70
MÉDIO    → prioridade 40
BAIXO    → prioridade 10
```

A fórmula final deve ser definida pela equipe e documentada.

---

# 19. O que a Heap deve permitir

A estrutura deverá permitir:

```text
inserir alerta
consultar alerta prioritário
remover alerta prioritário
```

Exemplo:

```text
Heap

        [100]
       /     \
     [80]    [70]
    /   \
  [50]  [40]
```

O alerta de maior prioridade fica disponível de maneira eficiente.

---

# 20. Trie — busca por prefixo

A Trie será utilizada para buscas como:

```text
COM
```

retornando:

```text
COM-01
COM-02
COM-03
```

Também podemos utilizar códigos de sensores:

```text
SEN-COM
```

retornando sensores relacionados.

---

# 21. Separação da Trie

Implementação de baixo nível:

```text
src/estruturas_baixo_nivel/trie.py
src/estruturas_baixo_nivel/no_trie.py
```

Camada de integração:

```text
src/estruturas/trie.py
```

A Trie deve implementar, no mínimo:

```text
insert()
search()
starts_with()
```

---

# 22. Exemplo de funcionamento da Trie

Inserir:

```text
COM-01
COM-02
COM-03
LAB-01
LAB-02
MED-01
```

Pesquisar:

```text
COM
```

Resultado:

```text
COM-01
COM-02
COM-03
```

Pesquisar:

```text
LAB
```

Resultado:

```text
LAB-01
LAB-02
```

---

# 23. Por que implementar em baixo nível?

O projeto precisa demonstrar conhecimento das estruturas de dados.

Portanto, não queremos apenas:

```python
import alguma_biblioteca
```

e utilizar uma estrutura pronta.

A implementação deve permitir explicar:

- nós;
- referências;
- inserção;
- busca;
- remoção;
- reorganização;
- complexidade;
- funcionamento interno.

A implementação de baixo nível será utilizada como evidência técnica no projeto e poderá ser demonstrada durante a apresentação.

---

# 24. Organização de computadores

Pasta:

```text
src/eletricidade/
```

A parte conceitual de organização de computadores poderá ser apresentada no relatório e no sistema.

Devemos relacionar:

```text
Entrada
   ↓
Sensor simulado
   ↓
Processamento
   ↓
Memória/dados
   ↓
Algoritmos
   ↓
Saída
```

Exemplo:

```text
Sensor de comunicação
        ↓
dados_aurora_siger.csv
        ↓
Pandas/Python
        ↓
SCIC
        ↓
Heap / Trie / Modelo
        ↓
Terminal
```

---

# 25. Representação numérica

O projeto deve demonstrar pelo menos uma conversão entre bases.

Exemplo:

```text
Decimal → Binário
Decimal → Hexadecimal
```

Isso pode ser apresentado no relatório e, se fizer sentido, em uma funcionalidade simples do sistema.

---

# 26. Eletricidade

Arquivo:

```text
src/eletricidade/calculos.py
```

Responsável por cálculos elétricos.

Principal relação:

```text
P = V × I
```

Onde:

```text
P = potência
V = tensão
I = corrente
```

Exemplo:

```text
V = 220 V
I = 2 A

P = 220 × 2
P = 440 W
```

Os valores devem ser provenientes dos dados simulados sempre que possível.

---

# 27. Integração entre eletricidade e comunicação

A eletricidade não deve aparecer como uma demonstração isolada.

Precisamos conectar os dados.

Exemplo:

```text
aumento de carga
      ↓
alteração no consumo
      ↓
maior demanda operacional
      ↓
possível impacto na comunicação
      ↓
aumento de latência
      ↓
geração de alerta
      ↓
Heap prioriza alerta
```

Essa relação ajudará a demonstrar que o projeto é um sistema integrado e não uma coleção de exercícios independentes.

---

# 28. Gestão inteligente da comunicação

O projeto deverá relacionar os resultados obtidos com conceitos de:

- monitoramento contínuo;
- sensores inteligentes;
- automação;
- armazenamento;
- redundância;
- manutenção preditiva;
- redes de comunicação;
- gerenciamento operacional.

A explicação deve ser baseada nos próprios resultados do SCIC.

Exemplo:

```text
O SCIC identificou aumento de latência em módulos
com alta carga.

↓

O sistema identifica o comportamento.

↓

O modelo estima a latência.

↓

O alerta é criado.

↓

A Heap determina a prioridade.

↓

A equipe pode atuar antes de uma falha completa.
```

---

# 29. Aspectos sociais, culturais e sustentabilidade

O projeto também deve contemplar os aspectos solicitados na atividade.

Devemos abordar pelo menos três temas entre:

- eficiência de comunicação e sustentabilidade;
- conhecimentos tradicionais/indígenas e decisões responsáveis sobre recursos;
- diversidade e inclusão cultural;
- transparência em decisões orientadas por dados;
- responsabilidade humana sobre decisões automatizadas;
- prevenção de linguagem discriminatória ou exclusão.

Esses temas precisam ser conectados ao SCIC.

Evitar um texto genérico desconectado do sistema.

---

# 30. Interface do sistema

Pasta:

```text
src/interface/
```

Arquivo:

```text
menu.py
```

O menu será responsável apenas pela interação com o usuário.

Exemplo:

```text
=========================================
       SCIC - AURORA SIGER
=========================================

1 - Carregar dados
2 - Consultar registros
3 - Calcular indicadores
4 - Calcular erros
5 - Executar previsão
6 - Avaliar modelo
7 - Priorizar alertas
8 - Buscar módulo por prefixo
9 - Calcular dados elétricos
10 - Executar análise completa
0 - Sair
```

O menu chama métodos da classe `SCIC`.

---

# 31. Regra de dependência

A arquitetura deve seguir aproximadamente:

```text
main.py
   ↓
SCIC
   ↓
+-------------------+
| Dados             |
| Análise           |
| Modelo            |
| Estruturas        |
| Eletricidade      |
| Interface         |
+-------------------+
```

Os módulos especializados não devem depender do `main.py`.

---

# 32. Organização das classes

Uma possibilidade:

```text
SCIC
│
├── GeradorDados
├── Indicadores
├── AnaliseErros
├── ModeloPrevisao
├── HeapAlertas
├── TrieModulos
├── CalculosEletricos
└── Menu
```

O `SCIC` funciona como fachada/orquestrador.

---

# 33. Fluxo de dados

O fluxo principal será:

```text
                 CSV
                  |
                  v
          +---------------+
          | Carregamento   |
          +---------------+
                  |
                  v
          +---------------+
          | DataFrame      |
          +---------------+
                  |
        +---------+---------+
        |         |         |
        v         v         v
   Indicadores  Erros    Modelo
        |         |         |
        |         |         v
        |         |     Métricas
        |         |
        |         v
        |     Alertas
        |         |
        |         v
        |        Heap
        |
        +----------------+
                         |
                         v
                       Trie
                         |
                         v
                  Consulta eficiente
```

---

# 34. Etapas de desenvolvimento

A equipe deve implementar o projeto nesta ordem.

## Etapa 1 — Estrutura do projeto

Criar:

```text
SCIC/
├── README.md
├── main.py
├── .dados/
├── .docs/
└── src/
```

Criar também os módulos vazios.

**Resultado esperado:** projeto executa sem erros estruturais.

---

# 35. Etapa 2 — Gerador de dados

Implementar:

```text
src/dados/gerador_dados.py
```

Objetivos:

- criar módulos;
- criar sensores;
- criar ciclos;
- gerar tensão;
- gerar corrente;
- calcular potência;
- gerar carga;
- gerar latência;
- inserir anomalias;
- definir status;
- criar alertas;
- salvar CSV.

**Resultado esperado:**

```text
.dados/dados_aurora_siger.csv
```

---

# 36. Etapa 3 — Carregamento

Implementar carregamento do CSV.

O SCIC deverá conseguir:

```text
CSV → DataFrame
```

Validar:

- colunas;
- tipos;
- valores ausentes;
- valores inválidos.

---

# 37. Etapa 4 — Indicadores

Implementar:

- média;
- mínimo;
- máximo;
- contagens;
- percentuais;
- indicadores operacionais.

Testar com o dataset gerado.

---

# 38. Etapa 5 — Erros

Implementar:

```text
erro absoluto
erro relativo
```

Validar casos extremos.

Gerar resultados que possam ser utilizados no relatório.

---

# 39. Etapa 6 — Modelo

Implementar:

```text
treino
↓
previsão
↓
teste
↓
MAE
MSE
RMSE
R²
```

Registrar os resultados.

---

# 40. Etapa 7 — Heap

Implementar primeiro a estrutura de baixo nível:

```text
src/estruturas_baixo_nivel/heap.py
```

Depois criar a camada de integração:

```text
src/estruturas/heap.py
```

Por fim:

```text
SCIC.priorizar_alertas()
```

---

# 41. Etapa 8 — Trie

Implementar primeiro:

```text
src/estruturas_baixo_nivel/no_trie.py
src/estruturas_baixo_nivel/trie.py
```

Depois:

```text
src/estruturas/trie.py
```

Por fim integrar:

```text
SCIC.buscar_por_prefixo()
```

---

# 42. Etapa 9 — Eletricidade e COA

Implementar:

```text
P = V × I
```

Adicionar a explicação da arquitetura:

```text
entrada → processamento → armazenamento → saída
```

Adicionar conversão de bases.

---

# 43. Etapa 10 — Menu

Implementar o menu.

O usuário deve conseguir executar as funcionalidades sem precisar conhecer a estrutura interna do código.

---

# 44. Etapa 11 — Integração

Executar o fluxo completo:

```text
Gerar dados
   ↓
Carregar dados
   ↓
Indicadores
   ↓
Erros
   ↓
Modelo
   ↓
Métricas
   ↓
Alertas
   ↓
Heap
   ↓
Trie
   ↓
Eletricidade
   ↓
Resultado final
```

Essa etapa é obrigatória antes da produção do relatório.

---

# 45. Etapa 12 — Testes

Cada módulo deve possuir testes básicos.

Testar principalmente:

### Dados

- geração;
- quantidade de registros;
- colunas;
- valores válidos.

### Indicadores

- médias;
- máximos;
- mínimos.

### Erros

- erro absoluto;
- erro relativo;
- divisão por zero.

### Modelo

- treinamento;
- previsão;
- métricas.

### Heap

- inserção;
- remoção;
- prioridade;
- ordenação.

### Trie

- inserção;
- busca;
- prefixos inexistentes;
- múltiplos resultados.

### Eletricidade

- tensão;
- corrente;
- potência.

---

# 46. Divisão de trabalho sugerida

A equipe pode ser dividida por módulos.

## Pessoa 1 — Dados

Responsável por:

```text
src/dados/
.dados/
```

Entregas:

- gerador;
- dataset;
- regras de geração;
- validação dos dados.

---

## Pessoa 2 — Análise e modelo

Responsável por:

```text
src/analise/
src/modelo/
```

Entregas:

- indicadores;
- erros;
- modelo;
- métricas.

---

## Pessoa 3 — Estruturas de dados

Responsável por:

```text
src/estruturas_baixo_nivel/
src/estruturas/
```

Entregas:

- Heap;
- Trie;
- nós;
- integração.

---

## Pessoa 4 — Eletricidade/COA/Interface

Responsável por:

```text
src/eletricidade/
src/interface/
```

Entregas:

- cálculos elétricos;
- conversão de bases;
- menu;
- apresentação dos resultados.

---

## Integração — todos

A integração final deve ser feita em conjunto.

Responsável final:

```text
src/scic/scic.py
main.py
README.md
.docs/relatorio_tecnico.pdf
```

---

# 47. Contrato entre módulos

Cada módulo deve receber dados e retornar resultados de maneira previsível.

Exemplo:

```python
resultado = indicadores.calcular_latencia_media(dados)
```

ou:

```python
previsoes = modelo.prever(dados)
```

Evitar que módulos alterem silenciosamente variáveis globais.

---

# 48. Regras de código

## Evitar

```python
dados = ...
resultado = ...
alertas = ...
```

espalhados por vários arquivos sem organização.

## Preferir

```python
class Indicadores:
    ...
```

```python
class ModeloPrevisao:
    ...
```

```python
class HeapAlertas:
    ...
```

```python
class TrieModulos:
    ...
```

---

# 49. Convenção de nomes

Classes:

```text
PascalCase
```

Exemplo:

```python
class ModeloPrevisao:
```

Funções:

```text
snake_case
```

Exemplo:

```python
calcular_erros()
```

Variáveis:

```text
snake_case
```

Exemplo:

```python
latencia_observada
```

---

# 50. Comentários

Os comentários devem explicar principalmente:

- decisões de implementação;
- regras de negócio;
- funcionamento das estruturas;
- fórmulas;
- partes que não sejam imediatamente óbvias.

Evitar comentários que simplesmente repetem o código.

---

# 51. Git e colaboração

Cada pessoa deve trabalhar preferencialmente em uma branch:

```text
feature/dados
feature/modelo
feature/heap-trie
feature/interface
```

Exemplos:

```text
feature/gerador-dados
feature/modelo-previsao
feature/estruturas-dados
feature/eletricidade
```

Após concluir uma funcionalidade:

```text
branch
   ↓
commit
   ↓
pull request
   ↓
review
   ↓
merge
```

---

# 52. Commits

Utilizar mensagens objetivas.

Exemplos:

```text
feat: adiciona gerador de dados da Aurora Siger
feat: implementa cálculo de erro absoluto e relativo
feat: adiciona modelo de previsão
feat: implementa heap de alertas
feat: implementa trie de módulos
feat: adiciona cálculos elétricos
feat: adiciona menu principal
fix: corrige cálculo de erro relativo
refactor: reorganiza integração do SCIC
docs: atualiza README
```

---

# 53. Regra importante para integração

Nenhuma pessoa deve criar um dataset próprio para seu módulo sem conversar com quem está responsável pelos dados.

Todos os módulos devem utilizar o mesmo universo de dados.

Exemplo:

```text
mesmo módulo
      ↓
mesmo sensor
      ↓
mesma carga
      ↓
mesma potência
      ↓
mesma latência
      ↓
mesmo alerta
```

Assim:

- o modelo utiliza os mesmos dados;
- o erro utiliza a mesma previsão;
- o Heap utiliza os mesmos alertas;
- a Trie utiliza os mesmos códigos;
- a eletricidade utiliza os mesmos valores;
- o relatório apresenta resultados coerentes.

---

# 54. Critério de integração

Antes de considerar o projeto concluído, deve ser possível executar:

```python
from src.scic.scic import SCIC

scic = SCIC()

scic.executar()
```

e chegar a um fluxo funcional sem precisar executar manualmente dezenas de scripts diferentes.

---

# 55. Checklist de conclusão

## Estrutura

- [ ] `README.md`
- [x] `codigo_fonte.py`
- [x] `.dados/`
- [ ] `.docs/`
- [ ] `src/`

## Dados

- [x] Dataset criado
- [x] Gerador implementado
- [x] Dados coerentes
- [x] Anomalias controladas
- [x] Potência relacionada a tensão/corrente

## Análise

- [x] Indicadores
- [x] Erro absoluto
- [x] Erro relativo
- [x] Interpretação dos erros (Fazer no relatório técnico)

## Modelo

- [x] Modelo simples
- [x] Treino/teste
- [x] MAE
- [x] MSE
- [x] RMSE
- [x] R²
- [x] Interpretação (Fazer no relatório técnico)

## Heap

- [x] Implementação de baixo nível
- [x] Nós/estrutura
- [x] Inserção
- [x] Remoção
- [x] Prioridade
- [x] Integração com alertas

## Trie

- [x] Implementação de baixo nível
- [x] Nós
- [x] Inserção
- [x] Busca
- [x] Busca por prefixo
- [x] Integração com módulos/sensores

## COA/Eletricidade

- [x] Entrada
- [x] Processamento
- [x] Armazenamento
- [x] Saída
- [x] Binário/decimal/hexadecimal
- [x] V × I = P

## Gestão inteligente

- [x] Monitoramento
- [x] Automação
- [x] Alertas
- [x] Previsão
- [x] Manutenção preditiva
- [x] Relação com resultados do SCIC

## Reflexão

- [x] Sustentabilidade
- [x] Responsabilidade humana
- [x] Transparência
- [x] Inclusão/diversidade
- [x] Uso responsável dos dados

## Integração

- [x] Classe `SCIC`
- [x] `main.py` executa o sistema
- [x] Menu funcional
- [x] Fluxo completo testado
- [x] README atualizado
- [x] Relatório final
- [ ] `link_video.txt`

---

# 56. Critério final de qualidade

O projeto não deve parecer:

```text
Exercício 1
+
Exercício 2
+
Exercício 3
+
Exercício 4
```

O objetivo é parecer:

```text
                    SCIC
                     |
        +------------+------------+
        |            |            |
      Dados       Análise      Operação
        |            |            |
        v            v            v
     Modelo       Métricas      Alertas
        |                           |
        |                           v
        |                          Heap
        |                           |
        v                           v
    Previsão                       Ação
        |
        +------------+
                     |
                     v
                   Trie
                     |
                     v
             Consulta eficiente
                     |
                     v
                Resultado
```

Cada componente deve utilizar dados provenientes do mesmo sistema e contribuir para a tomada de decisão operacional.

---

# 57. Entregável final

A estrutura final esperada:

```text
SCIC/
│
├── README.md
├── main.py
│
├── .dados/
│   ├── dados_aurora_siger.csv
│   └── dados_processados.csv
│
├── .docs/
│   ├── link_video.txt
│   └── relatorio_tecnico.pdf
│
├── src/
│   ├── __init__.py
│   │
│   ├── scic/
│   │   ├── __init__.py
│   │   └── scic.py
│   │
│   ├── dados/
│   │   ├── __init__.py
│   │   └── gerador_dados.py
│   │
│   ├── analise/
│   │   ├── __init__.py
│   │   ├── indicadores.py
│   │   └── erros.py
│   │
│   ├── modelo/
│   │   ├── __init__.py
│   │   └── previsao.py
│   │
│   ├── estruturas/
│   │   ├── __init__.py
│   │   ├── heap.py
│   │   └── trie.py
│   │
│   ├── estruturas_baixo_nivel/
│   │   ├── __init__.py
│   │   ├── heap.py
│   │   ├── trie.py
│   │   ├── no_heap.py
│   │   └── no_trie.py
│   │
│   ├── eletricidade/
│   │   ├── __init__.py
│   │   └── calculos.py
│   │
│   └── interface/
│       ├── __init__.py
│       └── menu.py
│
└── requirements.txt
```

---

# 58. Observação sobre o vídeo

O vídeo não faz parte do desenvolvimento automatizado neste plano.

A equipe deverá apenas manter:

```text
.docs/link_video.txt
```

para inserir posteriormente o link do vídeo apresentado pelo integrante responsável.

O roteiro da apresentação deverá ser construído depois que o sistema estiver funcional, para que a demonstração utilize resultados reais gerados pelo SCIC.

---

# 59. Próximo passo recomendado

Antes de começar a programar todos os módulos simultaneamente, a equipe deve fechar primeiro:

1. **schema definitivo do CSV**;
2. **lista definitiva de módulos da Aurora Siger**;
3. **regras de geração dos dados**;
4. **fórmula de prioridade dos alertas**;
5. **variáveis utilizadas pelo modelo**;
6. **regras que determinam `status` e `mensagem_alerta`**.

Depois disso, implementar o:

```text
gerador_dados.py
```

e gerar o primeiro:

```text
.dados/dados_aurora_siger.csv
```

Esse dataset será a base de integração de todo o restante do projeto.
