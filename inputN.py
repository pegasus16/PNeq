import numpy as np
from qiskit import circuit as Qcir
from qiskit import QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
import qiskit.circuit.library.standard_gates.x as stXgate
import matplotlib.pyplot as plt
def getMat(n,li):
    mat=np.zeros([2**n,2**n])
    for i in range(2**n):
        mat[li[i]][i]=1
    return mat
TRYCNT = 100
swp = []
def Simon(fgate : Qcir.Gate, ggate : Qcir.Gate, n : int):
    # print(type(fgate))
    qb = QuantumRegister(4 * n + 1)
    cb = ClassicalRegister(n, 'c')
    prog = Qcir.QuantumCircuit(qb, cb)
    prog.h(range(n, 2 * n))
    prog.append(fgate, range(n, 3 * n))
    prog.append(ggate, list(range(n, 2 * n)) + list(range(n)))
    # 4 * n -> f>g
    for i in range(n):
        prog.x(i)
        prog.append(stXgate.XGate().control(i + 2), list(range(i + 1)) + [2 * n + i, 4 * n])
        prog.cx(2 * n + i, i)
    for i in range(n):
        prog.cx(2 * n + i, 3 * n + i)
    prog.x(4 * n)
    for i in range(n):
        prog.x(i)
        prog.ccx(i, 4 * n, 3 * n + i)
        prog.x(i)
    for i in range(n - 1, -1, -1):
        prog.cx(2 * n + i, i)
        prog.append(stXgate.XGate().control(i + 2), list(range(i + 1)) + [2 * n + i, 4 * n])
        prog.x(i)
        pass
    prog.append(ggate, list(range(n, 2 * n)) + list(range(n)))
    prog.append(fgate, range(n, 3 * n))
    prog.h(range(n, 2 * n))
    prog.measure(range(n, 2 * n), cb)
    # print(prog)
    # prog.draw('mpl').savefig('inpN.png')
    # prog.draw('mpl').show()
    # plt.pause(-1)
    # print(prog.draw('text'))
    
    job = StatevectorSampler().run([prog], shots = TRYCNT)
    res = job.result()[0].data['c']
    return set(res.get_bitstrings())
def linearBase(res : set, n : int) -> int:
    now = [0] * n
    for x in res:
        s = int(x, 2)
        for i in range(n - 1, -1, -1):
            if (s & (2 ** i)) > 0:
                if now[i] == 0:
                    now[i] = s
                    break
                s ^= now[i]
    num = 0
    for i in range(n):
        if now[i] > 0:
            num = num + 1
    # print("num", num)
    for i in range(n):
        if now[i] > 0:
            print(2**i, now[i])
    if num == n:
        return 0
    if num < n - 1:
        return -1
    ans = 0
    for j in range(n):
        s = 2 ** j
        # print("S=", s)
        for i in range(n - 1, -1, -1):
            if (s & (2 ** i)) > 0:
                if now[i] == 0:
                    break
                s ^= now[i]
                # print("S:", s)
        if s == 0:
            # print("suc", 2**j)
            ans |= 2 ** j
    return 2**n - 1 - ans
def solve(fgate : Qcir.Gate, ggate : Qcir.Gate, n : int) -> int:
    while True:
        res = Simon(fgate, ggate, n)
        print(res)
        ans = linearBase(res, n)
        if ans >= 0:
            return ans
def getGate(mat : np.ndarray, n : int, oswp = [], ineg = [], name  : str = "BF"):
    prog = Qcir.QuantumCircuit(2 * n)
    for i in ineg:
        prog.x(i)
    prog.unitary(mat, range(n))
    for pr in oswp:
        prog.swap(pr[0] + n, n + pr[1])
    for i in range(n):
        prog.cx(i, i + n)
    for pr in oswp:
        prog.swap(pr[0] + n, n + pr[1])
    prog.unitary(mat, range(n)).inverse()
    for i in ineg:
        prog.x(i)
    return prog.to_gate(label = name)
def inputN(n : int, fli : list, gli : list) -> bool:
    for i in range(2 ** n):
        if gli[i] == fli[0]:
            neg = i
            break
    print("neg", f'{neg:0>{n}b}')
    for i in range(2 ** n):
        if gli[i ^ neg] != fli[i]:
            return False
    matf = getMat(n,fli)
    matg = getMat(n,gli)
    # print(np.int64(np.real(matf)))
    # print(np.int64(np.real(matg)))

    fgate = getGate(matf, n, name="F")
    ggate = getGate(matg, n, name="G")

    import time
    nowT = time.time()
    MYans = solve(fgate, ggate, n)
    endT = time.time()
    print("ans", f'{MYans:0>{n}b}')
    print(endT - nowT)
    # input("press any key")

    qf = QuantumRegister(n * 2, "q")
    progf = Qcir.QuantumCircuit(qf)
    progf.append(fgate, qf[:])
    # print(progf)
    progf.draw('mpl').savefig('ansf.png')

    qg = QuantumRegister(n * 2, "q")
    progg = Qcir.QuantumCircuit(qg)
    for i in range(n):
        if MYans & (2 ** i):
            progg.x(i)
    progg.swap(0, 1)
    progg.swap(0, 1)
    progg.append(ggate, qg[:])
    for i in range(n):
        if MYans & (2 ** i):
            progg.x(i)
    progg.swap(0, 1)
    progg.swap(0, 1)
    # print(progg)
    progg.draw('mpl').savefig('ansg.png')
    return True
# n = 3
# neg = np.random.randint(2**n)
# fli = np.random.permutation(range(2**n)).tolist()
# gli = []
# for i in range(2**n):
#     gli.append(fli[i ^ neg])
# print("fli:",fli)
# print("gli:",gli)
# matf = getMat(n,fli)
# matg = getMat(n,gli)
# print(np.int64(np.real(matf)))
# print(np.int64(np.real(matg)))

# fgate = getGate(matf, n, name="F")
# ggate = getGate(matg, n, name="G")

# import time
# nowT = time.time()
# MYans = solve(fgate, ggate, n)
# endT = time.time()
# print("neg", f'{neg:0>{n}b}')
# print("ans", f'{MYans:0>{n}b}')
# print(endT - nowT)
# # input("press any key")

# qf = QuantumRegister(n * 2, "q")
# progf = Qcir.QuantumCircuit(qf)
# progf.append(fgate, qf[:])
# # print(progf)
# progf.draw('mpl').savefig('ansf.png')

# qg = QuantumRegister(n * 2, "q")
# progg = Qcir.QuantumCircuit(qg)
# for i in range(n):
#     if MYans & (2 ** i):
#         progg.x(i)
# progg.append(ggate, qg[:])
# for i in range(n):
#     if MYans & (2 ** i):
#         progg.x(i)
# # print(progg)
# progg.draw('mpl').savefig('ansg.png')
if __name__ == "__main__":
    pass
    # inputN(3, [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7])