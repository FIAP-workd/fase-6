from src.utils import QuebraSecundaria
from src.estruturas_baixo_nivel import Trie
import pandas as pd


class Buscador:
    def __init__(self, dados):

        self._message = """
-------------------
Buscador de módulos
-------------------

1. Verificar existência do módulo por nome completo.
2. Verificar existência do módulo pelo início.
3. Busca pelo início do módulo.
4. Voltar
"""
        self._dict_opcao = {
            "1": self._existencia_modulo,
            "2": self._existencia_prefixo,
            "3": self._busca_por_prefixo,
            "4": self._voltar
        }
        
        self.trie = Trie()
        self._dados = dados
        self._inserir_modulos()


    def run(self):    
        try:
            while True:
                self._exibir_menu()
                opcao = input("Digite sua opção: ").strip()
                if opcao in self._dict_opcao:
                    self._dict_opcao[opcao]()
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
            
        except QuebraSecundaria:
            pass

    def _exibir_menu(self):
        print(self._message)

    def _inserir_modulos(self):
        for modulo in self._dados['modulo'].unique():
            self.trie.insert(modulo)


    def _existencia_modulo(self):
        word = input("Digite o módulo que deseja verificar a existência: ")
        
        if self.trie.search(word):
            print(f"Módulo {word} encontrado.")

        else:
            print(f"Módulo {word} não foi encontrado. Por favor verifique a palavra digitada.")

        self._pausar()
        

    def _existencia_prefixo(self):
        prefix = input("Digite o prefixo do módulo que deseja verificar a existência: ")
            
        if self.trie.starts_with(prefix):
            print(f"Existe módulos com o prefixo: {prefix}.")

        else:
            print(f"Não existe módulos com prefixo {prefix} cadastrados. Por favor, verifique valor passado.")

        self._pausar()


    def _busca_por_prefixo(self):
        prefix = input("Digite o prefixo que deseja procurar: ")

        words = self.trie.get_words_with_prefix(prefix)
        if not words:
            print("Nenhum módulo tem esse prefixo.")

        print(f"Foram encontrados os módulos: {", ".join(words)}")

        self._pausar()


    def _voltar(self):
        raise QuebraSecundaria

    def _pausar(self):
        input("Aperte ENTER para continuar")

    def _show(self):
        return self.trie


if __name__ == '__main__':
    dados = pd.read_csv(r".dados/dados_aurora_siger.csv")
    busca = Buscador(dados)
    busca.run()
#    busca._existencia_prefixo()