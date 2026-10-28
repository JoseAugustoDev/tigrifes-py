"""Experimento 1: frequências e lucro em 10.000 rodadas (semente 2026)."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PASTA = Path(__file__).resolve().parent.parent
PREMIOS = {0: 5, 1: 10, 2: 15, 3: 25, 4: 50}
LUCROS = [-1, 4, 9, 14, 24, 49]

dados = pd.read_excel(PASTA / "planilhas" / "rodadas.xlsx")
dados.columns = dados.columns.str.strip().str.capitalize()
if len(dados) != 10000:
    raise ValueError("rodadas.xlsx deve conter exatamente 10.000 rodadas.")

rolos = dados[["Rolo1", "Rolo2", "Rolo3"]].apply(pd.to_numeric, errors="raise")
if not rolos.isin(list(PREMIOS)).all().all():
    raise ValueError("Os rolos devem conter valores inteiros de 0 a 4.")

venceu = rolos["Rolo1"].eq(rolos["Rolo2"]) & rolos["Rolo2"].eq(rolos["Rolo3"])
premio = rolos["Rolo1"].map(PREMIOS).where(venceu, 0)
lucro = premio - 1  # Aposta fixa de um crédito por rodada.

contagens = lucro.value_counts()
tabela = pd.DataFrame({
    "Lucro (créditos)": LUCROS,
    "Probabilidade teórica": [120 / 125] + [1 / 125] * 5,
    "Contagem": [int(contagens.get(valor, 0)) for valor in LUCROS],
})
tabela["Frequência relativa"] = tabela["Contagem"] / len(dados)
assert tabela["Contagem"].sum() == 10000

resumo = pd.DataFrame([{
    "Lucro médio (créditos)": lucro.mean(),
    "RTP observado (%)": 100 * premio.mean(),
    "Rodadas premiadas": int(venceu.sum()),
    "Proporção premiada (%)": 100 * venceu.mean(),
    "Desvio-padrão amostral (créditos)": lucro.std(ddof=1),
}])

print("\nEXPERIMENTO 1 — FREQUÊNCIAS E PROBABILIDADES\n")
print(tabela.to_string(index=False, float_format=lambda valor: f"{valor:.4f}".replace(".", ",")))
print("\nContagens somadas:", tabela["Contagem"].sum())
print("\n" + resumo.to_string(index=False, float_format=lambda valor: f"{valor:.4f}".replace(".", ",")))
print("\nO lucro médio é o ganho ou perda líquida por rodada, em créditos.")
print("O desvio-padrão amostral mostra a dispersão dos lucros em torno dessa média, em créditos.")

pasta_resultados = PASTA / "resultados"
pasta_resultados.mkdir(exist_ok=True)
tabela.to_csv(pasta_resultados / "experimento1_frequencias.csv", index=False,
              sep=";", decimal=",", encoding="utf-8-sig")
resumo.to_csv(pasta_resultados / "experimento1_resumo.csv", index=False,
             sep=";", decimal=",", encoding="utf-8-sig")

fig, ax = plt.subplots(figsize=(9, 5))
posicoes = list(range(len(LUCROS)))
ax.bar([x - 0.2 for x in posicoes], tabela["Probabilidade teórica"] * 100,
       width=0.4, label="Teórica", color="#2878B5")
ax.bar([x + 0.2 for x in posicoes], tabela["Frequência relativa"] * 100,
       width=0.4, label="Observada", color="#F2A541")
ax.set_xticks(posicoes, [str(valor) for valor in LUCROS])
ax.set(title="Experimento 1 — Frequências teóricas e observadas",
       xlabel="Lucro líquido por rodada (créditos)", ylabel="Frequência (%)")
ax.grid(axis="y", alpha=0.25)
ax.set_axisbelow(True)
ax.legend()
fig.tight_layout()

pasta_graficos = PASTA / "graficos"
pasta_graficos.mkdir(exist_ok=True)
fig.savefig(pasta_graficos / "experimento1_frequencias.png", dpi=300)
plt.show()
plt.close(fig)
print(f"\nTabelas salvas em {pasta_resultados}")
print(f"Gráfico salvo em {pasta_graficos}")
