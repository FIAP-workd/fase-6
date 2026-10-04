from __future__ import annotations
from typing import Any, Optional

class TrieNode:
    def __init__(self) -> None:
        self.children = {}
        self._isEndOfWord = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        current = self.root

        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]

        current._isEndOfWord = True

    def search(self, word: str) -> bool:
        current = self.root

        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]

        return current._isEndOfWord

    def starts_with(self, prefix: str) -> bool:
        current = self.root

        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True
    
    def get_words_with_prefix(self, prefix: str) -> list[str]:
        """Retorna uma lista com todas as palavras que começam com o prefixo informado."""
        current = self.root

        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        # 2. Coleta todas as palavras válidas abaixo desse nó usando DFS
        words = []
        words = self._collect_words(current, prefix, words)
        return words

    def _collect_words(self, node: TrieNode, current_word: str, words: list[str]) -> None:
        """Função auxiliar recursiva para navegar pela árvore coletando palavras."""
        if node._isEndOfWord:
            words.append(current_word)
        
        # Explora todos os caracteres filhos ordenados alfabeticamente
        for char in sorted(node.children.keys()):
            self._collect_words(node.children[char], current_word + char, words)

        return words

    def __str__(self):
        """Gera uma representação visual da Trie em formato de árvore."""
        if not self.root.children:
            return "Trie vazia"
        
        linhas = ["(raiz)"]
        self._gerar_estrutura(self.root, "", linhas)
        return "\n".join(linhas)

    def _gerar_estrutura(self, node: TrieNode, prefixo_visual: str, linhas: list) -> None:
        chaves = sorted(node.children.keys())
        
        for i, char in enumerate(chaves):
            eh_ultimo = (i == len(chaves) - 1)
            # Trocado de ├──/└── para |-- e +-- que nunca dão erro de unicode
            galho = "+-- " if eh_ultimo else "|-- "
            
            filho = node.children[char]
            marcador_fim = " *" if filho._isEndOfWord else ""
            
            linhas.append(f"{prefixo_visual}{galho}{char}{marcador_fim}")
            
            proximo_prefixo = prefixo_visual + ("    " if eh_ultimo else "|   ")
            self._gerar_estrutura(filho, proximo_prefixo, linhas)


    
        



if __name__ == '__main__':
    word = 'apple'
    word2 = 'app'
    word3 = 'tree'
    word4 = 'bargain'
    t = Trie()
    t.insert(word)
    t.insert(word2)
    t.insert(word3)
    t.insert(word4)
    words = t.get_words_with_prefix('ap')
    print(words)
#    print(t)
#    print(t.starts_with('ap'))
#    print(t.search('appl'))