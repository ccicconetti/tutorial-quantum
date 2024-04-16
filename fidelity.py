#!/usr/bin/env python3

from qiskit import QuantumRegister, QuantumCircuit, Aer, execute
from qiskit.quantum_info.states import state_fidelity
import matplotlib.pyplot as plt
import os
from math import pi


def bell_state(simulator, phase: int):
    q = QuantumRegister(2)
    qc = QuantumCircuit(q)
    qc.rx(phase * 2 * pi / 360, q[0])
    qc.h(q[0])
    qc.cnot(q[0], q[1])
    # print(qc.draw(output="text"))
    return execute(qc, simulator).result().get_statevector(qc)


simulator = Aer.get_backend("statevector_simulator")

reference = bell_state(simulator, 0)
xdata = []
ydata = []
for phase in range(0, 361, 20):
    xdata.append(phase)
    ydata.append(state_fidelity(reference, bell_state(simulator, phase)))
    print(f"{phase} {ydata[-1]:.2f}")

if os.getenv("PLT") is not None:
    fig, ax = plt.subplots()
    ax.plot(xdata, ydata)
    ax.set(xlabel="Rx theta [degrees]", ylabel="Fidelity")
    ax.grid()
    plt.show()
