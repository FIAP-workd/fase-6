from __future__ import annotations

class Heap:
    
    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def __repr__(self):
        return str(self.heap)

    def insert(self, key, value):
        self.heap.append((key, value))
        self._sift_up(len(self.heap) - 1)

    def peek_top(self):
        if not self.heap:
            raise IndexError('Heap Vazio!')
        return self.heap[0]

    def extract_top(self):
        if not self.heap:
            raise IndexError('Heap Vazio!')

        element = self.heap[0]
        last_element = self.heap.pop()

        if self.heap:
            self.heap[0] = last_element
            self._sift_down(0)

        return element

    def heapify(self, elements: list):
        self.heap = list(elements)

        for i in reversed(range(self._parent(len(self.heap)-1)+1)):
            self._sift_down(i)


    def meld(self, other_heap: Heap):
        combined_heap = self.heap + other_heap.heap
        self.heapify(combined_heap)

        other_heap.heap = []

    def _parent(self, index):
        return (index-1) // 2 if index != 0 else None

    def _left(self, index):
        left = 2 * index + 1
        return left if left < len(self.heap) else None

    def _right(self, index):
        right =  2*index+2 
        return right if right < len(self.heap) else None

    def _sift_up(self, index):
        parent_index = self._parent(index)

        # Lógica aqui está de maxheap
        while parent_index is not None and self.heap[index][0] > self.heap[parent_index][0]:
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            index = parent_index
            parent_index = self._parent(index)

    def _sift_down(self, index):

        while True:

            greater = index

            left = self._left(index)
            right = self._right(index)

            if left is not None and self.heap[left][0] > self.heap[greater][0]:
                greater = left

            if right is not None and self.heap[right][0] > self.heap[greater][0]:
                greater = right

            if greater == index:
                break

            self.heap[index], self.heap[greater] = self.heap[greater], self.heap[index]
            index = greater

if __name__ == '__main__':
    h = Heap()

    h.heapify([(70, 'valor_armazenar 1'), (50, 'valor_armazenar 2')])
    print(h)
    h.insert(80, 'valor_armazenar 3')
    print(h)
    h.insert(75, 'valor_armazenar 4')
    print(h)
    h.extract_top()
    print(h)
    h.extract_top()
    print(h)