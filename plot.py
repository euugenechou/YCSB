#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os

def load_output_path(prefix):
    return f"{prefix}.load_results"

def run_output_path(prefix):
    return f"{prefix}.run_results"

def aggregate(prefixes):
    results = {}

    for prefix in prefixes:
        with open(load_output_path(prefix), "r") as f:
            load_throughput = float(f.readlines()[1].split(",")[-1].strip())

        with open(run_output_path(prefix), "r") as f:
            run_throughput = float(f.readlines()[1].split(",")[-1].strip())

        results[prefix] = [load_throughput, run_throughput]

    return results

def grouped_bar_chart(title, ylabel, xlabel, labels, keys, stats):
    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    width = 0.15

    for i, statlist in enumerate(stats):
        name = keys[i].split('/')[-1]
        offset = width * (2 * i - (len(stats) - 1)) / 2
        ax.bar(x + offset, statlist, width, label=name)

    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(color="lightgray", linestyle="dotted", linewidth=1, axis="y")
    ax.tick_params(length=0)
    ax.set_axisbelow(True)
    ax.set_ylabel(ylabel, fontweight="bold", labelpad=10)
    ax.set_xlabel(xlabel, fontweight="bold", labelpad=10)
    ax.set_title(title, fontweight="bold", pad=5)
    ax.set_xticks(x, labels)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.29), ncol=5)

    fig.set_size_inches(10, 6)

    return fig

def plot(prefixes, output):
    results = aggregate(prefixes)

    plot = grouped_bar_chart(
        "Throughput of Loading and Running",
        "Throughput (ops/sec)",
        "Phase",
        ["Loading", "Running"],
        [os.path.basename(prefix) for prefix in prefixes],
        [results[prefix] for prefix in prefixes],
    )

    plot.savefig(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output",
        default="plot.pdf",
        help="path to save plot to"
    )
    parser.add_argument(
        "prefixes",
        nargs="+",
        help="prefixes of results to plot"
    )
    args = parser.parse_args()

    plot(args.prefixes, args.output)

if __name__ == "__main__":
    main()
