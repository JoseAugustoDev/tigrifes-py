from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

APOSTA = 1
PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_RESULTADOS = PASTA_PROJETO / "resultados"
PASTA_GRAFICOS = PASTA_PROJETO / "graficos"
ARQUIVO = PASTA_PROJETO / "rodadas.xlsx"

# 1. Carregar as mesmas 10.000 rodadas
df = pd.read_excel(ARQUIVO)

df.columns = df.columns.str.strip().str.capitalize()

colunas = ["Rolo1", "Rolo2", "Rolo3"]
faltantes = [coluna for coluna in colunas + ["Venceu"] if coluna not in df.columns]
if faltantes:
    raise ValueError(f"Colunas ausentes na planilha: {', '.join(faltantes)}")

if len(df) != 10000:
    raise ValueError("A planilha deve conter 10.000 rodadas.")

for coluna in colunas:
    df[coluna] = pd.to_numeric(df[coluna], errors="raise")

simbolos = [0, 1, 2, 3, 4]

if not df[colunas].isin(simbolos).all().all():
    raise ValueError("Os rolos devem conter valores de 0 a 4.")

# 2. Definir tabelas de pagamento
tabela_base = {0: 5, 1: 10, 2: 15, 3: 25, 4: 50}

tabela_10 = {simbolo: premio * 1.10 for simbolo, premio in tabela_base.items()}

# 3. Reutilizar o resultado registrado na planilha, como no experimento 4
def converter_resultado(valor):
    texto = str(valor).strip().upper()

    if texto in ("VERDADEIRO", "TRUE", "1"):
        return True
    if texto in ("FALSO", "FALSE", "0"):
        return False

    raise ValueError(f"Resultado inválido na coluna Venceu: {valor}")


ganhou = df["Venceu"].apply(converter_resultado)

n = len(df)
qtd_vitorias = int(ganhou.sum())

# 4. Probabilidade teórica e frequência observada
prob_teorica = 5 / (5**3)
freq_observada = qtd_vitorias / n

# 5. Comparar as duas configurações
resultados = []

for nome, tabela in [("Base", tabela_base), ("Prêmios +10%", tabela_10)]:

    # Venceu define se há prêmio; Rolo1 identifica seu valor na tabela.
    pagamentos = df["Rolo1"].map(tabela).where(ganhou, 0.0)

    # Guardar pagamentos na planilha
    df[f"pagamento_{nome}"] = pagamentos

    # Prêmio médio teórico por rodada
    premio_teorico = sum(tabela.values()) / 125

    # Prêmio médio observado por rodada
    premio_observado = pagamentos.mean()

    # Lucro médio por rodada
    lucro_teorico = premio_teorico - APOSTA
    lucro_observado = premio_observado - APOSTA

    # RTP = retorno médio / aposta
    rtp_teorico = (premio_teorico / APOSTA) * 100
    rtp_observado = (premio_observado / APOSTA) * 100

    resultados.append(
        {
            "Configuração": nome,
            "Prob. teórica (%)": prob_teorica * 100,
            "Frequência observada (%)": freq_observada * 100,
            "Quantidade de prêmios": qtd_vitorias,
            "Prêmio médio teórico": premio_teorico,
            "Prêmio médio observado": premio_observado,
            "Lucro médio teórico": lucro_teorico,
            "Lucro médio observado": lucro_observado,
            "RTP teórico (%)": rtp_teorico,
            "RTP observado (%)": rtp_observado,
        }
    )

# 6. Criar tabela de resultados
resumo = pd.DataFrame(resultados)

print("\nEXPERIMENTO 5 - RESULTADOS\n")
print(resumo.round(4).to_string(index=False))

# 7. Conferir os resultados teóricos
assert abs(resultados[0]["RTP teórico (%)"] - 84.0) < 1e-9
assert abs(resultados[1]["RTP teórico (%)"] - 92.4) < 1e-9
assert abs(resultados[1]["Lucro médio teórico"] - (-0.076)) < 1e-9

# 8. Exportar os resultados
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)
resumo.to_csv(
    PASTA_RESULTADOS / "experimento5_resultados.csv",
    index=False,
    sep=";",
    decimal=",",
    encoding="utf-8-sig",
)

df.to_excel(PASTA_RESULTADOS / "experimento5_rodadas.xlsx", index=False)

print(f"\nResultados salvos em: {PASTA_RESULTADOS}")

# 9. Comparar os resultados teóricos e observados em gráficos (Feito com IA)
fig, eixos = plt.subplots(1, 2, figsize=(12, 5))
posicoes = list(range(len(resumo)))
largura = 0.35

for ax, coluna_teorica, coluna_observada, titulo, unidade in [
    (eixos[0], "RTP teórico (%)", "RTP observado (%)", "Retorno ao jogador (RTP)", "%"),
    (
        eixos[1],
        "Lucro médio teórico",
        "Lucro médio observado",
        "Lucro médio do jogador por rodada",
        "",
    ),
]:
    for deslocamento, coluna, legenda, cor in [
        (-largura / 2, coluna_teorica, "Teórico", "#2878B5"),
        (largura / 2, coluna_observada, "Observado", "#F2A541"),
    ]:
        barras = ax.bar(
            [posicao + deslocamento for posicao in posicoes],
            resumo[coluna],
            width=largura,
            label=legenda,
            color=cor,
        )
        casas = 2 if unidade == "%" else 4
        rotulos = [
            f"{valor:.{casas}f}{unidade}".replace(".", ",")
            for valor in resumo[coluna]
        ]
        ax.bar_label(barras, labels=rotulos, padding=5, fontsize=9)

    ax.set_title(titulo)
    ax.set_xticks(posicoes, resumo["Configuração"])
    ax.set_xlabel("Configuração de pagamentos")
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.25)

eixos[0].axhline(
    100, color="#C0392B", linestyle="--", label="Equilíbrio: RTP de 100%"
)
eixos[0].yaxis.set_major_formatter(PercentFormatter(xmax=100))
eixos[0].set_ylabel("Retorno médio / aposta")
eixos[1].axhline(0, color="#C0392B", linestyle="--", label="Equilíbrio: lucro zero")
eixos[1].set_ylabel("Unidades monetárias por rodada")

for ax in eixos:
    ax.margins(y=0.2)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17))

fig.suptitle(f"Experimento 5 — Comparação de pagamentos ({n:,} rodadas)".replace(",", "."))
fig.tight_layout()
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)
arquivo_grafico = PASTA_GRAFICOS / "experimento5_grafico.png"
fig.savefig(arquivo_grafico, dpi=300, bbox_inches="tight")
print(f"Gráfico salvo em: {arquivo_grafico}")
plt.show()
plt.close(fig)
