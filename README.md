# Caminho Hamiltoniano – IC0004 (Algoritmos e Grafos)

## 📌 Descrição
Este repositório contém a implementação (Python) do trabalho **Caminho Hamiltoniano: Complexidade, Algoritmos e Experimentos**, desenvolvido para a disciplina **IC0004 – Algoritmos e Grafos (UFBA)**.

- `bt`: Backtracking puro
- `bnb`: Branch and Bound (podas por conectividade do restante + grau residual 0)
- `rnd`: Heurística gulosa com reinícios aleatórios

O objetivo é analisar formalmente a complexidade do problema, implementar algoritmos exatos e heurísticos, e realizar experimentos computacionais.

---

## 📂 Estrutura do repositório

```
IC0004-Caminho-Hamiltoniano/
├─ codigo/
│  ├─ hamiltonian.py              # CLI principal (resolve SIM/NÃO)
│  └─ algorithms.py               # BT, BnB, RND (implementações)
├─ instances/
│  ├─ exemplo_enunciado.txt       # no formato n m + arestas
│  ├─ auto/                       # instâncias geradas automaticamente
│  └─ README.md                   # descreve formato + como foram geradas
├─ scripts/
│  ├─ generate_instances.py       # gera G(n,p) esparso/denso + seeds
│  ├─ run_experiments.py          # executa algoritmos e salva CSV bruto
│  ├─ aggregate_results.py        # agrega (medianas, taxa SIM)
│  └─ plot_results.py             # gera PNGs a partir dos CSVs
├─ results/
│  ├─ raw.csv
│  ├─ aggregated.csv
│  └─ figs/
│     ├─ tempo_vs_n_esparso.png
│     ├─ tempo_vs_n_denso.png
│     ├─ calls_vs_n_esparso.png
│     └─ calls_vs_n_denso.png
├─ requirements.txt
└─ README.md
```

---

## ▶️ Como executar

```bash
python -m venv .venv
# Windows (Git Bash): source .venv/Scripts/activate
# Linux/Mac:          source .venv/bin/activate
pip install -r requirements.txt
```
---

## 🔁 Rodar em uma instância

```bash
python codigo/hamiltonian.py instances/exemplo_minimo_sim.txt --algo bt --stats
python codigo/hamiltonian.py instances/exemplo_minimo_sim.txt --algo bnb --stats
python codigo/hamiltonian.py instances/exemplo_minimo_sim.txt --algo rnd --stats --restarts 2000 --seed 7
```

---

## 🔬 Reproduzir experimentos + gráficos

```bash
python scripts/generate_instances.py
python scripts/run_experiments.py
python scripts/aggregate_results.py
```

Gerar gráficos:
```bash
python -m pip install -r requirements.txt
python scripts/plot_results.py

Saídas:

- `results/raw.csv`
- `results/aggregated.csv`
- `results/figs/*.png`
```
---

## 📚 Referências

- FIGUEIREDO; LAMB. *Teoria da Computação*. SBC, 2011.
- GAREY; JOHNSON. *Computers and Intractability*. 1979.
- LIMA, George. Programação Dinâmica. Instituto de Computação, UFBA. (Slide da aula).
- LIMA, George. Algoritmos Gulosos. Instituto de Computação, UFBA. (Slide da aula).
- LIMA, George. Avanços e Retrocessos (Backtracking). Instituto de Computação, UFBA. (Slide da aula).
- LIMA, George. Introdução às classes P, NP e NP-Completo. Instituto de Computação, UFBA. (Slide da aula).
- LIMA, George. Grafos (conceitos iniciais). Instituto de Computação, UFBA. (Slide da aula).
- LIMA, George. Grafos ponderados e distâncias. Instituto de Computação, UFBA. (Slide da aula).
- Wikipédia – Problema do Caminho Hamiltoniano.

## ✅ Relatório
Entregue via sistema SIGAA.
