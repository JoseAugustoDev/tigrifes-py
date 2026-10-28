"""Experimento 2: médias acumuladas de três sequências de 10.000 rodadas."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PASTA = Path(__file__).resolve().parent.parent
SEMENTES = (10, 2026, 123456)
MARCOS = (100, 1000, 10000)

# Na planilha, Lucro já é o lucro acumulado. Dividir pelo número de
# rodadas evita usar a coluna Lucro médio, que está arredondada.
medias = {}
for semente in SEMENTES:
    arquivo = PASTA / "planilhas" / f"exp-2-seed-{semente}.xlsx"
    dados = pd.read_excel(arquivo)
    if len(dados) != 10000:
        raise ValueError(f"{arquivo.name} deve conter 10.000 rodadas.")
    lucro = pd.to_numeric(dados["Lucro"], errors="raise")
    medias[semente] = lucro / pd.Series(range(1, 10001))

tabela = pd.DataFrame(
    {
        f"Após {n:,} rodadas".replace(",", "."): [
            medias[semente].iloc[n - 1] for semente in SEMENTES
        ]
        for n in MARCOS
    },
    index=pd.Index(SEMENTES, name="Semente"),
)

print("\nEXPERIMENTO 2 — MÉDIA ACUMULADA\n")
print(tabela.to_string(float_format=lambda valor: f"{valor:.4f}".replace(".", ",")))

# O Experimento 1 usa semente 2026: comparar os dez primeiros sorteios.
arquivo_e1 = PASTA / "planilhas" / "rodadas.xlsx"
if arquivo_e1.exists():
    e1 = pd.read_excel(arquivo_e1)
    e2 = pd.read_excel(PASTA / "planilhas" / "exp-2-seed-2026.xlsx")
    primeiras_e1 = e1[["Rolo1", "Rolo2", "Rolo3"]].head(10).to_numpy()
    primeiras_e2 = e2[["Roleta 1", "Roleta 2", "Roleta 3"]].head(10).to_numpy()
    reproduzidos = (primeiras_e1 == primeiras_e2).all()
    print(f"Dez primeiros sorteios da semente 2026 reproduzidos: "
          f"{'SIM' if reproduzidos else 'NÃO'}")
else:
    print("Conferência da semente 2026 indisponível: rodadas.xlsx não encontrado.")

pasta_resultados = PASTA / "resultados"
pasta_resultados.mkdir(exist_ok=True)
tabela.to_csv(
    pasta_resultados / "experimento2_resultados.csv",
    sep=";", decimal=",", encoding="utf-8-sig",
)

fig, ax = plt.subplots(figsize=(10, 5))
for semente in SEMENTES:
    ax.plot(range(1, 10001), medias[semente], label=f"Semente {semente}")
ax.axhline(-0.16, color="red", linestyle="--", label="Média teórica: −0,16")
ax.set(title="Experimento 2 — Média acumulada", xlabel="Número de rodadas",
       ylabel="Lucro médio por rodada (créditos)")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

pasta_graficos = PASTA / "graficos"
pasta_graficos.mkdir(exist_ok=True)
fig.savefig(pasta_graficos / "experimento2_grafico.png", dpi=300)
print(f"Resultados salvos em {pasta_resultados}")
print(f"Gráfico salvo em {pasta_graficos}")
plt.show()
plt.close(fig)
