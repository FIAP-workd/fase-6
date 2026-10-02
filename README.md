# fase-6
Código referente a fase 6 do primeiro ano do curso de ciência da computação da FIAP

## Modelo de previsão

No menu principal, selecione a opção **3 - Modelo de previsão**. O submenu
permite treinar uma regressão múltipla para estimar a
`latencia_observada` usando `carga`, `tensao`, `corrente` e `ciclo`, além de
termos quadráticos e logarítmicos dessas variáveis para capturar tendências
não lineares.

Após o treinamento, é possível consultar uma amostra das previsões calculadas
para todos os registros, visualizar os dados de entrada e informar uma nova
instância de variáveis operacionais para obter a latência estimada.
Também é possível gerar arquivos PNG em `.dados/graficos_modelo` com os erros
residuais, a comparação entre previsão e observação, a relação log-linear
entre carga e latência e a relação quadrática entre carga e tensão.

Instale as dependências antes de executar o projeto:

```bash
python -m pip install -r requirements.txt
```
