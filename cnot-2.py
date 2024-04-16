#!/usr/bin/env python3

from qiskit import QuantumRegister, QuantumCircuit, Aer, execute


def cnot_table(control: int, target: int):
    assert control in [0, 1]
    assert target in [0, 1]
    q = QuantumRegister(2)
    qc = QuantumCircuit(q)
    if control == 1:
        qc.x(q[0])
    if target == 1:
        qc.x(q[1])
    qc.barrier()
    qc.h(q)
    qc.cnot(q[0], q[1])
    qc.h(q)
    print(qc.draw(output="text"))

    simulator = Aer.get_backend("statevector_simulator")
    job = execute(qc, simulator)
    result = job.result()
    statevector = result.get_statevector(qc)
    assert len(statevector.to_dict(5)) == 1
    return next(iter(statevector.to_dict(5).keys()))[::-1]


out = []
for control in [0, 1]:
    for target in [0, 1]:
        out.append(f"{control}{target} -> {cnot_table(control, target)}")

print("truth table:")
print("\n".join(out))
