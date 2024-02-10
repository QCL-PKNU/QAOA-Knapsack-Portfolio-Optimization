from qaoa import QuantumWalkQAOA
from plots import hist
import matplotlib.pyplot as plt

import os
import knapsack
import mv
import utils
import datetime


def main():
    p = 1
    m = 5

    # Apple and Microsoft
    er = [0.185895, 0.194126, 0.177782, 0.182612, 0.283484]

    budget = len(er) // 2
    prices = [1] * len(er)
    problem = knapsack.KnapsackProblem(er, prices, budget)

    bks = knapsack.classical_solutions(problem)

    for p in range(1, 6):
        utils.is_apply_noise = False

        print(f"Problem: {problem}")
        print("Building Circuit...")
        circuit = QuantumWalkQAOA(problem, p=p, m=m)
        print("Done!")
        print("Optimizing Angles...")
        angles = utils.find_optimal_angles(circuit, problem)
        print("Done!")
        print(f"Optimized Angles: {angles}")
        probs = utils.get_probs_dict(circuit, problem, angles)
        print(f"Probabilities of Bitstrings: {probs}")
        ratio = utils.approximation_ratio(problem, probs)
        print(f"Approximation Ratio: {ratio}")

        os.makedirs("plots", exist_ok=True)
        folder = os.path.join(
            "plots",
            f"{p}_{m}_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}_NOISELESS",
        )
        os.makedirs(folder, exist_ok=True)
        fig, ax = plt.subplots()
        fig.set_size_inches(18, 10)
        hist(ax, probs, folder=f"{folder}")

        comments = [
            f"Considered {problem}",
            f"QAOA circuit with {p = } and {m = }",
            f"Optimized angles: {angles}",
            f"Resulting Probabilities: {probs}",
            f"Best known solutions: {bks}",
            f"Approximation Ratio: {ratio}",
            f"Higher the probability: {max(probs.values())} at reversed key: {max(probs, key=probs.get)[::-1]}",
            f"Higher the probability: {max(probs.values())} at key: {max(probs, key=probs.get)}",
        ]

        file_name = f"result.txt"
        with open(os.path.join(f"{folder}", file_name), "w") as f:
            f.write("\n".join(comments))

        # utils.is_apply_noise = True

        # print(f"Problem: {problem}")
        # print("Building Circuit...")
        # circuit = QuantumWalkQAOA(problem, p=p, m=3)
        # print("Done!")
        # print("Optimizing Angles...")
        # angles = utils.find_optimal_angles(circuit, problem)
        # print("Done!")
        # print(f"Optimized Angles: {angles}")
        # probs = utils.get_probs_dict(circuit, problem, angles)
        # print(f"Probabilities of Bitstrings: {probs}")
        # ratio = utils.approximation_ratio(problem, probs)
        # print(f"Approximation Ratio: {ratio}")

        # os.makedirs("plots", exist_ok=True)
        # folder = os.path.join("plots", f"{p}_{m}_{datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}_NOISE")
        # os.makedirs(folder, exist_ok=True)
        # fig, ax = plt.subplots()
        # fig.set_size_inches(18, 10)
        # hist(ax, probs, folder=f"{folder}")

        # comments = [
        #     f"Considered {problem}",
        #     f"QAOA circuit with {p = } and {m = }",
        #     f"Optimized angles: {angles}",
        #     f"Resulting Probabilities: {probs}",
        #     f"Best known solutions: {bks}",
        #     f"Approximation Ratio: {ratio}",
        #     f"Higher the probability: {max(probs.values())} at reversed key: {max(probs, key=probs.get)[::-1]}",
        #     f"Higher the probability: {max(probs.values())} at key: {max(probs, key=probs.get)}"
        # ]

        # file_name = f"result.txt"
        # with open(os.path.join(f"{folder}", file_name), "w") as f:
        #     f.write("\n".join(comments))


if __name__ == "__main__":
    main()
