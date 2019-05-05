import tkinter

__authors__ = ["Mihaila Alexandra Ioana", "Dupu Robert-Daniel"]
__version__ = "1.0"
__status__ = "Dev"


def solve_u():
    u = 0.1
    while 1 + u != 1:
        u /= 10

    return u * 10


def get_u():
    return solve_u()


def start_app(text):
    title = "Exercitiul nr. 1"
    size = "300x100"

    root = tkinter.Tk()
    root.title(title)
    root.geometry(size)

    frame = tkinter.Frame(root)
    frame.pack()

    label = tkinter.Label(frame, text=text)
    label.pack()

    root.mainloop()


if __name__ == "__main__":
    text = "u = {}".format(solve_u())
    start_app(text)
