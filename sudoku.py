import itertools
from functools import reduce
import time

array = [0 if x is '.' else int(x) for x in '010020300004003050060000007005200040000800001020091000300005090000700805007000000']


def get_row(array, idx):
    return array[idx*9: (idx+1)*9]


def get_column(array, idx):
    return [array[i*9+idx] for i in range(9)]


def get_block(array, idx):
    row = idx // 3
    col = idx % 3
    #print(row, col)
    result = [array[i*9 + col*3+row*27: i*9+row*27+(col+1)*3] for i in range(3)]
    return [x for r in result for x in r]


def which_block(r, c):
    return r // 3 * 3 + c // 3


def valid(array, r, c):
    lst = list(filter(lambda x: x!=0, get_row(array, r)))
    if len(lst) != len(set(lst)):
        return False
    lst = list(filter(lambda x: x != 0, get_column(array, c)))
    if len(lst) != len(set(lst)):
        return False
    lst = list(filter(lambda x: x != 0, get_block(array, which_block(r, c))))
    if len(lst) != len(set(lst)):
        return False
    return True


def print_sudoku(array):
    for i in range(9):
        print(array[i*9:(i+1)*9])


def potential(array, r, c):
    remains = list(range(1, 10))
    for n in filter(lambda x: x!=0, itertools.chain(get_row(array, r),
                             get_column(array, c),
                             get_block(array, which_block(r, c)))):
        if n in remains:
            remains.remove(n)
    return remains


def get_search_space(array):
    search_space = []
    for r in range(9):
        for c in range(9):
            if array[r*9+c] == 0:
                search_space.append(((r, c), potential(array, r, c)))

    search_space.sort(key=lambda x: len(x[1]))
    return search_space, reduce(lambda x,y: x*y, [len(x[1]) for x in search_space], 1.0)


def solve(array, position_lookup, i):
    if i == len(position_lookup):
        return True
    (r, c),  p = position_lookup[i]
    for _p in p:
        array[r*9+c] = _p
        if valid(array, r, c):
            if solve(array, position_lookup, i+1):
                return True
        array[r*9+c] = 0
#
    return False
#
#
if __name__ == '__main__':
    start = time.time()
    print_sudoku(array)
    search_space, size = get_search_space(array)
    print(size)
    if solve(array, search_space, 0):
        print_sudoku(array)

    print('elapsed: ', time.time() - start)