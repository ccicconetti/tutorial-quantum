#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.tools.visualization import plot_histogram

# Import from Qiskit Aer noise module
from qiskit_aer.noise import (
    NoiseModel,
    pauli_error,
    depolarizing_error,
    thermal_relaxation_error,
)


def run_sim_noise(depth: int):
    circ = QuantumCircuit(1)
    for _ in range(depth):
        circ.x(0)
        circ.barrier()
    circ.measure_all()

    noise_model = NoiseModel()
    p_gate1 = 0.05
    error_gate1 = pauli_error([("X", p_gate1), ("I", 1 - p_gate1)])
    noise_model.add_all_qubit_quantum_error(error_gate1, ["x"])

    sim_noise = AerSimulator(noise_model=noise_model)

    # Transpile circuit for noisy basis gates
    circ_tnoise = transpile(circ, sim_noise)

    # Run and get counts
    result_bit_flip = sim_noise.run(circ_tnoise).result()
    counts_bit_flip = result_bit_flip.get_counts(0)

    # Plot noisy output
    if "1" in counts_bit_flip:
        return counts_bit_flip["0"] / (counts_bit_flip["0"] + counts_bit_flip["1"])
    return 1


xdata = []
ydata = []
for depth in range(0, 51, 2):
    xdata.append(depth)
    ydata.append(run_sim_noise(depth))
    print(f"depth {depth}: {ydata[-1]:.2f}")

if os.getenv("PLT") is not None:
    fig, ax = plt.subplots()
    ax.plot(xdata, ydata)
    ax.set(xlabel="Circuit depth", ylabel="Fraction of good experiments")
    ax.grid()
    plt.show()
