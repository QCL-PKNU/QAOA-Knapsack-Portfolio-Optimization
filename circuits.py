from functools import partial
from itertools import product
from fractions import Fraction
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, transpile, execute
from qiskit.circuit import Parameter
import numpy as np
import math

from knapsack import KnapsackProblem


class QFT(QuantumCircuit):
    """Compute the quantum fourier transform up to ordering of qubits."""
    def __init__(self, register):
        """Initialize the Circuit."""
        super().__init__(register, name="QFT")
        for idx, qubit in reversed(list(enumerate(register))):
            super().h(qubit)
            for c_idx, control_qubit in reversed(list(enumerate(register[:idx]))):
                k = idx - c_idx + 1
                super().cp(2 * np.pi / 2**k, qubit, control_qubit)


class Add(QuantumCircuit):
    """Circuit for adding n to intermediate state."""
    def __init__(self, register, n, control=None):
        """Initialize the Circuit."""
        self.register = register
        self.control = control
        qubits = [*register, *control] if control is not None else register
        super().__init__(qubits, name=f"Add {n}")
        binary = list(map(int, reversed(bin(n)[2:])))
        for idx, value in enumerate(binary):
            if value:
                self._add_power_of_two(idx)

    def _add_power_of_two(self, k):
        """Circuit for adding 2^k to intermediate state."""
        phase_gate = super().p
        if self.control is not None:
            phase_gate = partial(super().cp, target_qubit=self.control)
        for idx, qubit in enumerate(self.register):
            l = idx + 1
            if l > k:
                m = l - k
                phase_gate(2 * np.pi / 2**m, qubit)


class FeasibilityOracle(QuantumCircuit):
    """Circuit for checking feasibility of a choice."""

    def __init__(self, choice_reg, weight_reg, flag_qubit, problem,
                 clean_up=True):
        """Initialize the circuit."""
        c = math.floor(math.log2(problem.max_weight)) + 1
        w0 = 2**c - problem.max_weight - 1

        subcirc = QuantumCircuit(choice_reg, weight_reg, name="")
        qft = QFT(weight_reg)
        subcirc.append(qft.to_instruction(), weight_reg)
        for qubit, weight in zip(choice_reg, problem.weights):
            adder = Add(weight_reg, weight, control=[qubit]).to_instruction()
            subcirc.append(adder, [*weight_reg, qubit])
        adder = Add(weight_reg, w0)
        subcirc.append(adder.to_instruction(), weight_reg)
        subcirc.append(qft.inverse().to_instruction(), weight_reg)

        super().__init__(choice_reg, weight_reg, flag_qubit, name="U_v")
        super().append(subcirc.to_instruction(),
                       [*choice_reg, *weight_reg])
        super().x(weight_reg[c:])
        super().mcx(weight_reg[c:], flag_qubit)
        super().x(weight_reg[c:])
        if clean_up:
            super().append(subcirc.inverse().to_instruction(),
                           [*choice_reg, *weight_reg])


class SingleQubitQuantumWalk(QuantumCircuit):
    """Circuit for single qubit quantum walk mixing."""
    def __init__(self, choice_reg, weight_reg, flag_regs,
                 problem: KnapsackProblem, j: int):
        """Initialize the circuit."""
        flag_x, flag_neighbor, flag_both = flag_regs

        self.beta = Parameter("beta")

        super().__init__(choice_reg, weight_reg, *flag_regs,
                         name=f"SingleQubitQuantumWalk_{j=}")

        feasibility_oracle = FeasibilityOracle(choice_reg, weight_reg, flag_x,
                                               problem)

        # compute flag qubits
        super().append(feasibility_oracle.to_instruction(),
                       [*choice_reg, *weight_reg, flag_x])
        super().x(choice_reg[j])
        super().append(feasibility_oracle.to_instruction(),
                       [*choice_reg, *weight_reg, flag_neighbor])
        super().x(choice_reg[j])
        super().ccx(flag_x, flag_neighbor, flag_both)
        # mix with j-th neighbor
        super().crx(2 * self.beta, flag_both, choice_reg[j])
        # uncompute flag qubits
        super().ccx(flag_x, flag_neighbor, flag_both)
        super().x(choice_reg[j])
        super().append(feasibility_oracle.to_instruction(),
                       [*choice_reg, *weight_reg, flag_neighbor])
        super().x(choice_reg[j])
        super().append(feasibility_oracle.to_instruction(),
                       [*choice_reg, *weight_reg, flag_x])


class FeasibilityOracle(QuantumCircuit):
    """Circuit for checking feasibility of a choice."""
    def __init__(self, choice_reg, weight_reg, flag_qubit, problem,
                 clean_up=True):
        """Initialize the circuit."""
        c = math.floor(math.log2(problem.max_weight)) + 1
        w0 = 2**c - problem.max_weight - 1

        subcirc = QuantumCircuit(choice_reg, weight_reg, name="")
        qft = QFT(weight_reg)
        subcirc.append(qft.to_instruction(), weight_reg)
        for qubit, weight in zip(choice_reg, problem.weights):
            adder = Add(weight_reg, weight, control=[qubit]).to_instruction()
            subcirc.append(adder, [*weight_reg, qubit])
        adder = Add(weight_reg, w0)
        subcirc.append(adder.to_instruction(), weight_reg)
        subcirc.append(qft.inverse().to_instruction(), weight_reg)

        super().__init__(choice_reg, weight_reg, flag_qubit, name="U_v")
        super().append(subcirc.to_instruction(),
                       [*choice_reg, *weight_reg])
        super().x(weight_reg[c:])
        super().mcx(weight_reg[c:], flag_qubit)
        super().x(weight_reg[c:])
        if clean_up:
            super().append(subcirc.inverse().to_instruction(),
                           [*choice_reg, *weight_reg])


class QuantumWalkMixer(QuantumCircuit):
    """Mixing circuit for Knapsack QAOA with hard constraints."""
    def __init__(self, choice_reg, weight_reg, flag_regs,
                 problem: KnapsackProblem, m: int):
        """Initialize the circuit."""
        flag_x, flag_neighbor, flag_both = flag_regs

        self.beta = Parameter("beta")

        super().__init__(choice_reg, weight_reg, *flag_regs,
                         name=f"QuantumWalkMixer_{m=}")
        for __ in range(m):
            for j in range(problem.N):
                jwalk = SingleQubitQuantumWalk(choice_reg, weight_reg,
                                               flag_regs, problem, j)
                super().append(jwalk.to_instruction({jwalk.beta: self.beta / m}),
                               [*choice_reg, *weight_reg, *flag_regs])


class DephaseValue(QuantumCircuit):
    """Dephase Value of an item choice."""

    def __init__(self, choice_reg, problem):
        """Initialize the circuit."""
        self.gamma = Parameter("gamma")
        super().__init__(choice_reg, name="Dephase Value")
        for qubit, value in zip(choice_reg, problem.values):
            super().p(- self.gamma * value, qubit)