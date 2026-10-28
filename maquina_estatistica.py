"""Menu da Máquina Estatística: jogo individual e experimentos 1 a 5.

Uso: python maquina_estatistica.py [--saldo 100] [--semente 2026]
"""

import argparse
import csv
import random
import secrets
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SIMBOLOS = "ABCDE"
PREMIOS = {"A": 5, "B": 10, "C": 15, "D": 25, "E": 50}
APOSTA = 1


def mostrar_regras():
    print("\nMÁQUINA ESTATÍSTICA — JOGO INDIVIDUAL")
    print("Somente créditos fictícios. Aposta: 1 crédito por rodada.")
    print("Cada rolo sorteia uma parada de 0 a 4, independentemente.")
    print("O centro mostra o símbolo seguinte à parada na sequência circular ABCDE.")
    print("Somente três símbolos iguais na linha central concedem prêmio:")
    for simbolo, premio in PREMIOS.items():
        print(f"  {simbolo}-{simbolo}-{simbolo}: {premio} créditos")
    print("Outras combinações: 0. Lucro líquido = prêmio - aposta.")
    print("Chance de prêmio: 4% | RTP teórico: 84%\n")


def sortear_rodada(rng):
    paradas = [rng.randrange(len(SIMBOLOS)) for _ in range(3)]
    # Cada coluna mostra três símbolos consecutivos do rolo circular.
    tabuleiro = [
        [SIMBOLOS[(parada + linha) % len(SIMBOLOS)] for parada in paradas]
        for linha in range(3)
    ]
    centro = tabuleiro[1]
    premio = PREMIOS[centro[0]] if centro[0] == centro[1] == centro[2] else 0
    return paradas, tabuleiro, premio


def mostrar_tabuleiro(tabuleiro):
    print("          Rolo 1  Rolo 2  Rolo 3")
    for indice, linha in enumerate(tabuleiro):
        prefixo = "CENTRO -> " if indice == 1 else "          "
        print(prefixo + "     ".join(f"[{simbolo}]" for simbolo in linha))


def salvar_historico(historico, saida, semente):
    pasta = Path(saida) / "jogador"
    pasta.mkdir(parents=True, exist_ok=True)
    data = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    caminho = pasta / f"sessao_{data}_seed{semente}.csv"
    with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(historico[0]), delimiter=";")
        escritor.writeheader()
        escritor.writerows(historico)
    print(f"Histórico salvo em: {caminho.resolve()}")


def jogar(saldo_inicial=100, semente=None, saida=Path("resultados")):
    if saldo_inicial < APOSTA:
        raise ValueError("O saldo inicial deve ser pelo menos 1 crédito fictício.")
    if semente is None:
        semente = secrets.randbits(64)

    rng = random.Random(semente)
    saldo = saldo_inicial
    historico = []
    mostrar_regras()
    print(f"Saldo inicial: {saldo} créditos | Semente: {semente}")

    while saldo >= APOSTA:
        try:
            comando = input("\n[ENTER] Girar | [S] Sair: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nJogo encerrado pelo usuário.")
            break
        if comando in ("s", "sair", "q", "0"):
            break
        if comando:
            print("Comando inválido. Use ENTER ou S.")
            continue

        paradas, tabuleiro, premio = sortear_rodada(rng)
        lucro = premio - APOSTA
        saldo += lucro
        historico.append({
            "Rodada": len(historico) + 1,
            "Rolo1": paradas[0],
            "Rolo2": paradas[1],
            "Rolo3": paradas[2],
            "Linha central": "-".join(tabuleiro[1]),
            "Premiada": "VERDADEIRO" if premio > 0 else "FALSO",
            "Prêmio bruto": premio,
            "Lucro líquido": lucro,
            "Saldo": saldo,
        })

        print(f"\nRodada {len(historico)}")
        mostrar_tabuleiro(tabuleiro)
        print(f"Prêmio bruto: {premio} | Lucro líquido: {lucro:+d}")
        print(f"Saldo atual: {saldo} crédito(s)")

    if saldo < APOSTA:
        print("Saldo insuficiente para outra rodada.")
    print(f"\nSessão concluída: {len(historico)} rodadas | Saldo: {saldo} "
          f"| Lucro total: {saldo - saldo_inicial:+d} crédito(s)")
    if historico:
        salvar_historico(historico, saida, semente)
    else:
        print("Nenhuma rodada efetuada.")


def executar_experimento(numero):
    pasta = Path(__file__).resolve().parent
    arquivo = pasta / "experimentos" / f"experimento-{numero}.py"
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo.name}")
    print(f"\nExecutando experimento {numero}...", flush=True)
    subprocess.run([sys.executable, str(arquivo)], cwd=pasta, check=True)


def menu(saldo_inicial=100, semente=None, saida=Path("resultados")):
    while True:
        print("\nMÁQUINA ESTATÍSTICA")
        print("1. Experimento 1 — Frequências e probabilidades")
        print("2. Experimento 2 — Tamanho da amostra e média acumulada")
        print("3. Experimento 3 — Saldo limitado")
        print("4. Experimento 4 — Probabilidade condicional")
        print("5. Experimento 5 — Comparação de pagamentos")
        print("6. Jogar individualmente")
        print("0. Sair")
        try:
            opcao = input("Escolha uma opção: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nPrograma encerrado.")
            break

        try:
            if opcao == "0":
                break
            elif opcao == "6":
                jogar(saldo_inicial, semente, saida)
            elif opcao in ("1", "2", "3", "4", "5"):
                executar_experimento({"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}[opcao])
            else:
                print("Opção inválida. Escolha 1, 2, 3, 4, 5, 6 ou 0.")
        except subprocess.CalledProcessError:
            print("O experimento não foi concluído. Confira a mensagem de erro acima.")
        except (OSError, ValueError) as erro:
            print(f"Erro: {erro}")
        except KeyboardInterrupt:
            print("\nExecução interrompida. Retornando ao menu.")


def main():
    parser = argparse.ArgumentParser(description="Menu do jogo individual e dos experimentos.")
    parser.add_argument("--saldo", type=int, default=100, help="Saldo inicial (padrão: 100).")
    parser.add_argument("--semente", type=int, help="Semente opcional para repetir os sorteios.")
    parser.add_argument("--saida", type=Path, default=Path("resultados"),
                        help="Pasta para salvar o histórico (padrão: resultados).")
    args = parser.parse_args()
    if args.saldo < APOSTA:
        parser.error("O saldo inicial deve ser pelo menos 1 crédito fictício.")
    menu(args.saldo, args.semente, args.saida)


if __name__ == "__main__":
    main()
