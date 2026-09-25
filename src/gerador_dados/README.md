# Regras de Geração de Dados — Aurora Siger

## 1. Objetivo

O módulo `src/dados/gerador_dados.py` é responsável por criar o universo de dados utilizado na simulação da estrutura marciana **Aurora Siger**.

O gerador deve produzir dados coerentes entre si. As variáveis não devem ser sorteadas de forma independente, pois o dataset será utilizado posteriormente para demonstrar estruturas de dados, regras de negócio, detecção de anomalias e previsão.

O arquivo gerado é:

```text
.dados/dados_aurora_siger.csv
```

---

## 2. Classe principal

A implementação deve utilizar a classe:

```python
GeradorDados
```

O arquivo deve permanecer em:

```text
src/
└── dados/
    └── gerador_dados.py
```

O caminho de saída fica definido no `__init__`:

```python
self.output_path = Path(".dados/dados_aurora_siger.csv")
```

Esse caminho pode ser alterado diretamente quando necessário.

---

## 3. Módulos simulados

A Aurora Siger possui os seguintes módulos:

| Módulo | Tipo | Criticidade |
|---|---|---|
| COM-01 | Comunicacao | Critica |
| COM-02 | Comunicacao | Critica |
| COM-03 | Comunicacao | Media |
| ENE-01 | Energia | Critica |
| ENE-02 | Energia | Alta |
| LAB-01 | Laboratorio | Alta |
| HAB-01 | Habitacao | Alta |
| HAB-02 | Habitacao | Media |
| MED-01 | Medico | Critica |
| ADM-01 | Administrativo | Baixa |

Cada módulo possui um perfil próprio de:

- tensão nominal;
- corrente nominal;
- latência base;
- criticidade;
- prioridade padrão.

A intenção é que módulos diferentes apresentem comportamentos diferentes mesmo quando submetidos às mesmas condições gerais da estação.

---

## 4. Ciclos de monitoramento

Cada ciclo representa uma coleta de dados.

Por padrão:

```text
quantidade de ciclos = 1000
intervalo = 10 minutos
```

Cada ciclo gera um registro para cada módulo.

Com 1000 ciclos e 10 módulos:

```text
1000 × 10 = 10.000 registros
```

O campo `ciclo` identifica a coleta e o campo `data` registra o instante correspondente.

---

## 5. Identificação

Cada registro possui:

```text
id
ciclo
modulo
tipo_modulo
codigo_sensor
```

O `id` é único em todo o dataset.

O sensor é associado diretamente ao módulo:

```text
COM-01 → SNS-COM-01
ENE-01 → SNS-ENE-01
MED-01 → SNS-MED-01
```

---

## 6. Relação entre carga e tempo

A carga deve possuir continuidade temporal.

Não é desejável que:

```text
ciclo 1  → 20%
ciclo 2  → 93%
ciclo 3  → 7%
```

sem uma causa.

A carga atual deve depender parcialmente da carga anterior, de uma condição global da estação e de ruído.

A fórmula implementada é conceitualmente:

```text
carga atual =
    82% da carga anterior
  + 12% de uma condição média da estação
  + 6% de uma variação adicional
```

O resultado é limitado ao intervalo:

```text
0% ≤ carga ≤ 100%
```

Isso cria uma série temporal mais realista.

---

## 7. Potência

A potência nunca deve ser sorteada independentemente.

A regra obrigatória é:

```text
P = V × I
```

No código:

```python
potencia = tensao * corrente
```

Consequentemente, alterações na tensão ou corrente também alteram a potência.

---

## 8. Tensão

A tensão parte de um valor nominal específico de cada módulo.

A tensão pode apresentar:

- pequena variação aleatória;
- pequena queda quando a carga está muito elevada;
- queda significativa quando ocorre uma anomalia de tensão.

Exemplo conceitual:

```text
tensão = tensão nominal
       - efeito da carga
       + ruído
```

Em uma anomalia de queda de tensão, a tensão é reduzida de maneira significativa.

---

## 9. Corrente

A corrente possui relação com a carga.

Quanto maior a carga:

```text
maior tendência de corrente
```

A corrente também possui pequeno ruído.

Em uma anomalia de corrente:

```text
corrente > corrente nominal esperada
```

Isso pode provocar aumento de potência.

---

## 10. Latência prevista

A latência prevista depende do perfil do módulo e da carga.

Regra conceitual:

```text
latência prevista =
    latência base
    + efeito da carga
```

No código:

```python
latencia_prevista = latencia_base + 0.70 × carga
```

Portanto, módulos com diferentes latências-base possuem comportamentos diferentes.

---

## 11. Latência observada

A latência observada é derivada da latência prevista.

Regra:

```text
latência observada =
    latência prevista
    + ruído
    + efeito de eventual anomalia
```

Isso cria uma relação que poderá ser utilizada posteriormente em modelos estatísticos ou de previsão.

