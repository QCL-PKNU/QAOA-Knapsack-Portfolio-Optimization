from functools import partial

import numpy as np
from qiskit import transpile

import knapsack
import circuits

from qiskit import Aer, IBMQ
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from scipy.optimize import shgo

backend = Aer.get_backend("aer_simulator_statevector")
provider = IBMQ.load_account()
bk = provider.get_backend("ibm_cairo")
noise_model = NoiseModel.from_backend(bk)
simulator = QasmSimulator(noise_model=noise_model)


is_apply_noise = True


def get_statevector(transpiled_circuit, parameter_dict):
    bound_circuit = transpiled_circuit.bind_parameters(parameter_dict)
    if is_apply_noise:
        result = simulator.run(bound_circuit, shots=1).result()
    else:
        result = backend.run(bound_circuit, shots=1).result()
    statevector = result.get_statevector()
    return statevector


def average_value(probs_dict, func):
    """Calculate the average value of a function over a probability dict."""
    bitstrings = list(probs_dict.keys())
    values = np.array(list(map(func, bitstrings)))
    probs = np.array(list(probs_dict.values()))
    return sum(values * probs)


def optimize_angles(p, angles_to_value, gamma_range, beta_range):
    """Optimize the parameters beta, gamma for a given function angles_to_value"""
    bounds = np.array([gamma_range, beta_range] * p)
    result = shgo(angles_to_value, bounds, iters=3)
    return result.x


def bitstring_to_choice(bitstring, problem):
    """Convert a qiskit bitstring to a choice numpy array."""
    bits = np.array(list(map(int, list(bitstring))))[::-1]
    choice = np.array(bits[:problem.N])
    return choice


def objective_function(bitstring, problem):
    """The objective function of the quantum walk mixer based approach."""
    choice = bitstring_to_choice(bitstring, problem)
    value = choice.dot(problem.values)
    return value


def to_parameter_dict(angles, circuit):
    """Create a circuit specific parameter dict from given parameters.
    
    angles = np.array([gamma0, beta0, gamma1, beta1, ...])"""
    gammas = angles[0::2]
    betas = angles[1::2]
    parameters = {}
    for parameter, value in zip(circuit.betas, betas):
        parameters[parameter] = value
    for parameter, value in zip(circuit.gammas, gammas):
        parameters[parameter] = value
    return parameters


def get_probs_dict(circuit, problem, angles, choices_only=True):
    """Simulate circuit for given parameters and return probability dict."""
    transpiled_circuit = transpile(circuit, backend)
    parameter_dict = to_parameter_dict(angles, circuit)
    statevector = get_statevector(transpiled_circuit, parameter_dict)
    if choices_only:
        probs_dict = statevector.probabilities_dict(range(problem.N))
    else:
        probs_dict = statevector.probabilities_dict()
    return probs_dict


def get_expectation_value(circuit, problem, angles):
    """Return the expectation value of the objective function for given parameters."""
    probs_dict = get_probs_dict(circuit, angles)
    obj = partial(objective_function, problem=problem)
    return average_value(probs_dict, obj)


def find_optimal_angles(circuit, problem):
    """Optimize the parameters beta, gamma for given circuit and parameters."""
    transpiled_circuit = transpile(circuit, backend)
    obj = partial(objective_function, problem=problem)
    angles_to_parameters = partial(to_parameter_dict, circuit=circuit)

    def angles_to_value(angles):
        parameter_dict = angles_to_parameters(angles)
        statevector = get_statevector(transpiled_circuit, parameter_dict)
        probs_dict = statevector.probabilities_dict()
        value = - average_value(probs_dict, obj)
        return value

    return optimize_angles(circuit.p, angles_to_value,
                                        circuit.gamma_range(),
                                        circuit.beta_range())


def comparable_objective_function(bitstring, problem):
    """An approach independent objective function"""
    choice = bitstring_to_choice(bitstring, problem)
    if knapsack.is_choice_feasible(choice, problem):
        return knapsack.value(choice, problem)
    return 0


def comparable_expectation_value(problem, probs):
    """Calculate the expectation value of the approach independent objective function for given parameters."""
    obj = partial(comparable_objective_function, problem=problem)
    expectation = average_value(probs, obj)
    return expectation


def approximation_ratio(problem, probs):
    """Calculate the approximation ratio of the qwqaoa approach for given problem and parameters."""
    expectation = comparable_expectation_value(problem, probs)
    best_known_solutions = knapsack.classical_solutions(problem)
    choice = best_known_solutions[0]
    best_value = knapsack.value(choice, problem)
    ratio = expectation / best_value
    return ratio
