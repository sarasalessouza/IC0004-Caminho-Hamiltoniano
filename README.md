# IC0004 — Caminho Hamiltoniano

Repositório reprodutível do trabalho de IC0004 (Caminho Hamiltoniano): redução polinomial, algoritmos (BT, BnB, heurística com reinícios) e experimentos.

## Requisitos
- **Python 3.12+ (recomendado)**  
  > Observação: versões *alpha* do Python (ex.: 3.15a) podem não ter wheels de bibliotecas científicas.
- (Opcional para gráficos) `matplotlib`:
```bash
python -m pip install -r requirements.txt
```

## Formato das instâncias (conforme enunciado)
Arquivo texto:
- 1ª linha: `n m`
- Próximas `m` linhas: `u v` (aresta **não direcionada**)

## Rodar uma instância (SIM/NAO + metricas)
Exemplo mínimo (em `instances/exemplo_minimo_sim.txt`):
```bash
python codigo/hamiltonian.py instances/exemplo_minimo_sim.txt --algo bt --stats
python codigo/hamiltonian.py instances/exemplo_minimo_sim.txt --algo bnb --stats
python codigo/hamiltonian.py instances/exemplo_minimo_sim.txt --algo rnd --stats --restarts 2000 --seed 7
```

## Reproduzir experimentos (pipeline completo)
1) Gerar instâncias ER G(n,p) (10/20/30/40/50; esparso/denso):
```bash
python scripts/generate_instances.py
```

2) Executar algoritmos e gerar CSV bruto:
```bash
python scripts/run_experiments.py
```

3) Agregar (medianas + taxa SIM):
```bash
python scripts/aggregate_results.py
```

4) (Opcional) Gerar gráficos:
```bash
python -m pip install -r requirements.txt
python scripts/plot_results.py
```

Saídas:
- `results/raw.csv`
- `results/aggregated.csv`
- `results/figs/*.png`

## Relatório
Arquivos finais em `docs/`.
