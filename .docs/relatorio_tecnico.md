# Relatório Técnico - SCIC Aurora Siger.
Grupo:  
PEDRO CESAR FERNANDES DE BRITO,  
Gabriel Coutinho Barcelos,  
Matheus de Carvalho Teodoro,  
Luis Gustavo Ribeiro Andrade,  
João Victor Viana Feitosa  


# Fase 6 - SCIC

O objetivo da missão da fase é construir um Sistema de Comunicação Interplanetária da Colônia. As missões principais que precisávamos resolver são:  
* Coleta e organização dos dados;
* Cálculo dos indicadores;
* Modelo de Previsão com Avaliação;
* Priorização de Alertas com Heap;
* Consulta de Módulos com Trie;
* Geração do Relatório.

Cada ponto abordamos de uma forma diferente no processo, mas geramos todos em uma estrutura única de desenvolvimento.

## Estrutura do desenvolvimento.

Durante a construção do código, optamos por uma técnica de código mais limpo, onde dividimos tudo em classes, e cada execução estará voltada como uma classe. Dessa forma, o nosso arquivo principal apenas chamará a classe do SCIC e executará uma função que vai executar toda a estratégia principal.

Essa forma, facilita a manutenção do código, além de ficar mais alinhado com a técnica SOLID, uma vez que temos Single Responsability, e Open-Closed Principles.

Como podemos reparar, isso minimiza a quantidade de linhas de códigos dos nossos arquivos. Essa técnica de separarmos as funções por arquivos semelhantes, se chama Modularização, e utilizarmos de Classes para fazer essa Modularização nos permite deixar o código mais genérico e replicável.

## Coleta e organização dos dados.

Ao iniciarmos a classe do SCIC, estamos inicialmente realizando os pontos de chamada da nossa classe GeradorDados(), isso faz com que possamos capturar informações compartilhadas entre essas duas classes, e caso o arquivo com os dados simulados não exista, estaremos realizando a execução do Gerador de Dados para que o arquivo passa a existir no caminho desejado. Note que utilizando a modularização por classes, podemos compartilhar os caminhos com um único comando. Dessa forma, minimizamos trabalho duplicado, em caso de termos que alterar o caminho de output, e o caminho de leitura dos dados.

A organização dos dados se dá pelo formato de .csv, e o arquivo é salvo na pasta .dados do repositório. Facilitando assim o acesso a pasta.

## Menu de opções e pontos que resolvem

Dentro do nosso SCIC, geramos um Menu de opções, sendo que cada um desses pontos do Menu são chamados para resolver um ponto adicional das informações que estão por ali.

No menu, temos ali as seguintes opções:
```
1 - Consultar registros
2 - Analisar indicadores
3 - Modelo de previsão
4 - Gerenciar Alertas
5 - Buscar módulos
6 - Analisar consumo e eletricidade
7 - Sair
```

Cada menu resolve um problema, e utiliza de uma técnica ensinada em aula.

Os principais pontos resolvidos pelo Menu são:
> __Consultar Registros:__ Consulta os dados gerados pelos dados simulados.  
__Analisar indicadores:__ Calcula os indicadores dos dados, mostrando os principais pontos que devemos ter atenção.  
__Modelo de previsão:__ Realiza o modelo de regressão linear com os dados existêntes e avalia a qualidade do modelo resolvido.  
__Gerenciar Alertas:__ Gerenciamento de alertas, com uma fila de prioridade com uma estrutura de MaxHeap.  
__Buscar módulos:__ Busca os módulos existentes com base na estrutura de uma Trie.
__Analisar consumo e eletricidade:__ Realiza a análise do consumo e da eletricidade dos pontos 

Pelo menu, podemos analisar que maior parte dos nossos grandes problemas estão resolvidos pelo processo. Mas vamos destrinchar melhor cada tópico.

## Consultar Registros

Utilizando da nossa estrutura, ao chamarmos a função de consultar registros, somos enviados a uma classe de Consulta de Registros. Essa classe vai receber os dados lidos pelo SCIC e utilizar para realizar as nossas primeiras visualizações.

O Consultar Registros é um dos módulos mais simples, ele trabalha com manipulações de DataFrames Pandas.

Dentro da própria classe, temos um outro menu. Ali, decidimos qual próximo passo vamos seguir, podemos exibir os primeiros registros, que vai exibir o .head do dataframe, o que exibe últimos registros, que vai mostrar agora o .tail, e as outras funções do Menu, vai mostrar para nós o dataframe com filtros aplicados.

## Modelo de Previsão.

Diante do modelo de previsão.