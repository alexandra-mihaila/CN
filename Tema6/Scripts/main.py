import json
import random
import fractions
import warnings

from Utils.config import *

warnings.filterwarnings("ignore", category=DeprecationWarning)
__author__ = "Alexandra Mihaila Ioana"
__version__ = "1.2"
__status__ = "Dev"


def write_result(x_k, file_name):
    with open(file_name, 'a') as file_handler:
        file_handler.write("{}\n".format(", ".join([str(item) for item in x_k])))


def first_derivative(polynomial):
    polynomial_order = len(polynomial) - 1
    n = len(polynomial)
    return [polynomial[i] * (polynomial_order - i) for i in range(n - 1)]


def second_derivative(first_derivative_of_polynomial):
    return first_derivative(first_derivative_of_polynomial)


def horner_method(polynomial, value):
    b_0 = polynomial[0]
    b_i_minus_1 = b_0
    for i in range(1, len(polynomial)):
        b_i = polynomial[i] + b_i_minus_1 * value
        b_i_minus_1 = b_i

    return b_i_minus_1


def get_x_i(polynomial, x, bonus=False):
    horner_polynomial = horner_method(polynomial, x)
    horner_polynomial_first_derivative = horner_method(first_derivative(polynomial), x)
    horner_polynomial_second_derivative = horner_method(second_derivative(polynomial), x)

    Q = 1
    if not bonus:
        Q = fractions.gcd(horner_polynomial, horner_polynomial_first_derivative)

    A = 2 * (horner_polynomial_first_derivative ** 2) - ((horner_polynomial / Q) * horner_polynomial_second_derivative)
    if abs(A) < epsilon:
        return [None, None]

    delta = ((horner_polynomial / Q) * horner_polynomial_first_derivative) / A
    x_i = x - delta

    return [x_i, delta]


def halley_method(polynomial, limit, bonus=False):
    for iteration in range(nr_iterations):
        x_k = list()
        x_0 = random.uniform(-limit, limit)
        x_k.append(x_0)
        x, delta = get_x_i(polynomial, x_0, bonus)
        if not delta:
            continue

        x_k.append(x)
        k = 2
        while epsilon <= abs(delta) <= 10 ** 8 and k <= nr_iterations:
            x, delta = get_x_i(polynomial, x, bonus)
            if not delta:
                delta = 10 ** (-5)
                break

            x_k.append(x)
            k += 1

        if abs(delta) < epsilon:
            print("[i] Done: x_0 = {}, x_k = {}, iteration = {}, k = {}".format(x_0, x, iteration, k))
            if bonus:
                return x_k

            for i in range(k):
                for j in range(i + 1, k - 1):
                    if abs(x_k[i] - x_k[j]) <= epsilon:
                        x_k.remove(x[i])
                        break

            return x_k


def find_limit(polynomial):
    return (abs(polynomial[0]) + max(polynomial[1:])) / abs(polynomial[0])


def print_polynomial(polynomial, derivative_order=0):
    polynomial_order = len(polynomial) - 1
    print("\tP" + "'" * derivative_order + "(x) = {}x^{}".format(polynomial[0], polynomial_order), end='')

    for i in range(1, polynomial_order):
        if polynomial[i] >= 0:
            print(" + {}x^{}".format(polynomial[i], polynomial_order - i), end='')
        else:
            print(" - {}x^{}".format(polynomial[i] * (-1), polynomial_order - i), end='')

    if polynomial[-1] >= 0:
        print(" + {}".format(polynomial[-1]))
    else:
        print(" - {}".format(polynomial[-1] * (-1)))


def get_random_polynomial(polynomials):
    all_orders = [item for item in polynomials["order"]]
    random_order = random.choice(all_orders)
    random_index = random.randrange(0, len(polynomials["order"][random_order]))
    return [polynomials["order"][random_order][random_index], random_order, random_index]


def load_polynomials(file_name=r'../Utils/polynomials.json'):
    with open(file_name, 'r') as file_handler:
        return json.load(file_handler)


def main():
    print("[i] Started")
    polynomials = load_polynomials()
    polynomial, random_order, random_index = get_random_polynomial(polynomials)

    print("[i] We've chosen:", end='')
    print_polynomial(polynomial)

    limit = find_limit(polynomial)
    interval = [-limit, limit]
    print("[i] We're working in {} interval".format(interval))

    print("[i] Searching for approximation to the polynomial's root")
    x_k = halley_method(polynomial, limit, bonus=True)
    if not x_k:
        print("[x] Done. No result")
        return

    file_name = r'../Results/{}_{}.txt'.format(random_order, random_index)
    write_result(x_k, file_name)


if __name__ == '__main__':
    main()
