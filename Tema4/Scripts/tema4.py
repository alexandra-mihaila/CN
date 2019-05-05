import os


__author__ = "Dupu Robert-Daniel"
__version__ = "1.1"
__status__ = "Dev"


def citire(filename):
    with open(filename, 'r') as f:
        n = int(f.readline())
        b = []
        A = [[] for _ in range(n)]
        for line in f.readlines():
            if line != '\n':
                val = float(line.split(',')[0])
                if len(line.split(',')) > 1:
                    i = int(line.split(',')[1])
                    j = int(line.split(',')[2])
                    nuExista = True
                    for l in range(len(A[i])):
                        if A[i][l][1] == j:
                            A[i][l][0] += val
                            nuExista = False
                            break
                    if nuExista:
                        A[i].append([val, j])
                else:
                    b.append(val)

    return A, b


def diagonalaNenula(A):
    esp = 1e-10
    for i in range(len(A)):
        j = -1
        for l in range(len(A[i])):
            if i == A[i][l][1]:
                j = l
                break
        if j > 0 and A[i][j][0] - 0 > esp:
            return False

    return True


def inmultesteVector(A, x):
    vec = []
    for i in range(len(A)):
        sum = 0
        for l in range(len(A[i])):
            sum = sum + A[i][l][0] * x[A[i][l][1]]
        vec.append(sum)
    return vec


def obtineComponente(A):
    n = len(A)

    # D = diagonala  L = trunghiul inferior U = triunghiul superior
    D = []
    L = []
    U = []
    for i in range(n):
        lineL = []
        lineU = []
        for l in range(len(A[i])):
            if A[i][l][1] == i:
                D.append([A[i][l][0]])
            elif A[i][l][1] < i:
                lineL.append([A[i][l][0], A[i][l][1]])
            else:
                lineU.append([A[i][l][0], A[i][l][1]])
        L.append(lineL)
        U.append(lineU)
    return D, L, U


def sumOriVal(v, x):
    sum = 0
    for i in range(len(v)):
        sum += (v[i][0] * x[v[i][1]])
    return sum


def vectoriEgali(v1, v2):
    if len(v1) != len(v2):
        return False

    esp = 1e-7
    for i in range(len(v1)):
        if abs(v1[i] - v2[i]) > esp:
            return False

    return True


def Xsor(A, b, w):
    # x(0) = [0,0,.....]
    n = len(b)
    x = [0 for _ in range(n)]
    k = 0
    D, L, U = obtineComponente(A)
    while not vectoriEgali(inmultesteVector(A, x), b):
        k += 1
        for i in range(n):
            x[i] = (1 - w) * x[i] + (w / D[i][0]) * (b[i] - sumOriVal(L[i], x) - sumOriVal(U[i], x))

        if k > 100:
            break

    print("[i] Numar iteratii: {}".format(k))
    return x


def norma(v1, v2):
    max = 0
    for i in range(len(v1)):
        if abs(v1[i] - v2[i]) > max:
            max = abs(v1[i] - v2[i])

    return max


def start(filename):
    A, b = citire(filename)

    for w in [0.8, 1, 1.2]:
        print("[i] w = {}".format(w))
        x = Xsor(A, b, w)
        output_file = os.path.join(r'..\Utils\output', os.path.basename(filename)[:-4] + '_x_' + str(w) + '.txt')
        with open(output_file, 'w') as fout:
            fout.write(str(x))

        print("[i] Am scris in {}".format(output_file))
        print("[i] Norma = {}\n".format(norma(inmultesteVector(A, x), b)))


if __name__ == '__main__':
    start(r'..\Utils\input\m_rar_2019_1.txt')
    # start(r'..\Utils\input\m_rar_2019_2.txt')
    # start(r'..\Utils\input\m_rar_2019_3.txt')
    # start(r'..\Utils\input\m_rar_2019_4.txt')
    # start(r'..\Utils\input\m_rar_2019_5.txt')
