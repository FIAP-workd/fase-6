from datetime import datetime
from dataclasses import dataclass
from src.estruturas_baixo_nivel import Heap
from src.utils import QuebraSecundaria


@dataclass
class Modulo:
    nome: str
    ciclo: int
    tipo: str
    prioridade: str
    status: str
    mensagem_alerta: str
    data: str

def calcular_prioridade(modulo: Modulo) -> int:
    prioridade_status = {
        "Critico": 2,
        "Alerta": 1,
        "Normal": 0
    }

    prioridade_nivel = {
        "Critica":3,
        "Alta": 2,
        "Media": 1,
        "Nenhuma": 0
    }

    status = prioridade_status[modulo.status]
    nivel = prioridade_nivel[modulo.prioridade]

    base = status * 10 + nivel

    return base * 1000 - modulo.ciclo

class GerenciadorAlertas:
    def __init__(self, dados):
        self.heap = Heap()
        self._dados = dados
        self.__message_menu = """
----------------------
Gerenciador de Alertas
----------------------

1. Visualizar próximo alerta a ser atendido.
2. Adicionar Alerta.
3. Marcar alerta prioritário como realizado.
4. Sair
"""
        self.dict_opcoes = {
            "1": self.visualizar_proximo_alerta,
            "2": self.adicionar_alertas,
            "3": self.alerta_solucionado,
            "4": self._voltar
        }

        self.registrar_fila_prioridade()


    def registrar_fila_prioridade(self):
        list_modulos = []
        for _, row in self._dados.iterrows():
            nome = row['modulo']
            ciclo = int(row['ciclo'])
            tipo = row['tipo_modulo']
            prioridade = row['prioridade']
            status = row['status']
            mensagem_alerta = row['mensagem_alerta']
            data = row['data']
            modulo_temp = Modulo(nome=nome, ciclo=ciclo, tipo=tipo, prioridade=prioridade, status=status, mensagem_alerta=mensagem_alerta, data=data)
            valor_prioridade = calcular_prioridade(modulo_temp)
            tupla_fila = (valor_prioridade, modulo_temp)
            if not status == 'Normal':
                list_modulos.append(tupla_fila)

        self.heap.heapify(list_modulos)

    def adicionar_alertas(self):
        def _get_ciclo():
            try:
                value = int(input("Insira o número do ciclo: "))
                return value
            except:
                print("Valor inválido.")
                _get_ciclo()

        def _get_prioridade():
            print("1.Crítica\n2.Alta\n3.Media\n4.Nenhuma")
            _dict_op = {"1":"Critica", "2":"Alta", "3":"Media", "4":"Nenhuma"}
            opcao = input("Digite o valor da proridade: ")
            if opcao not in _dict_op:
                return _get_prioridade()
            return _dict_op.get(opcao)
        
        nome = input("Insira o nome do módulo")
        ciclo = _get_ciclo()
        tipo = input("Insira o tipo do módulo")
        prioridade = _get_prioridade()
            

    def visualizar_proximo_alerta(self):
        try:
            next_alerta = self.heap.peek_top()
            print("Alerta que necessita ser analisado.")
            print(f"Nome do Modulo: {next_alerta[1].nome}")
            print(f"Tipo: {next_alerta[1].tipo}")
            print(f"Prioridade: {next_alerta[1].prioridade}")
            print(f"Status: {next_alerta[1].status}")
            print(f"Mensagem Alerta: {next_alerta[1].mensagem_alerta}")
            print(f"Data Alerta: {next_alerta[1].data}")

        except IndexError:
            print("Fila de prioridades está vazia.")

        finally:
            self._pausar()


    def alerta_solucionado(self):
        try: 
            element = self.heap.extract_top()
            print(f"Alerta {element[1].nome} retirado.")
        except IndexError:
            print("Fila de prioridades está vazia.")
        finally:
            self._pausar()

    def _voltar(self):
        raise QuebraSecundaria

    def _exibir_menu(self):
        print(self.__message_menu)

    def run(self):
        try:
            while True:
                self._exibir_menu()
                opcao = input("Digite sua opção: ").strip()
                if opcao in self.dict_opcoes:
                    self.dict_opcoes[opcao]()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
            
        except QuebraSecundaria:
            pass

    def _pausar(self):
        input("Pressione ENTER para continuar...")
