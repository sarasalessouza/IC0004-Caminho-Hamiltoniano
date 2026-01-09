import random
from pathlib import Path

# Geração de instâncias ER G(n,p) (esparso/denso) com conectividade forçada.
# Saída: instances/auto/g_n{n}_{dens}_{k}.txt no formato:
#   n m
#   u v
#   ...

SIZES = [10, 20, 30, 40, 50]
K = 5
SEED = 12345

def er_edges(n, p, rng):
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                edges.append((u, v))
    return edges

def ensure_connected(n, edges, rng):
    # Conecta componentes ligando um vértice de cada componente ao vértice 0.
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    seen = [False] * n
    stack = [0]
    seen[0] = True
    while stack:
        v = stack.pop()
        for u in adj[v]:
            if not seen[u]:
                seen[u] = True
                stack.append(u)

    if all(seen):
        return edges

    new_edges = set(edges)
    for v in range(n):
        if not seen[v]:
            a, b = (0, v) if 0 < v else (v, 0)
            new_edges.add((min(a, b), max(a, b)))
    return sorted(new_edges)

def write_instance(path, n, edges):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{n} {len(edges)}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")

def main():
    out = Path("instances/auto")
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)

    for n in SIZES:
        for dens in ["esparso", "denso"]:
            p = (2.0 / n) if dens == "esparso" else 0.35
            for k in range(K):
                seed = rng.randrange(10**9)
                r2 = random.Random(seed)
                edges = er_edges(n, p, r2)
                edges = ensure_connected(n, edges, r2)
                write_instance(out / f"g_n{n}_{dens}_{k}.txt", n, edges)

    print("[OK] Instancias geradas em instances/auto")

if __name__ == "__main__":
    main()
