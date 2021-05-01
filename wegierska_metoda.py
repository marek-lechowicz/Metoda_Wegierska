from typing import List
import numpy as np


class Matrix:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = np.array(matrix)
        self.size = len(matrix)

    def reduce_and_get_sum(self):
        reduction_sum = 0

        for row in range(self.size):
            min_value = min(self.matrix[row])
            reduction_sum += min_value
            for col in range(self.size):
                self.matrix[row][col] -= min_value

        return reduction_sum

    def reduce_matrix(self):
        reduction_sum = 0

        # reduce rows and update reduction sum
        reduction_sum += self.reduce_and_get_sum()

        # reduce cols and update reduction sum
        self.matrix = self.matrix.T
        reduction_sum += self.reduce_and_get_sum()
        self.matrix = self.matrix.T

        return reduction_sum

    def searching_independent_zero(self):

        independent_row = []
        independent_col = []
        # DO POPRAWY poniższy kod  zadziała tylko w korzystnym przypadku, nie miałem lepszego pomysłu
        for row in range(self.size):
            for col in range(self.size):
                if (self.matrix[row][col] == 0) and (row not in independent_row) and (col not in independent_col):
                    independent_row.append(row)
                    independent_col.append(col)
                    break

        independent = []
        for element in range(len(independent_row)):
            index = (independent_row[element], independent_col[element])
            independent.append(index)

        return independent
    
    def get_result(self):   # zwracanie wyniku końcowego jeśli liczba nizależnych zer jest równa rozmiarowi macierzy

        result = self.searching_independent_zero()
        if len(result) == self.size:
            return result
        
# to w celach testowych było, macierz jest z jego przykładu, można wywalić
if __name__ == '__main__':
    matrix_example = Matrix([
        [5, 2, 3, 2, 7],
        [6, 8, 4, 2, 5],
        [6, 4, 3, 7, 2],
        [6, 9, 0, 4, 0],
        [4, 1, 2, 4, 0]
    ])

    print('Macierz przed redukcją:\n', matrix_example.matrix)
    print('\nSuma redukcji: ', matrix_example.reduce_matrix(), '\n')
    print('Macierz po redukcji:\n', matrix_example.matrix)
