import numpy
import json

with open('a.json', 'r') as f:
    data = json.load(f)

A = numpy.matrix(data[0])
b = numpy.array(data[1])
x = numpy.array([])
n = len(A)
esp = data[2]


def sigma_u(i, p):
    # sigma(k = 1, i - 1) (l_ik * u_kp)
    sigma_sum = 0
    for k in range(1, i):
        l_ik = A[i - 1, k - 1]
        u_kp = 1 if k == p else A[k - 1, p - 1]
        sigma_sum += l_ik * u_kp

    return sigma_sum


def sigma_l(i, p):
    # sigma(k = 1, i - 1) (l_pk * u_ki)
    sigma_sum = 0
    for k in range(1, i):
        l_pk = A[p - 1, k - 1]
        u_ki = 1 if k == i else A[k - 1, i - 1]
        sigma_sum += l_pk * u_ki

    return sigma_sum


def LU_factorization():
    for p in range(1, n + 1):
        # elements of p column for U: u(ip) = 1...p-1
        # NB: u(pp) = 1
        for i in range(1, p):
            a_ip = A_init[i - 1, p - 1]
            l_ii = A[i - 1, i - 1]
            if not numpy.abs(l_ii) > esp:
                return False

            u_ip = (a_ip - sigma_u(i, p)) / l_ii
            A[i - 1, p - 1] = u_ip

        # elements of p line for L: l(pi) = 1...p
        for i in range(1, p + 1):
            a_pi = A_init[p - 1, i - 1]
            l_pi = a_pi - sigma_l(i, p)
            A[p - 1, i - 1] = l_pi

    return True


def print_U():
    for l in range(1, n + 1):
        for c in range(1, n + 1):
            if c < l:
                print(0, end=' ')
            elif c == l:
                print(1, end=' ')
            else:
                print(A[l - 1, c - 1], end=' ')

        print()


def print_L():
    for l in range(1, n + 1):
        for c in range(1, n + 1):
            if c <= l:
                print(A[l - 1, c - 1], end=' ')
            else:
                print(0, end=' ')
        print()


def determinant_L():
    det = 1
    for i in range(1, n + 1):
        det *= A[i - 1, i - 1]

    return det


def sigma_x_L(i):
    # sigma (j = 1, i - 1) (a_ij * x_j)
    sigma_sum = 0
    for j in range(1, i):
        sigma_sum += A[i - 1, j - 1] * x[j - 1]

    return sigma_sum


def sigma_x_U(i):
    # sigma (j = i + 1, n) (a_ij * x_j)
    sigma_sum = 0
    for j in range(i + 1, n + 1):
        sigma_sum += A[i - 1, j - 1] * x[j - 1]

    return sigma_sum


def solve_system():
    global x

    if not determinant_L():
        return []

    for i in range(1, n + 1):
        if not numpy.abs(A[i - 1, i - 1]) > esp:
            return []

        x_i = (b[i - 1] - sigma_x_L(i)) / A[i - 1, i - 1]
        x = numpy.append(x, x_i)

    for i in range(n, 0, -1):
        x_i = x[i - 1] - sigma_x_U(i)
        x[i - 1] = x_i


def norm():
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

    return numpy.sqrt(euclidean_norm)


if __name__ == '__main__':
    A_init = A.copy()
    done = LU_factorization()
    if not done:
        print("[x] Matrix A has a null minor. We can't solve the system.")
        exit()

    # punctul a
    print("a) printam descompunerea: L si U")
    print_L()
    print()
    print_U()

    print("=" * 100)
    print()

    # punctul b
    print("b) printam descompunerea: determinantul A")
    print(determinant_L())
    print()
    print("=" * 100)
    print()

    # punctul c
    print("c) printam solutia aprox: x_LU")
    solve_system()
    print(x)
    print()
    print("=" * 100)
    print()

    # punctul d
    print("d) printam norma: || A_init * x_LU - b_init ||2")
    print(norm())
    print()
    print("=" * 100)
    print()

    # bonus
    print("e) printam bonusul")
    x_lib = numpy.linalg.solve(A_init, b)
    A_inverse = numpy.linalg.inv(A_init)

    print("x_lib = ", end='')
    print(x_lib)
    print()
    print("A^-1 = ", end='')
    print(A_inverse)

    b_1 = numpy.subtract(x, x_lib)
    euclidean_norm = 0
    for i in range(1, n + 1):
        euclidean_norm += b_1[i - 1] ** 2

    print("\n|| x_LU - x_lib ||2 = ", end='')
    print(numpy.sqrt(euclidean_norm))

    b_2 = numpy.subtract(x, numpy.matmul(A_inverse, b))
    euclidean_norm = 0
    for i in range(1, n + 1):
        euclidean_norm += b_2.item((0, i - 1)) ** 2

    print("\n|| x_LU - A_lib ^-1 * b_init ||2 = ", end='')
    print(numpy.sqrt(euclidean_norm))


