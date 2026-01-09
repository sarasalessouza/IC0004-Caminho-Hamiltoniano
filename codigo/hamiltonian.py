#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IC0004 - Caminho Hamiltoniano (decisão)

Entrada (arquivo):
  primeira linha: n m
  m linhas: u v     (arestas não direcionadas, 0 <= u,v < n)

Saída:
  SIM  se existe caminho hamiltoniano
  NAO  caso contrário (ou timeout)

Algoritmos:
  --algo bt   : Backtracking (exato)
  --algo bnb  : Branch-and-Bound (exato, com podas)
  --algo rnd  : Heurística (não garantida), para n grandes

Opções:
  --stats            : imprime métricas (calls/backtracks/prunes/elapsed)
  --timelimit <seg>  : limite de tempo por execução (default: 2.0s)
  --restarts <k>     : (apenas rnd) número de reinícios (default: 2000)
  --seed <s>         : (apenas rnd) semente (default: 42)
"""

from __future__ import annotations
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional


# -----------------------------
# Estruturas auxiliares
# -----------------------------
@dataclass
class Stats:
    calls: int = 0
    backtracks: int = 0
    prunes: int = 0
    start: float = 0.0
    elapsed: float = 0.0


def now() -> float:
    return time.perf_counter()


def timed_out(stats: Stats, time_limit: Optional[float]) -> bool:
    return time_limit is not None and (now() - stats.start) > time_limit


# -----------------------------
# Leitura do grafo
# -----------------------------
def read_graph(path: str) -> List[List[int]]:
    with open(path, "r", encoding="utf-8") as f:
        first = f.readline().strip().split()
        if len(first) < 2:
            raise ValueError("Formato inválido: primeira linha deve conter n m")
        n, m = map(int, first[:2])

        adj = [set() for _ in range(n)]
        for _ in range(m):
            line = f.readline()
            if not line:
                break
            u, v = map(int, line.strip().split())
            if u == v:
                continue
            if 0 <= u < n and 0 <= v < n:
                adj[u].add(v)
                adj[v].add(u)

    return [sorted(list(s)) for s in adj]


# -----------------------------
# Podas e heurísticas
# -----------------------------
def order_neighbors(adj: List[List[int]], visited: List[bool], v: int) -> List[int]:
    """
    Heurística: visita primeiro vizinhos "mais restritos"
    (menor grau residual = menos opções futuras)
    """
    cand = [u for u in adj[v] if not visited[u]]

    def residual_degree(u: int) -> int:
        return sum(1 for w in adj[u] if not visited[w])

    cand.sort(key=residual_degree)
    return cand


def subgraph_connected(adj: List[List[int]], allowed: List[bool], start: int) -> bool:
    """
    Verifica conectividade do subgrafo induzido por allowed=True.
    """
    n = len(adj)
    # acha um start permitido
    if start < 0 or start >= n or not allowed[start]:
        start = -1
        for i in range(n):
            if allowed[i]:
                start = i
                break
        if start == -1:
            return True  # vazio é "conexo"

    stack = [start]
    seen = [False] * n
    seen[start] = True
    count = 1

    while stack:
        v = stack.pop()
        for u in adj[v]:
            if allowed[u] and not seen[u]:
                seen[u] = True
                count += 1
                stack.append(u)

    total = sum(1 for x in allowed if x)
    return count == total


def residual_degree_in_allowed(adj: List[List[int]], allowed: List[bool], v: int) -> int:
    return sum(1 for u in adj[v] if allowed[u])


# -----------------------------
# Backtracking (exato)
# -----------------------------
def hamilton_bt(adj: List[List[int]], time_limit: Optional[float]) -> Tuple[bool, Stats]:
    n = len(adj)
    st = Stats(start=now())

    # poda trivial: se n>1 e existe vértice isolado, impossível
    if n > 1 and any(len(adj[v]) == 0 for v in range(n)):
        st.elapsed = now() - st.start
        return False, st

    visited = [False] * n

    def dfs(pos: int, v: int) -> bool:
        st.calls += 1
        if timed_out(st, time_limit):
            raise TimeoutError

        if pos == n:
            return True

        for u in order_neighbors(adj, visited, v):
            visited[u] = True
            if dfs(pos + 1, u):
                return True
            visited[u] = False
            st.backtracks += 1
        return False

    # tenta todos os vértices como início
    for s in range(n):
        visited[s] = True
        try:
            if dfs(1, s):
                st.elapsed = now() - st.start
                return True, st
        except TimeoutError:
            st.elapsed = now() - st.start
            return False, st
        visited[s] = False

    st.elapsed = now() - st.start
    return False, st


# -----------------------------
# Branch-and-Bound (exato)
# -----------------------------
def hamilton_bnb(adj: List[List[int]], time_limit: Optional[float]) -> Tuple[bool, Stats]:
    n = len(adj)
    st = Stats(start=now())

    if n > 1 and any(len(adj[v]) == 0 for v in range(n)):
        st.elapsed = now() - st.start
        return False, st

    visited = [False] * n
    path = [-1] * n

    # inicia por vértices de maior grau (mais promissores)
    starts = list(range(n))
    starts.sort(key=lambda v: len(adj[v]), reverse=True)

    def should_prune(current_last: int) -> bool:
        """
        Podas:
        1) Se existe vértice não visitado com grau residual 0 no subgrafo restante -> impossível
        2) Se o subgrafo (não visitados + last) não é conexo -> impossível completar
        """
        allowed_remaining = [not visited[i] for i in range(n)]
        remaining = sum(1 for x in allowed_remaining if x)
        if remaining <= 1:
            return False

        # Poda por grau residual 0
        for i in range(n):
            if allowed_remaining[i] and residual_degree_in_allowed(adj, allowed_remaining, i) == 0:
                return True

        # Poda por conectividade: inclui o vértice atual (last) no conjunto permitido
        allowed2 = allowed_remaining[:]
        allowed2[current_last] = True
        if not subgraph_connected(adj, allowed2, current_last):
            return True

        return False

    def dfs(pos: int, v: int) -> bool:
        st.calls += 1
        if timed_out(st, time_limit):
            raise TimeoutError

        if pos == n:
            return True

        if should_prune(v):
            st.prunes += 1
            return False

        for u in order_neighbors(adj, visited, v):
            visited[u] = True
            path[pos] = u
            if dfs(pos + 1, u):
                return True
            visited[u] = False
            st.backtracks += 1
        return False

    for s in starts:
        visited[s] = True
        path[0] = s
        try:
            if dfs(1, s):
                st.elapsed = now() - st.start
                return True, st
        except TimeoutError:
            st.elapsed = now() - st.start
            return False, st
        visited[s] = False

    st.elapsed = now() - st.start
    return False, st


# -----------------------------
# Heurística (não garantida): random-restart greedy
# -----------------------------
def hamilton_rnd(adj: List[List[int]], time_limit: Optional[float], restarts: int, seed: int) -> Tuple[bool, Stats]:
    import random
    n = len(adj)
    st = Stats(start=now())
    rng = random.Random(seed)

    # ordem inicial: tenta começar por maior grau
    starts = list(range(n))
    starts.sort(key=lambda v: len(adj[v]), reverse=True)

    def greedy_from(start: int) -> bool:
        visited = [False] * n
        visited[start] = True
        v = start

        for _ in range(n - 1):
            st.calls += 1
            if timed_out(st, time_limit):
                raise TimeoutError

            cand = [u for u in adj[v] if not visited[u]]
            if not cand:
                return False

            # desempate aleatório + menor grau residual
            rng.shuffle(cand)
            cand.sort(key=lambda u: sum(1 for w in adj[u] if not visited[w]))
            u = cand[0]
            visited[u] = True
            v = u

        return True

    for r in range(restarts):
        if timed_out(st, time_limit):
            st.elapsed = now() - st.start
            return False, st

        start = starts[r % n]  # alterna inícios
        try:
            if greedy_from(start):
                st.elapsed = now() - st.start
                return True, st
        except TimeoutError:
            st.elapsed = now() - st.start
            return False, st

    st.elapsed = now() - st.start
    return False, st


# -----------------------------
# CLI
# -----------------------------
def main(argv: List[str]) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print("Uso: python codigo/hamiltonian.py <arquivo> [--algo bt|bnb|rnd] [--stats] [--timelimit S] [--restarts K] [--seed SEED]")
        return 2

    path = argv[1]
    algo = "bnb"
    show_stats = False
    time_limit = 2.0
    restarts = 2000
    seed = 42

    i = 2
    while i < len(argv):
        if argv[i] == "--algo" and i + 1 < len(argv):
            algo = argv[i + 1].strip()
            i += 2
        elif argv[i] == "--stats":
            show_stats = True
            i += 1
        elif argv[i] == "--timelimit" and i + 1 < len(argv):
            time_limit = float(argv[i + 1])
            i += 2
        elif argv[i] == "--restarts" and i + 1 < len(argv):
            restarts = int(argv[i + 1])
            i += 2
        elif argv[i] == "--seed" and i + 1 < len(argv):
            seed = int(argv[i + 1])
            i += 2
        else:
            # argumento desconhecido
            i += 1

    adj = read_graph(path)

    if algo == "bt":
        ok, st = hamilton_bt(adj, time_limit)
    elif algo == "bnb":
        ok, st = hamilton_bnb(adj, time_limit)
    elif algo == "rnd":
        ok, st = hamilton_rnd(adj, time_limit, restarts=restarts, seed=seed)
    else:
        print("Erro: --algo deve ser bt, bnb ou rnd")
        return 2

    print("SIM" if ok else "NAO")
    if show_stats:
        # saída mecanicamente verificável
        print(f"calls={st.calls} backtracks={st.backtracks} prunes={st.prunes} elapsed={st.elapsed:.6f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
