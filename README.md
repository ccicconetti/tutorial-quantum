# Qiskit scripts

These scripts are used as part of the tutorial _A Practical Introduction to Quantum Computing and Networking_ by [Claudio Cicconetti](https://ccicconetti.github.io/).

## Environment preparation

```
git clone https://github.com/ccicconetti/tutorial-quantum.git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## QUBO

A tiny QUBO script using VQE.

```
python qubo.py
```

Expected output:

```
Problem name: QUBO test

Minimize
  x*y - x*z + y*z - k - x - 2*y + z

Subject to
  No constraints

  Binary variables (4)
    x y z k

operator:
0.5 * IIIZ
+ 0.5 * IIZI
- 0.5 * IZII
+ 0.5 * ZIII
+ 0.25 * IIZZ
- 0.25 * IZIZ
+ 0.25 * IZZI
VQE quantum circuit:
     ┌──────────┐            ┌──────────┐                                 »
q_0: ┤ Ry(θ[0]) ├─■──■─────■─┤ Ry(θ[4]) ├─────────────────■───────■─────■─»
     ├──────────┤ │  │     │ └──────────┘┌──────────┐     │       │     │ »
q_1: ┤ Ry(θ[1]) ├─■──┼──■──┼──────■──────┤ Ry(θ[5]) ├─────■───────┼──■──┼─»
     ├──────────┤    │  │  │      │      └──────────┘┌──────────┐ │  │  │ »
q_2: ┤ Ry(θ[2]) ├────■──■──┼──────┼───────────■──────┤ Ry(θ[6]) ├─■──■──┼─»
     ├──────────┤          │      │           │      ├──────────┤       │ »
q_3: ┤ Ry(θ[3]) ├──────────■──────■───────────■──────┤ Ry(θ[7]) ├───────■─»
     └──────────┘                                    └──────────┘         »
«     ┌──────────┐                                  ┌───────────┐             »
«q_0: ┤ Ry(θ[8]) ├──────────────────■───────■─────■─┤ Ry(θ[12]) ├─────────────»
«     └──────────┘┌──────────┐      │       │     │ └───────────┘┌───────────┐»
«q_1: ─────■──────┤ Ry(θ[9]) ├──────■───────┼──■──┼───────■──────┤ Ry(θ[13]) ├»
«          │      └──────────┘┌───────────┐ │  │  │       │      └───────────┘»
«q_2: ─────┼───────────■──────┤ Ry(θ[10]) ├─■──■──┼───────┼────────────■──────»
«          │           │      ├───────────┤       │       │            │      »
«q_3: ─────■───────────■──────┤ Ry(θ[11]) ├───────■───────■────────────■──────»
«                             └───────────┘                                   »
«                  
«q_0: ─────────────
«                  
«q_1: ─────────────
«     ┌───────────┐
«q_2: ┤ Ry(θ[14]) ├
«     ├───────────┤
«q_3: ┤ Ry(θ[15]) ├
«     └───────────┘
x (binary) == 0
y (binary) == 1
z (binary) == 0
k (binary) == 1
optimum                               : -3.0
VQE on Aer qasm simulator (no noise)  : -2.998
VQE on Aer qasm simulator (with noise): -2.398
```

## Version used

| Package              | Version |
| -------------------- | ------- |
| qiskit               | 0.43.0  |
| qiskit-aer           | 0.12.0  |
| qiskit-ibmq-provider | 0.20.2  |
| qiskit-optimization  | 0.5.0   |
| qiskit-terra         | 0.24.0  |
