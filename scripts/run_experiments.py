import csv
import glob
import subprocess
from pathlib import Path

TIME_LIMIT = 2.0

def run(inst_path, algo, restarts=2000, seed=42):
    cmd = [
        "python",
        "codigo/hamiltonian.py",
        inst_path,
        "--algo", algo,
        "--stats",
        "--timelimit", str(TIME_LIMIT),
    ]
    if algo == "rnd":
        cmd += ["--restarts", str(restarts), "--seed", str(seed)]
    out = subprocess.check_output(cmd, text=True).strip().splitlines()
    ans = out[0].strip()

    stats_line = out[1].strip() if len(out) > 1 else ""
    d = {}
    for token in stats_line.split():
        if "=" in token:
            k, v = token.split("=")
            d[k] = v.replace("s", "")

    return ans, int(d.get("calls", "0")), int(d.get("backtracks", "0")), int(d.get("prunes", "0")), float(d.get("elapsed", "0"))

def main():
    Path("results").mkdir(exist_ok=True)

    with open("results/raw.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["arquivo","n","densidade","algo","ans","calls","backtracks","prunes","elapsed_s"])

        for inst in sorted(glob.glob("instances/auto/g_*.txt")):
            name = Path(inst).stem  # g_n30_denso_2
            parts = name.split("_")
            n = int(parts[1][1:])   # n30 -> 30
            dens = parts[2]         # esparso|denso

            # Exatos até 22 (por custo exponencial); grandes via heurística.
            algos = ["bt", "bnb"] if n <= 22 else ["rnd"]
            for algo in algos:
                ans, calls, backs, prunes, elapsed = run(inst, algo)
                w.writerow([inst, n, dens, algo, ans, calls, backs, prunes, f"{elapsed:.6f}"])

    print("[OK] results/raw.csv gerado")

if __name__ == "__main__":
    main()
