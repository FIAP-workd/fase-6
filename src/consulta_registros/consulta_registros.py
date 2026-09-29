from src.utils import QuebraSecundaria
import pandas as pd


class Consulta:
    def __init__(self, registros: pd.DataFrame):
        self.registros = registros
        self.dict_opcoes = {
            "1": self._exibir_primeiros_registros,
            "2": self._exibir_ultimos_registros,
            "3": self._consultar_por_modulo,
            "4": self._consultar_por_tipo_modulo,
            "5": self._consultar_por_status,
            "6": self._voltar
        }
        self.menu_message = """
---------------------
Consulta de registros
---------------------

1. Exibir primeiros registros
2. Exibir últimos registros
3. Consultar por módulo
4. Consultar por tipo de módulo
5. Consultar por status
6. Voltar

"""

    def _exibir_menu(self):
        print(self.menu_message)

    def run(self):
        try:
            while True:
                self._exibir_menu()
                print(self.menu_message)
                opcao = input("Digite sua opção: ").strip()
                if opcao in self.dict_opcoes:
                    self.dict_opcoes[opcao]()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
            
        except QuebraSecundaria:
            pass


    def get_num_registros(self, tipo):
        try:
            num_registros = int(input(f"Digite o número de {tipo} registros que deseja exibir: "))
            return num_registros
        except ValueError:
            print("Valor inválido. Por favor, digite um número inteiro.")
            return self.get_num_registros(tipo)

    def _exibir_primeiros_registros(self):
        numero_primeiros_registros = self.get_num_registros("primeiros")
        
        print(f"\nExibindo os {numero_primeiros_registros} primeiros registros:\n")
        print(self.registros.head(numero_primeiros_registros))

    def _exibir_ultimos_registros(self):
        numero_ultimos_registros = self.get_num_registros("últimos")
        
        print(f"\nExibindo os {numero_ultimos_registros} últimos registros:\n")
        print(self.registros.tail(numero_ultimos_registros))

    def _consultar_por_modulo(self):
        modulo = input("Digite o módulo que deseja consultar: ").strip()

        if modulo not in self.registros["modulo"].values:
            print(f"\nMódulo '{modulo}' não encontrado nos registros.\n")
            return

        registros_filtrados = self.registros[self.registros["modulo"] == modulo]
        
        if registros_filtrados.empty:
            print(f"\nNenhum registro encontrado para o módulo '{modulo}'.\n")
        else:
            print(f"\nRegistros encontrados para o módulo '{modulo}':\n")
            print(registros_filtrados)


    def _consultar_por_tipo_modulo(self):
        tipo_modulo = input("Digite o tipo de módulo que deseja consultar: ").strip()

        if tipo_modulo not in self.registros["tipo_modulo"].values:
            print(f"\nTipo de módulo '{tipo_modulo}' não encontrado nos registros.\n")
            return

        registros_filtrados = self.registros[self.registros["tipo_modulo"] == tipo_modulo]
        
        if registros_filtrados.empty:
            print(f"\nNenhum registro encontrado para o tipo de módulo '{tipo_modulo}'.\n")
        else:
            print(f"\nRegistros encontrados para o tipo de módulo '{tipo_modulo}':\n")
            print(registros_filtrados)

    def _consultar_por_status(self):
        dict_status = {
            1: "Crítico",
            2: "Alerta",
            3: "Normal"
        }
        status = int(input("Digite o status que deseja consultar: \n1. Crítico\n2. Alerta\n3. Normal").strip())
        if status not in (1, 2, 3):
            print("\nStatus inválido. Por favor, escolha uma opção válida.\n")
            return

        status_nome = dict_status[status]
        registros_filtrados = self.registros[self.registros["status"] == status_nome]

        if registros_filtrados.empty:
            print(f"\nNenhum registro encontrado para o status '{status_nome}'.\n")
        else:
            print(f"\nRegistros encontrados para o status '{status_nome}':\n")
            print(registros_filtrados)

    def _voltar(self):
        raise QuebraSecundaria