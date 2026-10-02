# fase-6
Código referente a fase 6 do primeiro ano do curso de ciência da computação da FIAP

## Modelo de previsão

No menu principal, selecione a opção **3 - Modelo de previsão**. O submenu
permite treinar uma regressão linear múltipla para estimar a
`latencia_observada` usando `carga`, `tensao`, `corrente` e `ciclo`.

Após o treinamento, é possível consultar uma amostra das previsões calculadas
para todos os registros, visualizar os dados de entrada e informar uma nova
instância de variáveis operacionais para obter a latência estimada.

Instale as dependências antes de executar o projeto:

```bash
python -m pip install -r requirements.txt
```
