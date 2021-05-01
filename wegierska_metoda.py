from typing import List
import numpy as np
from copy import deepcopy
from random import randint


class Matrix:
    def __init__(self, matrix: List[List[int]]):
        self.matrix = np.array(matrix)
        self.base_matrix = deepcopy(self.matrix)
        self.size = len(matrix)
        self.independent_row = list()
        self.independent_col = list()

    def reduce_helper(self):
        # funkcja pomocnicza do funkcji reduce_matrix

        # iterujemy po rzędach macierzy
        for row in range(self.size):
            # znajdujemy minimalną wartość w danym rzędzie
            min_value = min(self.matrix[row])
            # iterujemy po kolumnach, czyli po każdym elemencie z danego wiersza i odejmujemy od niego minimalną wartość
            for col in range(self.size):
                self.matrix[row][col] -= min_value

    def reduce_matrix(self):
        # funkcja redukująca macierz

        # redukcja wierszy
        self.reduce_helper()

        # redukcja kolumn - ponieważ funkcja reduce_helper iteruje po wierszach, to najpier należy dokonać transpozycji
        # macierzy, tak aby jej kolumny 'stały się' wierszami, jest to prostsza operacja
        self.matrix = self.matrix.T
        self.reduce_helper()
        # po zredukowaniu transponujemy macierz ponownie, w celu uzyskania wynikowej macierzy po redukcji
        self.matrix = self.matrix.T

    def min_lines(self):
        # funkcja wykreślająca zera w macierzy minimalną liczbą linii

        # utworzenie zmiennych, któe przechowywać będą "wykreślone" wierze i kolumny
        self.independent_row = []
        self.independent_col = []

        # iteracja po całej macierzy
        for row in range(self.size):
            for col in range(self.size):
                # sprawdzamy iedy element jest równy zero i czy nie jest wykreślony, jeśli te warunki są spełnione, to
                # przechodzimy dalej
                if (self.matrix[row][col] == 0) and (row not in self.independent_row) and (col not in self.independent_col):
                    # jeśli w rzędzie jest więcej
                    if list(self.matrix[row]).count(0) > 1:
                        self.independent_row.append(row)
                        break
                    if list(self.matrix[:, col]).count(0) > 1:
                        self.independent_col.append(col)
                        break
                    self.independent_row.append(row)
                    break

    def create_additional_zeros(self):
        # funkcja powiększająca zbiór zer niezależnych

        # znalezienie minimalnego elementu w niewykreślonej części
        min_element = np.inf
        # iterujemy po całej macierzy
        for row in range(self.size):
            for col in range(self.size):
                # sprawdzamy tylko te elementy, które nie są zakreślone
                if (row not in self.independent_row) and (col not in self.independent_col):
                    # sprawdzamy czy dany element jest mniejszy niż aktualnie rozważany
                    if self.matrix[row, col] < min_element:
                        # jeśli tak to aktualizujemy zmienną min_element
                        min_element = self.matrix[row, col]

        # odjęcie minimalnego elementu od niewykreślonej części
        # iterujemy po całej macierzy
        for row in range(self.size):
            for col in range(self.size):
                # odejmujemy minimalny element od tych elementów, które nie są zakreślone
                if (row not in self.independent_row) and (col not in self.independent_col):
                    self.matrix[row, col] -= min_element

                # dodanie minimalnego elementu do wszystkich elementów przykrytych dwoma liniami
                elif (row in self.independent_row) and (col in self.independent_col):
                    self.matrix[row, col] += min_element

    def get_total_cost(self):
        # funkcja obliczająca koszt oraz przydział zadań
        optimal_points = []
        total_cost = 0

        chosen_col = []
        chosen_row = []

        # iterujemy po całej macierzy
        for row in range(self.size):
            minimal_zeros = np.inf
            best_candidate = []
            for col in range(self.size):
                # szukamy elementu w danym wierszu, który jest równy 0 i niezakreślony
                if (self.matrix[row, col] == 0) and (col not in chosen_col):
                    number_of_zeros = 0
                    # obliczenie liczby niewykreślonych zer w kolumnie o indeksie zera, które znaleźliśmy w poprzednim
                    # kroku dla danego wiersza
                    for col_row in range(self.size):
                        if (self.matrix[col_row, col] == 0) and (col_row not in chosen_row):
                            number_of_zeros += 1
                    # jeśli liczba zer jest mniejsza niż aktualna, to znaleźliśmy przydział zadania
                    if number_of_zeros < minimal_zeros:
                        minimal_zeros = number_of_zeros
                        best_candidate = [row, col]

            # aktualizujemy przydział zadań oraz całkowity koszt
            optimal_points.append((best_candidate[0], best_candidate[1]))
            total_cost += self.base_matrix[best_candidate[0], best_candidate[1]]

        # funkcja zwraca przydział zadań oraz całkowity koszt ich wykonania
        return optimal_points, total_cost

    def hungarian_method(self):
        # przebieg metody węgierskiej

        # na początku dokonujemy redukcji macierzy
        self.reduce_matrix()
        # następnie wyznaczamy pokrycie zer macierzy minimalną liczbą linii
        self.min_lines()
        print("\n\nMacierz pośrednia:\n", self.matrix)

        while True:
            # sprawdzamy czy liczba minimlalnych linii jest równa wymiarowi macierzy
            if len(self.independent_col) + len(self.independent_row) == self.size:
                # jeśli tak, algorytm kończy pracę i zwracamy wynik
                return self.get_total_cost()
            # w przeciwnym wypadku
            else:
                # dokonujemy próby powiększenia zbioru zer niezależnych
                self.create_additional_zeros()
                # szukamy minimalnej liczby linii
                self.min_lines()
                print("\n\nMacierz pośrednia:\n", self.matrix)


