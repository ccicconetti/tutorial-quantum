#!/usr/bin/env python3

from qiskit.utils import algorithm_globals
from qiskit.algorithms.minimum_eigensolvers import NumPyMinimumEigensolver
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization import QuadraticProgram
from qiskit_aer.primitives import Estimator as AerEstimator
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.circuit.library import TwoLocal
from qiskit.algorithms.optimizers import SPSA
from qiskit_aer.noise import NoiseModel
from qiskit.providers.fake_provider import FakeVigo

import sys

# create a QUBO
qubo = QuadraticProgram(name="QUBO test")
qubo.binary_var("x")
qubo.binary_var("y")
qubo.binary_var("z")
qubo.binary_var("k")
qubo.linear_constraint([1, 0, 0, 1], "<=", 1)
qubo.minimize(
    linear=[-1, -2, 1, -1],
    quadratic={("x", "y"): 1, ("x", "z"): -1, ("y", "z"): 2, ("z", "y"): -1},
)
print(qubo.prettyprint())

conv = QuadraticProgramToQubo()
problem = conv.convert(qubo)

op, offset = problem.to_ising()
print("operator:")
print(op)

print("solve exactly with classical method (press return to continue)")
sys.stdin.read(1)

numpy_solver = NumPyMinimumEigensolver()
result_numpy = numpy_solver.compute_minimum_eigenvalue(operator=op)
print(f"optimum                               : {offset+result_numpy.eigenvalue.real}")
N = problem.get_num_binary_vars()
assert len(result_numpy.eigenstate) == 2**N
res = -1
for i, k in zip(result_numpy.eigenstate, range(len(result_numpy.eigenstate))):
    if i != 0:
        res = k
        break
assert res >= 0
for i in range(N):
    zero_or_one = 0
    if res & (1 << i) != 0:
        zero_or_one = 1
    print(f"{problem.get_variable(i)} == {zero_or_one}")

###
### VQE without noise
###

print("solve with VQE without noise (press return to continue)")
sys.stdin.read(1)

seed = 170
algorithm_globals.random_seed = seed
noiseless_estimator = AerEstimator(
    run_options={"seed": seed, "shots": 1024},
    transpile_options={"seed_transpiler": seed},
)
iterations = 125
ansatz = TwoLocal(rotation_blocks="ry", entanglement_blocks="cz")
spsa = SPSA(maxiter=iterations)
vqe = VQE(noiseless_estimator, ansatz, optimizer=spsa)
result_vqe = vqe.compute_minimum_eigenvalue(operator=op)
print("VQE quantum circuit:")
print(vqe.ansatz.decompose())

print(
    f"VQE on Aer qasm simulator (no noise)  : {result_vqe.eigenvalue.real+offset:.3f}"
)


###
### VQE with noise
###

print("solve with VQE with noise (press return to continue)")
sys.stdin.read(1)

device = FakeVigo()
coupling_map = device.configuration().coupling_map
noise_model = NoiseModel.from_backend(device)

noisy_estimator = AerEstimator(
    backend_options={
        "method": "density_matrix",
        "coupling_map": coupling_map,
        "noise_model": noise_model,
    },
    run_options={"seed": seed, "shots": 1024},
    transpile_options={"seed_transpiler": seed},
)
vqe.estimator = noisy_estimator

result_vqe_noise = vqe.compute_minimum_eigenvalue(operator=op)

print(
    f"VQE on Aer qasm simulator (with noise): {result_vqe_noise.eigenvalue.real+offset:.3f}"
)
