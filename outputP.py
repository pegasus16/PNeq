import numpy as np
from collections import Counter
from qiskit import circuit as Qcir
from qiskit import QuantumRegister, ClassicalRegister
from qiskit.primitives import StatevectorSampler
import matplotlib.pyplot as plt
def getMat(n,li):
    mat=np.zeros([2**n,2**n])
    for i in range(2**n):
        mat[li[i]][i]=1
    return mat
TRYCNT = 100
swp = []
# def DJtry(fgate : Qcir.Gate, ggate : Qcir.Gate, n : int, fi : int, gi : int):
#     qb = QuantumRegister(4 * n + 1)
#     cb = ClassicalRegister(n, 'c')
#     prog = Qcir.QuantumCircuit(qb, cb)
#     prog.h(qb[:n])
#     for i in range(n):
#         prog.cx(qb[i], qb[i + 2 * n])
#     prog.append(fgate, qb[: 2 * n])
#     prog.append(ggate, qb[2 * n : 4 * n])
#     prog.cx(qb[fi + n], qb[gi + 3 * n])
#     prog.cx(qb[gi + 3 * n], qb[4 * n])
#     prog.cx(qb[fi + n], qb[gi + 3 * n])
#     prog.append(ggate, qb[2 * n : 4 * n])
#     prog.append(fgate, qb[: 2 * n])
#     for i in range(n - 1, -1, -1):
#         prog.cx(qb[i], qb[i + 2 * n])
#     prog.h(qb[:n])
#     prog.measure(qb[:n], cb)
#     print(prog)
#     job = StatevectorSampler().run([prog], shots = TRYCNT)
#     res = job.result()[0].data['c']
#     return Counter(res.get_bitstrings())
def DJtry(fgate : Qcir.Gate, ggate : Qcir.Gate, n : int, fi : int, gi : int):
    qb = QuantumRegister(3 * n + 1, "q")
    cb = ClassicalRegister(n, 'c')
    prog = Qcir.QuantumCircuit(qb, cb)
    prog.h(range(n, 2 * n))
    prog.x(3 * n)
    prog.h(3 * n)
    prog.append(fgate, range(n, 3 * n))
    prog.append(ggate, list(range(n, 2 * n)) + list(range(n)))
    prog.cx(qb[fi + 2 * n], qb[gi])
    prog.cx(qb[gi], qb[3 * n])
    prog.cx(qb[fi + 2 * n], qb[gi])
    prog.append(ggate, list(range(n, 2 * n)) + list(range(n)))
    prog.append(fgate, range(n, 3 * n))
    prog.h(range(n, 2 * n))
    prog.measure(range(n, 2 * n), cb)
    # if fi == 0 and gi == 0:
    #     print(prog)
    #     prog.draw('mpl').savefig('optP.png')
        # plt.pause(-1)
    # print(prog)
    job = StatevectorSampler().run([prog], shots = 1)
    res = job.result()[0].data['c']
    return res.get_bitstrings()[0]
def solve(fgate : Qcir.Gate, ggate : Qcir.Gate, n : int):
    ans = [-1] * n
    for i in range(n):
        for j in range(n):
            now = DJtry(fgate, ggate, n, i, j)
            # print(i, j, now)
            if now == '0' * n:
                if ans[i] != -1:
                    ans[i] = -2
                else:
                    ans[i] = j
    print(ans)
    return ans
def getGate(mat : np.ndarray, n : int, swp = [], name  : str = "BF"):
    prog = Qcir.QuantumCircuit(2 * n)
    prog.unitary(mat, range(n))
    for pr in swp:
        prog.swap(pr[0] + n, n + pr[1])
    for i in range(n):
        prog.cx(i, i + n)
    for pr in swp:
        prog.swap(pr[0] + n, n + pr[1])
    prog.unitary(mat, range(n)).inverse()
    return prog.to_gate(label = name)
# n = 3
# plist = np.random.permutation(n).tolist()
# print("plist",plist)
# fli = np.random.permutation(range(2**n)).tolist()
# gli = []
# for i in range(2**n):
#     tmpi = fli[i]
#     gli.append(0)
#     for j in range(n):
#         if tmpi%2 == 1:
#             gli[i] += 2**plist[j]
#         tmpi = tmpi//2
# swp = []
# for i in range(n):
#     if plist[i] == i:
#         continue
#     for j in range(i+1,n):
#         if plist[j] != i:
#             continue
#         swp.append([i,j])
#         tmp = plist[j]
#         plist[j] = plist[i]
#         plist[i] = tmp
# print("swp:", swp)
# print("fli:",fli)
# print("gli:",gli)
def outputP(n : int, fli : list, gli : list) -> bool:
    matf = getMat(n,fli)
    matg = getMat(n,gli)
    fgate = getGate(matf, n, name="F")
    ggate = getGate(matg, n, name="G")
    qf = QuantumRegister(n * 2, "q")
    progf = Qcir.QuantumCircuit(qf)
    progf.append(fgate, qf[:])
    progf.draw('mpl').savefig('ansf.png')

    qg = QuantumRegister(n * 2, "q")
    progg = Qcir.QuantumCircuit(qg)
    progg.append(ggate, qg[:])
    progg.draw('mpl').savefig('ansg.png')
    plist = [-1] * n
    flis = [format(fli[i], '03b')[::-1] for i in range(2**n)]
    glis = [format(gli[i], '03b')[::-1] for i in range(2**n)]
    print(flis)
    print(glis)
    for i in range(2 ** n):
        cnt = -1
        for j in range(n):
            if flis[i][j] == '1':
                if cnt != -1:
                    cnt = -1
                    break
                cnt = j
        if cnt == -1:
            continue
        for j in range(n):
            if glis[i][j] == '0':
                continue
            if plist[cnt] == -1:
                plist[cnt] = j
            else:
                return False
    print("plist", plist)
    for i in range(2 ** n):
        for j in range(n):
            if glis[i][plist[j]] != flis[i][j]:
                return False
    print(np.int64(np.real(matf)))
    print(np.int64(np.real(matg)))

    ans = solve(fgate, ggate, n)
    print(ans)
    swp = []
    for i in range(n):
        if ans[i] == i:
            continue
        for j in range(i + 1, n):
            if ans[j] == i:
                swp.append([i, j])
                ans[j] = ans[i]
                ans[i] = i
                break
    print("swap", swp)
    qg = QuantumRegister(n * 2, "q")
    progg = Qcir.QuantumCircuit(qg)
    for i in range(len(swp) - 1, -1, -1):
        progg.swap(swp[i][0] + n, swp[i][1] + n)
    progg.append(ggate, qg[:])
    for i in range(len(swp)):
        progg.swap(swp[i][0] + n, swp[i][1] + n)
    progg.draw('mpl').savefig('ansg.png')
    return True