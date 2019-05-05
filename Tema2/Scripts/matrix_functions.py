import numpy

from Utils.config import *


__author__ = "Mihaila Alexandra Ioana"
__version__ = "1.1"
__status__ = "Dev"


def sigma_u(A, i, p):
    # sigma(k = 1, i - 1) (l_ik * u_kp)
    sigma_sum = 0
    for k in range(1, i):
        l_ik = A[i - 1, k - 1]
        u_kp = 1 if k == p else A[k - 1, p - 1]
        sigma_sum += l_ik * u_kp

    return sigma_sum


def sigma_l(A, i, p):
    # sigma(k = 1, i - 1) (l_pk * u_ki)
    sigma_sum = 0
    for k in range(1, i):
        l_pk = A[p - 1, k - 1]
        u_ki = 1 if k == i else A[k - 1, i - 1]
        sigma_sum += l_pk * u_ki

    return sigma_sum


def LU_factorization(A, n):
    A_init = A

    for p in range(1, n + 1):
        # elements of p column for U: u(ip) = 1...p-1
        # NB: u(pp) = 1
        for i in range(1, p):
            a_ip = A_init[i - 1, p - 1]
            l_ii = A[i - 1, i - 1]
            if not numpy.abs(l_ii) > epsilon:
                print("[x] Matrix A has a null minor. We can't solve the system.")
                return False

            u_ip = (a_ip - sigma_u(A, i, p)) / l_ii
            A[i - 1, p - 1] = u_ip

        # elements of p line for L: l(pi) = 1...p
        for i in range(1, p + 1):
            a_pi = A_init[p - 1, i - 1]
            l_pi = a_pi - sigma_l(A, i, p)
            A[p - 1, i - 1] = l_pi

    print("a) printam descompunerea: L si U")
    print_L(A, n)
    print()
    print_U(A, n)
    print("{}\n".format("=" * 100))

    return A


def print_U(A, n):
    for l in range(1, n + 1):
        for c in range(1, n + 1):
            if c < l:
                print(0, end=' ')
            elif c == l:
                print(1, end=' ')
            else:
                print(A[l - 1, c - 1], end=' ')

        print()


def print_L(A, n):
    for l in range(1, n + 1):
        for c in range(1, n + 1):
            if c <= l:
                print(A[l - 1, c - 1], end=' ')
            else:
                print(0, end=' ')
        print()


def determinant_L(A, n, print_determinant=False):
    if print_determinant:
        print("b) printam descompunerea: determinantul A\n")

    det = 1
    for i in range(1, n + 1):
        det *= A[i - 1, i - 1]

    if print_determinant:
        print("{}\n{}\n".format(det, "=" * 100))

    return det


def sigma_x_L(A, x, i):
    # sigma (j = 1, i - 1) (a_ij * x_j)
    sigma_sum = 0
    for j in range(1, i):
        sigma_sum += A[i - 1, j - 1] * x[j - 1]

    return sigma_sum


def sigma_x_U(A, n, x, i):
    # sigma (j = i + 1, n) (a_ij * x_j)
    sigma_sum = 0
    for j in range(i + 1, n + 1):
        sigma_sum += A[i - 1, j - 1] * x[j - 1]

    return sigma_sum


def solve_system(A, n, b, x):
    print("c) printam solutia aprox: x_LU")
    if not determinant_L(A, n):
        return []

    for i in range(1, n + 1):
        if not numpy.abs(A[i - 1, i - 1]) > epsilon:
            return []

        x_i = (b[i - 1] - sigma_x_L(A, x, i)) / A[i - 1, i - 1]
        x = numpy.append(x, x_i)

    for i in range(n, 0, -1):
        x_i = x[i - 1] - sigma_x_U(A, n, x, i)
        x[i - 1] = x_i

    print("{}\n{}\n".format(x, "=" * 100))

    return x


def check_solution(A_init, b, x, n):
    print("d) printam norma: || A_init * x_LU - b_init ||2 < 10 ** (-8)")

    # A_init * x = y
    y = numpy.array([])
    for i in range(1, n + 1):
        y_i = 0
        for j in range(1, n + 1):
            y_i += A_init[i - 1, j - 1] * x[j - 1]

        y = numpy.append(y, y_i)

    z = numpy.subtract(y, b)
    euclidean_norm = 0
    for i in range(1, n + 1):
        euclidean_norm += z[i - 1] ** 2

    m = numpy.sqrt(euclidean_norm)
    print("{} < 10 ** (-8) = {}\n{}\n".format(
        m,
        m < 10 ** (-8),
        "=" * 100
    ))


def bonus(A_init, n, b, x):
    print("e) printam bonusul")
    x_lib = numpy.linalg.solve(A_init, b)
    A_inverse = numpy.linalg.inv(A_init)

    print("x_lib = {}".format(x_lib))
    print("A^-1 = {}".format(A_inverse))

    b_1 = numpy.subtract(x, x_lib)
    euclidean_norm = 0
    for i in range(1, n + 1):
        euclidean_norm += b_1[i - 1] ** 2

    print("\n|| x_LU - x_lib ||2 = {}".format(numpy.sqrt(euclidean_norm)))

    b_2 = numpy.subtract(x, numpy.matmul(A_inverse, b))
    euclidean_norm = 0
    for i in range(1, n + 1):
        euclidean_norm += b_2.item((0, i - 1)) ** 2

    print("\n|| x_LU - A_lib ^-1 * b_init ||2 = {}".format(numpy.sqrt(euclidean_norm)))
