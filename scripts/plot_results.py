import csv
from pathlib import Path
import matplotlib.pyplot as plt

def load_rows():
    with open("results/aggregated.csv", "r", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        rows = []
        for r in rd:
            r["n"] = int(r["n"])
            r["med_elapsed_s"] = float(r["med_elapsed_s"])
            r["med_calls"] = float(r["med_calls"])
            rows.append(r)
        return rows

def plot_metric(rows, dens, metric, outname, ylabel, log=True):
    Path("results/figs").mkdir(parents=True, exist_ok=True)
    plt.figure()
    algos = sorted({r["algo"] for r in rows if r["densidade"] == dens})
    for algo in algos:
        xs = [r["n"] for r in rows if r["densidade"] == dens and r["algo"] == algo]
        ys = [r[metric] for r in rows if r["densidade"] == dens and r["algo"] == algo]
        plt.plot(xs, ys, marker="o", label=algo)
    if log:
        plt.yscale("log")
    plt.xlabel("n (vertices)")
    plt.ylabel(ylabel)
    plt.title(f"{ylabel} vs n ({dens})")
    plt.legend()
    plt.savefig(f"results/figs/{outname}", dpi=160, bbox_inches="tight")
    plt.close()

def main():
    rows = load_rows()
    for dens in ["esparso","denso"]:
        plot_metric(rows, dens, "med_elapsed_s", f"tempo_vs_n_{dens}.png", "tempo mediano (s)", log=True)
        plot_metric(rows, dens, "med_calls", f"calls_vs_n_{dens}.png", "calls medianas", log=True)
    print("[OK] Graficos em results/figs/")

if __name__ == "__main__":
    main()