if __name__ == '__main__':
    # matrix_example = Matrix([
    #     [5, 2, 3, 2, 7],
    #     [6, 8, 4, 2, 5],
    #     [6, 4, 3, 7, 2],
    #     [6, 9, 0, 4, 0],
    #     [4, 1, 2, 4, 0]
    # ])
    #
    # print('Macierz przed redukcją:\n', matrix_example.matrix)
    # print('\nSuma redukcji: ', matrix_example.reduce_matrix(), '\n')
    # print('Macierz po redukcji:\n', matrix_example.matrix)

    # matrix_example = Matrix([
    #     [82, 83, 69, 92],
    #     [77, 37, 49, 92],
    #     [11, 69, 5, 86],
    #     [8, 9, 98, 23]
    # ])
    #
    # matrix_example2 = Matrix([
    #     [20, 40, 10, 50],
    #     [100, 80, 30, 40],
    #     [10, 5, 60, 20],
    #     [70, 30, 10, 25]
    # ])
    #
    # print("Wynik", matrix_example.hungarian_method())
    # print("Wynik2", matrix_example2.hungarian_method())

    # matrix_example = Matrix([
    #     [5, 2, 3, 2, 7, 4, 10],
    #     [6, 8, 4, 2, 5, 72, 1],
    #     [6, 4, 3, 7, 2, 2, 3],
    #     [6, 9, 0, 4, 0, 3, 5],
    #     [4, 1, 2, 4, 0, 1, 1],
    #     [9, 2, 7, 3, 2, 10, 2],
    #     [12, 2, 3, 2, 3, 1, 9]
    # ])
    # print("Macierz początkowa: \n", matrix_example.base_matrix)
    # result = matrix_example.hungarian_method()
    # print("\n\nMacierz końcowa: \n", matrix_example.matrix)
    # print("\n\nWynik", result)
    #
    # matrix_example = Matrix([
    #     [5, 2, 3, 2, 7, 4, 10],
    #     [6, 8, 4, 1, 5, 72, 7],
    #     [6, 4, 3, 7, 2, 2, 3],
    #     [6, 9, 0, 4, 0, 3, 5],
    #     [4, 3, 2, 4, 0, 3, 8],
    #     [9, 2, 7, 3, 2, 10, 2],
    #     [12, 2, 3, 2, 3, 2, 9]
    # ])
    # print("Macierz początkowa: \n", matrix_example.base_matrix)
    # result = matrix_example.hungarian_method()
    # print("\n\nMacierz końcowa: \n", matrix_example.matrix)
    # print("\n\nWynik", result)
    #
    # matrix_example = []
    # for i in range(7):
    #     matrix_example.append([])
    #     for j in range(7):
    #         matrix_example[i].append(randint(3, 15))
    #
    # matrix_example = Matrix(matrix_example)

    matrix_example = Matrix([[4, 6, 6, 5, 10, 6, 7],
                             [7, 13, 10, 9, 15, 12, 14],
                             [7, 13, 13, 13, 9, 12, 11],
                             [0, 10, 6, 8, 5, 6, 12],
                             [7, 4, 8, 15, 13, 11, 5],
                             [3, 3, 4, 4, 4, 5, 10],
                             [15, 12, 15, 14, 10, 12, 5]])

    print("Macierz początkowa: \n", matrix_example.base_matrix)
    result = matrix_example.hungarian_method()
    print("\n\nMacierz końcowa: \n", matrix_example.matrix)
    print("\n\nWynik", result)







