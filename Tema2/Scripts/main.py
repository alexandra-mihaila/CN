import json

from Scripts.matrix_functions import LU_factorization, determinant_L, solve_system, check_solution, bonus, numpy

__author__ = "Mihaila Alexandra Ioana"
__version__ = "1.1"
__status__ = "Dev"


def load_input(file_name=r'../Utils/data.json'):
    with open(file_name, 'r') as file_handler:
        return json.load(file_handler)


def main():
    data = load_input()
    A_init = numpy.matrix(data[0])
    b = numpy.array(data[1])
    x = numpy.array([])
    n = len(A_init)

    LU = LU_factorization(A_init.copy(), n)
    if LU is False:
        return

    determinant_L(LU, n, print_determinant=True)
    x = solve_system(LU, n, b, x)
    check_solution(A_init, b, x, n)
    bonus(A_init, n, b, x)


if __name__ == '__main__':
    main()
