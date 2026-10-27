from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_RESULTADOS = PASTA_PROJETO / "resultados"
PASTA_GRAFICOS = PASTA_PROJETO / "graficos"

df = pd.read_excel(PASTA_PROJETO / "rodadas.xlsx")
# Aceitar Rolo1, Rolo2, Rolo3 e Venceu, ignorando espaços e maiúsculas/minúsculas.
df.columns = df.columns.str.strip().str.capitalize()

if "Venceu" not in df.columns:
    raise ValueError("A planilha deve conter a coluna Venceu.")


# 1. Converter a coluna Venceu para valores booleanos
def converter_resultado(valor):
    texto = str(valor).strip().upper()

    if texto in ("VERDADEIRO", "TRUE", "1"):
        return True
    if texto in ("FALSO", "FALSE", "0"):
        return False

    raise ValueError(f"Resultado inválido: {valor}")


resultados = df["Venceu"].apply(converter_resultado).tolist()

# 2. Verificar a quantidade de rodadas
if len(resultados) != 10000:
    raise ValueError(f"Esperadas 10000 rodadas, encontradas {len(resultados)}")

# 3. Criar contadores para cada grupo
contagens = {True: {"total": 0, "premios": 0}, False: {"total": 0, "premios": 0}}

# 4. Analisar os 9.999 pares consecutivos
for anterior, seguinte in zip(resultados[:-1], resultados[1:]):

    contagens[anterior]["total"] += 1

    if seguinte:
        contagens[anterior]["premios"] += 1

# 5. Construir tabela de resultados
tabela = []

for resultado_anterior, nome in [(True, "Premiada"), (False, "Não premiada")]:
    total = contagens[resultado_anterior]["total"]
    premios = contagens[resultado_anterior]["premios"]

    proporcao = (
        f"{premios / total:.2%}".replace(".", ",") if total > 0 else "Não estimável"
    )

    tabela.append(
        {
            "Resultado anterior": nome,
            "Total de pares": total,
            "Prêmios na rodada seguinte": premios,
            "Proporção": proporcao,
        }
    )

tabela_df = pd.DataFrame(tabela)

# 6. Exibir resultados
print("\nEXPERIMENTO 4 - PROBABILIDADE CONDICIONAL\n")
print(tabela_df.to_string(index=False))

print("\nTotal de pares analisados:", len(resultados) - 1)
print("Probabilidade teórica de vitória: 4%")

# 7. Exportar tabela para CSV
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
tabela_df.to_csv(
    PASTA_RESULTADOS / "experimento4_resultados.csv",
    index=False, sep=";", encoding="utf-8-sig"
)

print(f"\nResultados salvos em: {PASTA_RESULTADOS}")

# 8. Plotar a probabilidade de prêmio conforme o resultado anterior (Feito com IA)
rotulos = ["Premiada", "Não premiada"]
proporcoes = [
    contagens[resultado]["premios"] / contagens[resultado]["total"]
    if contagens[resultado]["total"] > 0
    else float("nan")
    for resultado in (True, False)
]

fig, ax = plt.subplots(figsize=(8, 5))
barras = ax.bar(rotulos, proporcoes, color=["#2878B5", "#F2A541"], width=0.55)
ax.axhline(0.04, color="#C0392B", linestyle="--", label="Probabilidade teórica: 4%")

for barra, proporcao in zip(barras, proporcoes):
    estimavel = pd.notna(proporcao)
    texto = f"{proporcao:.2%}".replace(".", ",") if estimavel else "Não estimável"
    ax.annotate(
        texto,
        (barra.get_x() + barra.get_width() / 2, proporcao if estimavel else 0),
        xytext=(0, 6),
        textcoords="offset points",
        ha="center",
    )

ax.set_title("Experimento 4 — Probabilidade condicional")
ax.set_xlabel("Resultado da rodada anterior")
ax.set_ylabel("Proporção de prêmios na rodada seguinte")
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
ax.set_ylim(0, max(0.04, *(p for p in proporcoes if pd.notna(p))) * 1.3)
ax.set_axisbelow(True)
ax.grid(axis="y", alpha=0.25)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16))
fig.tight_layout()
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)
arquivo_grafico = PASTA_GRAFICOS / "experimento4_grafico.png"
fig.savefig(arquivo_grafico, dpi=300, bbox_inches="tight")
print(f"Gráfico salvo em: {arquivo_grafico}")
plt.show()
plt.close(fig)
