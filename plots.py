import matplotlib.pyplot as plt
import numpy as np


plt.rcParams.update({
    "figure.autolayout": True,
    "text.usetex": True,
    "font.family": "serif",
    "font.size": "16",
})


def key_to_label(key):
    digits = list(reversed(list(key)))
    label = "(" + ", ".join(digits) + ")"
    return label


def hist(ax, probs, folder="plots"):
    x = list(range(len(probs.keys())))
    heights = np.array(list(probs.values()))
    keys = list(probs.keys())
    labels = list(map(key_to_label, keys))

    ax.bar(x, heights, tick_label=labels)
    ax.tick_params(axis='x', rotation=90)
    ax.set_xlabel(r"Item choice $x$")
    ax.set_ylabel(r"Probability $p(x)$")

    plt.savefig(f"{folder}/hist.png")