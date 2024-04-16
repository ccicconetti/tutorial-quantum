#!/usr/bin/env python3
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import os

q = QuantumRegister(1)
c = ClassicalRegister(1)
qc = QuantumCircuit(q, c)
qc.measure(q, c)
format = "png" if os.getenv("FORMAT") is None else os.getenv("FORMAT")
qc.draw(output="latex", scale=4, with_layout=False).save(
    f"{__file__.replace('.py','')}.{format}", format=format
)
