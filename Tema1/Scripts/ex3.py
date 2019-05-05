import tkinter
import math
import time

import numpy

__authors__ = ["Mihaila Alexandra Ioana", "Dupu Robert-Daniel"]
__version__ = "1.1"
__status__ = "Dev"

n = 1000
frequency_array = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
c = [1 / math.factorial(i) for i in range(1, 14, 2)]


def get_n_values(n):
    return numpy.random.uniform(-numpy.pi / 2, numpy.pi / 2, n)


def get_error(polynomial_i, x):
    return abs(polynomial_i - math.sin(x))


def polynomial_1(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * c[2]))


def polynomial_2(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] - y * c[3])))


def polynomial_3(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] + y * (-c[3] + y * c[4]))))


def polynomial_4(x):
    y = (x ** 2)
    return x * (1 + y * (-0.166 + y * (0.00833 + y * (-c[3] + y * c[4]))))


def polynomial_5(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] + y * (-c[3] + y * (c[4] - y * c[5])))))


def polynomial_6(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] + y * (-c[3] + y * (c[4] + y * (-c[5] + y * c[6]))))))


def solve():
    values = get_n_values(n)
    polynomials = [polynomial_1, polynomial_2, polynomial_3, polynomial_4, polynomial_5, polynomial_6]
    for v in values:
        index = 1
        current_errors = list()
        for solve_polynomial in polynomials:
            error = get_error(solve_polynomial(v), v)
            current_errors.append([index, error])
            index += 1

        current_errors.sort(key=lambda x: x[1])
        for i in range(0, 3):
            frequency_array[current_errors[i][0]][1] += 1

    frequency_array.sort(key=lambda x: x[1], reverse=True)
    frequency_array.remove([0, 0])
    return [x[0] for x in frequency_array]


def bonus():
    solving_times = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
    values = get_n_values(n * 10)
    polynomials = [polynomial_1, polynomial_2, polynomial_3, polynomial_4, polynomial_5, polynomial_6]
    for v in values:
        index = 0
        for solve_polynomial in polynomials:
            start_time = time.time()
            solve_polynomial(v)
            solving_times[index][1] += (time.time() - start_time)
            index += 1

    solving_times.sort(key=lambda x: x[1])
    return solving_times


def start_app(top_6, solving_times):
    title = "Exercitiul nr. 3"
    size = "300x300"

    part_a = "Top dupa acuratete:\n1. P{}\n2. P{}\n3. P{}\n4. P{}\n5. P{}\n6. P{}".format(top_6[0], top_6[1], top_6[2],
                                                                                          top_6[3], top_6[4], top_6[5])
    part_b = "Top dupa timp:\n1. P{}: {}s\n2. P{}: {}s\n3. P{}: {}s\n4. P{}: {}s\n5. P{}: {}s\n6. P{}: {}s".format(
        solving_times[0][0], solving_times[0][1], solving_times[1][0], solving_times[1][1], solving_times[2][0],
        solving_times[2][1], solving_times[3][0], solving_times[3][1], solving_times[4][0], solving_times[4][1],
        solving_times[5][0], solving_times[5][1])

    text = "{}\n\n\n{}".format(part_a, part_b)

    root = tkinter.Tk()
    root.title(title)
    root.geometry(size)

    frame = tkinter.Frame(root)
    frame.pack()

    label = tkinter.Label(frame, text=text)
    label.pack()

    root.mainloop()


if __name__ == '__main__':
    top_6 = solve()
    solving_times = bonus()
    start_app(top_6, solving_times)
