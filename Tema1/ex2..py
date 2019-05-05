import tkinter

from ex1 import get_u

u = get_u()
x = 1.0
y, z = u, u


def plus_asociativ(x, y, z):
    if (x + y) + z == x + (y + z):
        return True

    return False


def inmultire_asociativa(x, y, z):
    while (x * y) * z == x * (y * z):
        x = x + 1

    return x


def start_app(punctul_a, punctul_b):
    title = "Exercitiul nr. 2"
    size = "450x100"

    root = tkinter.Tk()
    root.title(title)
    root.geometry(size)

    frame = tkinter.Frame(root)
    frame.pack()

    p_a = tkinter.Label(frame, text=punctul_a)
    p_a.pack()

    p_b = tkinter.Label(frame, text=punctul_b)
    p_b.pack()

    root.mainloop()


if __name__ == '__main__':
    punctul_a_adevarat = "a) ({0} + {1}) + {2} == {0} + ({1} + {2}) -> adevarat".format(x, y, z)
    punctul_a_fals = "a) ({0} + {1}) + {2} != {0} + ({1} + {2}) -> fals".format(x, y, z)
    if not plus_asociativ(x, y, z):
        punctul_a = punctul_a_fals
    else:
        punctul_a = punctul_a_adevarat

    punctul_b = "b) ({0} * {1}) * {2} != {0} * ({1} * {2}) -> x = {0}, y = {1}, z = {2}".\
                format(inmultire_asociativa(x, y, z), y, z)

    start_app(punctul_a, punctul_b)
