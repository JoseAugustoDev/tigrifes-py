"""Experimento 3: saldo limitado em 100 sessões de até 500 rodadas."""

import random
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PASTA = Path(__file__).resolve().parent.parent
PREMIOS = {0: 5, 1: 10, 2: 15, 3: 25, 4: 50}
SALDO_INICIAL = 100
MAX_RODADAS = 500
PARTICIPANTES = 100

# O mesmo gerador continua entre os participantes, sem reiniciar a semente.
gerador = random.Random(42)
sessoes = []
trajetorias = []

for participante in range(1, PARTICIPANTES + 1):
    saldo = SALDO_INICIAL
    rodadas = 0
    trajetoria = [saldo]

    while rodadas < MAX_RODADAS and saldo >= 1:
        rolos = [gerador.randrange(5) for _ in range(3)]
        premio = PREMIOS[(rolos[0] + 1) % 5] if rolos[0] == rolos[1] == rolos[2] else 0
        saldo += premio - 1
        rodadas += 1
        trajetoria.append(saldo)

    resultado = "Ganho" if saldo > SALDO_INICIAL else "Empate" if saldo == SALDO_INICIAL else "Perda"
    esgotou = saldo < 1
    sessoes.append({
        "Participante": participante,
        "Saldo final (créditos)": saldo,
        "Rodadas": rodadas,
        "Resultado": resultado,
        "Esgotou": "SIM" if esgotou else "NÃO",
    })

    if participante <= 5:
        # Após a parada, repetir o último saldo até a rodada 500.
        trajetoria.extend([saldo] * (MAX_RODADAS + 1 - len(trajetoria)))
        trajetorias.append(trajetoria)

ganhos = sum(sessao["Resultado"] == "Ganho" for sessao in sessoes)
empates = sum(sessao["Resultado"] == "Empate" for sessao in sessoes)
perdas = sum(sessao["Resultado"] == "Perda" for sessao in sessoes)
esgotamentos = sum(sessao["Esgotou"] == "SIM" for sessao in sessoes)
saldos_finais = [sessao["Saldo final (créditos)"] for sessao in sessoes]

assert ganhos + empates + perdas == PARTICIPANTES
assert esgotamentos <= perdas
assert all(len(trajetoria) == MAX_RODADAS + 1 for trajetoria in trajetorias)

resumo = pd.DataFrame([{
    "Participantes": PARTICIPANTES,
    "Ganho (%)": 100 * ganhos / PARTICIPANTES,
    "Empate (%)": 100 * empates / PARTICIPANTES,
    "Perda (%)": 100 * perdas / PARTICIPANTES,
    "Esgotamento (%)": 100 * esgotamentos / PARTICIPANTES,
    "Saldo final médio (créditos)": statistics.mean(saldos_finais),
    "Saldo final mediano (créditos)": statistics.median(saldos_finais),
}])

print("\nEXPERIMENTO 3 — SALDO LIMITADO\n")
print(resumo.to_string(index=False, float_format=lambda valor: f"{valor:.2f}".replace(".", ",")))
print(f"\nGanho + empate + perda: {ganhos + empates + perdas}/{PARTICIPANTES} participantes (100%).")
print(f"Esgotamento: {esgotamentos} participantes, todos entre as perdas.")

pasta_resultados = PASTA / "resultados"
pasta_resultados.mkdir(exist_ok=True)
pd.DataFrame(sessoes).to_csv(pasta_resultados / "experimento3_sessoes.csv", index=False,
                              sep=";", encoding="utf-8-sig")
resumo.to_csv(pasta_resultados / "experimento3_resumo.csv", index=False,
              sep=";", decimal=",", encoding="utf-8-sig")

fig, ax = plt.subplots(figsize=(10, 5))
for participante, trajetoria in enumerate(trajetorias, start=1):
    ax.plot(range(MAX_RODADAS + 1), trajetoria, label=f"Participante {participante}")
ax.axhline(SALDO_INICIAL, color="black", linestyle="--", linewidth=1, label="Saldo inicial")
ax.set(title="Experimento 3 — Primeiros cinco participantes",
       xlabel="Rodada da sessão", ylabel="Saldo (créditos)")
ax.grid(alpha=0.25)
ax.legend()
fig.tight_layout()

pasta_graficos = PASTA / "graficos"
pasta_graficos.mkdir(exist_ok=True)
fig.savefig(pasta_graficos / "experimento3_trajetorias.png", dpi=300)
plt.show()
plt.close(fig)
print(f"\nResultados salvos em {pasta_resultados}")
print(f"Gráfico salvo em {pasta_graficos}")
