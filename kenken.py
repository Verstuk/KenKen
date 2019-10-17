import operator
from itertools import product, permutations
import re

import numpy as np


def calculate(numbers, target, op):
    operator_dict = {"+": operator.add,
                     "-": operator.sub,
                     "*": operator.mul,
                     "/": operator.truediv}

    running_total = numbers[0]
    for number in numbers[1:]:
        running_total = operator_dict[op](running_total, number)

    if running_total == target:
        return True
    return False


def valid_number(row, column, board, size):
    valid_row = set()
    for number in range(1, size + 1):
        if number not in board[row]:
            valid_row.add(number)

    valid_column = set()
    column_numbers = [int(board[i, column]) for i in range(size)]
    for number in range(1, size + 1):
        if number not in column_numbers:
            valid_column.add(number)

    valid_numbers = valid_row & valid_column
    yield from valid_numbers


def is_valid_sum(board, instruction_array, number_groups):
    for group in range(1, number_groups + 1):
        coordinates = []
        list_numbers = []
        next_group = 0
        for i, j in product([row for row in range(size)], [column for column in range(size)]):
            if instruction_array[i][j][0] == group:
                if len(instruction_array[i][j]) == 2:
                    next_group = 1
                    break
                target = instruction_array[i][j][1]
                op = instruction_array[i][j][2]
                list_numbers.append(int(board[i, j]))
        if next_group == 1:
            continue
        combination_numbers = permutations(list_numbers, len(list_numbers))
        for combination in combination_numbers:
            target_reached = calculate(combination, target, op)
            if target_reached:
                break
        if target_reached:
            continue
        else:
            return False
    return True


def is_full(board, size):
    for row in range(size):
        for column in range(size):
            if board[row, column] == 0:
                return False
    return True


def solve_board(board, instruction_array, size, number_groups):
    if is_full(board, size):
        if is_valid_sum(board, instruction_array, number_groups):
            return True, board
        return False, board
    for i, j in product([row for row in range(size)],
                        [column for column in range(size)]):  # Product is from itertools library
        if board[i, j] != 0:
            continue
        for number in valid_number(i, j, board, size):
            board[i, j] = number
            is_solved, board = solve_board(board, instruction_array, size, number_groups)
            if is_solved:
                return True, board
            board[i, j] = 0
        return False, board
    return False, board


def fill_obvious(board, instruction_array, size):
    # Заполните фиксированные номера
    for row in range(size):
        for column in range(size):
            if len(instruction_array[row][column]) == 2:
                board[row, column] = instruction_array[row][column][1]
    return board


if __name__ == "__main__":
    # Инструкции в массиве представлены в формате groupID, target, symbol.
    # ID группы необходим для ситуации, когда две соседние группы имеют одну и ту же цель и символ
    # Что есть возможность в игре
    # Квадраты, которые имеют фиксированное число, принимают номер группы и число в качестве входных данных. Не размещайте символ в квадрате
    # instruction_array = [[[1, 6, "*"],  [1, 6, "*"], [ 2, 1, "-"], [2, 1, "-"]],
    #                     [[3, 16, "*"], [1, 6, "*"], [4, 1, "-"], [5, 1, ""]],
    #                     [[3, 16, "*"], [3, 16, "*"], [4, 1, "-"], [6, 2, "/"]],
    #                     [[7, 6, "+"],  [7, 6, "+"], [7, 6, "+"], [6, 2,"/"]]]

    # instruction_array = [[[1, 11, '+'], [2,2,'/'], [2,2,'/'], [4, 20, '*'], [5, 6, '*'], [5, 6, '*']],
    #                      [[1, 11, "+"], [3, 3, '-'], [3, 3, '-'],[4, 20, '*'], [6, 3, '/'], [5, 6, '*']],
    #                      [[7, 240, '*'], [7, 240, '*'], [8, 6, '*'], [8, 6, '*'], [6, 3, '/'], [5, 6, '*']],
    #                      [[7, 240, '*'], [7, 240, '*'], [9, 6, '*'], [12, 7, '+'], [10, 30, '*'], [10, 30, '*']],
    #                      [[11, 6, '*'], [11, 6, '*'], [9, 6, '*'], [12, 7, '+'], [12, 7, '+'], [13, 9, '+']],
    #                      [[14, 8, '+'], [14, 8, '+'], [14, 8, '+'], [15, 2, '/'], [15, 2, '/'], [13, 9, '+']]]

    instruction_array = [[[1,24,'*'], [2,4,'-'], [2,4,'-'], [3,1,'-'], [3,1,'-']],
                         [[1,24,'*'], [1,24,'*'], [4,3,'+'],[4,3,'+'],[5,75,'*']],
                         [[6,3,'+'], [6,3,'+'], [7,10,'+'], [5,75,'*'], [5,75,'*']],
                         [[8,13,'+'], [8,13,'+'], [7,10,'+'], [7,10,'+'],[5,75,'*']],
                         [[8,13,'+'], [9,7,'+'], [9,7,'+'], [10,2,'/'], [10,2,'/']]]

    # instruction_array = []
    # dim2 = []
    # f = open('array_1.txt', 'r')
    # for s in f.readlines():
    #     s = s.strip()
    #     if s == '':
    #         instruction_array.append(dim2)
    #         dim2 = []
    #     else:
    #         dim1 = re.split('\s+', s)
    #         dim2.append(dim1)
    # if len(dim2) > 0:
    #     instruction_array.append(dim2)
    # f.close()

    number_groups = 10
    size = len(instruction_array[0])
    board = np.zeros(size * size).reshape(size, size)
    board = fill_obvious(board, instruction_array, size)
    is_solved, solved = solve_board(board, instruction_array, size, number_groups)
    if is_solved:
         print(solved)
