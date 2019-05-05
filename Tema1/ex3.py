import tkinter

import numpy as np
import math
import time


n = 1000
frequency_array = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
c = [1 / math.factorial(i) for i in range(1, 14, 2)]


def get_n_values(n):
    return np.random.uniform(-np.pi / 2, np.pi / 2, n)


def get_error(polinom_i, x):
    return abs(polinom_i - math.sin(x))


def polinom1(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * c[2]))


def polinom2(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] - y * c[3])))



def polinom3(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] + y * (-c[3] + y * c[4]))))


def polinom4(x):
    y = (x ** 2)
    return x * (1 + y * (-0.166 + y * (0.00833 + y * (-c[3] + y * c[4]))))


def polinom5(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] + y * (-c[3] + y * (c[4] - y * c[5])))))


def polinom6(x):
    y = (x ** 2)
    return x * (1 + y * (-c[1] + y * (c[2] + y * (-c[3] + y * (c[4] + y * (-c[5] + y * c[6]))))))


def solve():
    values = get_n_values(n)
    polynomials = [polinom1, polinom2, polinom3, polinom4, polinom5, polinom6]
    for v in values:
        index = 1
        current_errors = list()
        for p in polynomials:
            error = get_error(p(v), v)
            current_errors.append([index, error])
            index += 1

        current_errors.sort(key=lambda x: x[1])
        for i in range(0, 3):
            frequency_array[current_errors[i][0]][1] += 1

    frequency_array.sort(key=lambda x: x[1], reverse=True)
    frequency_array.remove([0, 0])
    return [x[0] for x in frequency_array]


def bonus():
    times = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]
    values = get_n_values(n * 10)
    polynomials = [polinom1, polinom2, polinom3, polinom4, polinom5, polinom6]
    for v in values:
        index = 0
        for p in polynomials:
            start_time = time.time()
            p(v)
            times[index][1] += (time.time() - start_time)
            index += 1

    times.sort(key=lambda x: x[1])
    return times


def start_app(top_6, times):
    title = "Exercitiul nr. 3"
    size = "300x300"

    part_a = "Top dupa acuratete:\n1. P{}\n2. P{}\n3. P{}\n4. P{}\n5. P{}\n6. P{}".format(top_6[0], top_6[1], top_6[2], top_6[3], top_6[4], top_6[5])
    part_b = "Top dupa timp:\n1. P{}: {}\n2. P{}: {}\n3. P{}: {}\n4. P{}: {}\n5. P{}: {}\n6. P{}: {}".format(times[0][0], times[0][1], times[1][0], times[1][1], times[2][0], times[2][1], times[3][0], times[3][1], times[4][0], times[4][1], times[5][0], times[5][1])

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
    times = bonus()
    start_app(top_6, times)
