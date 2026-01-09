import csv
from collections import defaultdict
from statistics import median
from pathlib import Path

def main():
    Path("results").mkdir(exist_ok=True)

    with open("results/raw.csv", "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    grp = defaultdict(list)
    for r in rows:
        key = (int(r["n"]), r["densidade"], r["algo"])
        grp[key].append(r)

    with open("results/aggregated.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n","densidade","algo","med_elapsed_s","med_calls","med_backtracks","med_prunes","taxa_sim","execucoes"])

        for (n, dens, algo), lst in sorted(grp.items()):
            med_elapsed = median(float(x["elapsed_s"]) for x in lst)
            med_calls = median(int(x["calls"]) for x in lst)
            med_back = median(int(x["backtracks"]) for x in lst)
            med_pru = median(int(x["prunes"]) for x in lst)
            taxa_sim = sum(1 for x in lst if x["ans"] == "SIM") / len(lst)

            w.writerow([n, dens, algo, f"{med_elapsed:.6f}", med_calls, med_back, med_pru, f"{taxa_sim:.2f}", len(lst)])

    print("[OK] results/aggregated.csv gerado")

if __name__ == "__main__":
    main()