A carga também influencia a latência de forma indireta e direta.

---

## 12. Condição global da estação

Além das características individuais dos módulos, cada ciclo possui uma condição global.

Essa condição combina:

- componente sazonal;
- ruído pequeno.

A finalidade é fazer com que módulos diferentes apresentem alguma correlação temporal sem produzir exatamente os mesmos valores.

---

## 13. Anomalias

Aproximadamente:

```text
5% dos registros
```

devem receber alguma situação anormal.

O valor de 5% é uma probabilidade aproximada, não uma obrigação de exatamente 5.000 registros em um dataset de 100.000 registros.

Os tipos de anomalia são:

```text
latencia_alta
carga_alta
queda_tensao
corrente_alta
comunicacao_degradada
```

### 13.1 Latência alta

A latência observada sofre um aumento significativo.

### 13.2 Carga alta

A carga tende a atingir uma condição elevada e também pode provocar aumento adicional de latência.

### 13.3 Queda de tensão

A tensão é reduzida em relação ao valor nominal.

### 13.4 Corrente alta

A corrente sofre aumento acima do comportamento nominal.

Como:

```text
P = V × I
```

isso também altera a potência.

### 13.5 Comunicação degradada

A latência observada aumenta significativamente, representando degradação da comunicação entre Marte e Terra.

---

## 14. Status

O status não deve ser sorteado.

Ele deve ser consequência das condições observadas.

Valores utilizados:

```text
Normal
Alerta
Critico
```

Exemplo:

```text
sem condição anormal → Normal
uma condição anormal → Alerta
múltiplas condições graves → Critico
```

---

## 15. Prioridade

A prioridade deve considerar a criticidade do módulo.

Módulos críticos recebem maior prioridade quando ocorre uma condição anormal.

Valores:

```text
Nenhuma
Baixa
Media
Alta
Critica
```

Para registros normais:

```text
prioridade = Nenhuma
```

Para registros anormais:

- módulo crítico → Critica;
- módulo de alta criticidade → Alta;
- módulo de média/baixa criticidade → Media.

---

## 16. Mensagem de alerta

A mensagem deve ser derivada das condições encontradas.

Exemplos:

```text
Sem alertas
```

ou:

```text
Carga elevada
```

ou:

```text
Latência muito alta
```

ou:

```text
Queda de tensão; corrente acima do nominal
```

Não gerar mensagens aleatórias que não correspondam às medições.

---

## 17. Estrutura final do CSV

O dataset deve possuir as seguintes colunas:

```text
id
ciclo
modulo
tipo_modulo
codigo_sensor
tensao
corrente
potencia
carga
latencia_prevista
latencia_observada
status
prioridade
mensagem_alerta
data
```

---

## 18. Validações obrigatórias

Antes de salvar o CSV, o gerador deve verificar:

### Potência

```python
potencia == tensao * corrente
```

considerando uma pequena tolerância numérica.

### Carga

```text
0 ≤ carga ≤ 100
```

### Latência

```text
latencia_observada > 0
```

### Anomalias

O dataset não deve ultrapassar uma quantidade exagerada de registros anormais.

O código utiliza 15% como limite superior de segurança para detectar uma geração incompatível com a regra aproximada de 5%.

---

## 19. Reprodutibilidade

O gerador possui uma `seed`.

Exemplo:

```python
GeradorDados(seed=42)
```

Isso permite reproduzir a mesma geração de dados.

Para gerar uma simulação diferente, pode-se alterar a seed.

---

## 20. Execução

A partir da raiz do projeto:

```bash
python src/dados/gerador_dados.py
```

Ou:

```python
from src.dados.gerador_dados import GeradorDados

gerador = GeradorDados(
    quantidade_ciclos=1000,
    intervalo_minutos=10,
    seed=42,
)

caminho = gerador.gerar()

print(caminho)
```

---

## 21. Responsabilidade da Pessoa 1

A Pessoa 1 é responsável por:

```text
src/dados/
.dados/
```

Entregas:

- implementação do gerador;
- definição dos perfis dos módulos;
- geração do dataset;
- regras de coerência;
- validação dos dados.

O gerador não deve implementar estruturas de dados como:

- árvore;
- heap;
- fila;
- pilha;
- matriz;
- hash table.

Essas estruturas pertencem às demais partes do sistema e utilizarão o dataset gerado como entrada.

---

## 22. Princípio geral

O dataset deve representar um sistema físico e operacional plausível.

A regra principal é:

> **Uma variável deve possuir uma justificativa baseada em outras variáveis ou no estado do sistema.**

Exemplos:

```text
carga → corrente
carga → latência
tensão + corrente → potência
anomalia → alteração das medições
criticidade + anomalia → prioridade
medições + regras → status
status + condição → mensagem
```

Dessa forma, o dataset poderá ser utilizado posteriormente para demonstrar análise, previsão, detecção de anomalias e estruturas de dados sem depender de números completamente desconectados.
