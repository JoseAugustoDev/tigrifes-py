# Tigrifes — Experimentos em Python - Jose Augusto, Matheus e Rodolfo.

Projeto de análise de resultados de rodadas, com tabelas e gráficos em Python.

O arquivo `maquina_estatistica.py` oferece um menu para jogar individualmente com créditos fictícios ou executar os experimentos.

## Estado do projeto

O **Experimento 4 — Probabilidade condicional** analisa 10.000 rodadas e compara a proporção de prêmios na rodada seguinte conforme a rodada anterior tenha sido premiada ou não. São analisados 9.999 pares consecutivos, com uma referência teórica de vitória de 4%.

O **Experimento 5 — Comparação de pagamentos** compara a configuração base com prêmios aumentados em 10%, usando as mesmas rodadas.

## Pré-requisitos

- Python 3 com `pip` e suporte a ambientes virtuais (`venv`). Utilize Python 3.12 ou superior como base para a instalação.
- Arquivo `rodadas.xlsx` na mesma pasta dos scripts, necessário para os experimentos 4 e 5.
- Ambiente gráfico para abrir a janela do gráfico (ou utilize o modo sem janela descrito abaixo).

## Instalação

Baixe e extraia o projeto ou clone este repositório. Abra um terminal **na pasta do projeto**, onde está `requirements.txt`.

Crie um ambiente virtual e instale as dependências. Os comandos abaixo usam o Python do ambiente diretamente, sem precisar ativá-lo.

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se o comando `py` não estiver disponível, utilize `python` no primeiro comando. Se nenhum dos dois for reconhecido, instale o Python e habilite sua inclusão no PATH; depois reabra o terminal.

### Linux e macOS

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

Se a criação do ambiente falhar por falta de `venv` ou `pip`, instale esses componentes pelo gerenciador de pacotes do seu sistema e repita o comando.

### Dependências

| Pacote | Uso | Scripts |
| --- | --- | --- |
| `pandas` | Leitura e análise dos dados e exportação de tabelas CSV/XLSX. | Experimentos 4 e 5. |
| `openpyxl` | Suporte ao pandas para ler `rodadas.xlsx` e gravar `experimento5_rodadas.xlsx`. | Leitura nos experimentos 4 e 5; escrita no 5. |
| `matplotlib` | Exibição dos gráficos e salvamento das imagens PNG. | Experimentos 4 e 5. |

O `requirements.txt` contém as três dependências externas necessárias aos experimentos, sem fixar versões. `openpyxl` precisa estar instalado mesmo sem um `import openpyxl` nos scripts, pois é utilizado pelo pandas nas operações com Excel. Não é necessário instalar Microsoft Excel para executar os experimentos.

Os módulos `argparse`, `csv`, `datetime`, `pathlib`, `random`, `secrets`, `subprocess` e `sys` fazem parte da biblioteca padrão do Python e não precisam ser instalados com `pip`. As dependências dos pacotes, como NumPy, são instaladas automaticamente pelo `pip`.

A instalação foi validada no Windows com Python **3.14.6**, pandas **3.1.0**, matplotlib **3.11.2** e openpyxl **3.1.5**. O comando `pip check` não encontrou conflitos, e o menu, o jogo e os experimentos 4 e 5 foram executados, incluindo leitura e escrita de arquivos e geração de gráficos em modo sem janela. Essas são as versões verificadas, não versões fixadas pelo projeto; outras combinações e sistemas operacionais não foram validados nesta revisão.

## Menu principal

Depois de instalar as dependências, abra o menu com o Python do ambiente virtual.

No Windows (PowerShell):

```powershell
.\.venv\Scripts\python.exe maquina_estatistica.py
```

No Linux ou macOS:

```bash
./.venv/bin/python maquina_estatistica.py
```

Escolha uma das opções:

| Opção | Ação |
| --- | --- |
| `1` | Jogar individualmente. |
| `2` | Executar `experimento-4.py`. |
| `3` | Executar `experimento-5.py`. |
| `0` | Encerrar o programa. |

Os experimentos usam o mesmo Python do menu e procuram `rodadas.xlsx` na pasta dos scripts. As tabelas são salvas em `resultados/` e as imagens em `graficos/`, dentro da pasta do projeto. Essas pastas são criadas automaticamente. Feche a janela do gráfico para retornar ao menu e escolher outra opção. As configurações de execução sem janela descritas abaixo também se aplicam ao menu.

### Jogar individualmente

O menu e o jogo usam somente a biblioteca padrão do Python. Para jogar, também é possível abrir o menu com `py -3 maquina_estatistica.py` no Windows ou `python3 maquina_estatistica.py` no Linux/macOS, sem instalar as dependências dos experimentos.

Após escolher `1`, pressione **ENTER** para jogar uma rodada ou digite **S** para voltar ao menu. Cada rodada custa 1 crédito e apenas três símbolos iguais na linha central concedem prêmio. O saldo inicial é de 100 créditos; a sessão termina quando você sai ou fica sem saldo.

As opções `--saldo`, `--semente` e `--saida` se aplicam ao jogo individual: ajustam o saldo inicial, permitem repetir uma sequência de sorteios e escolhem a pasta do histórico. Exemplo no Windows:

```powershell
.\.venv\Scripts\python.exe maquina_estatistica.py --saldo 50 --semente 2026 --saida resultados
```

Se houver alguma rodada, o histórico será salvo em `resultados/jogador/sessao_<data>_seed<semente>.csv` (ou na pasta indicada por `--saida`). Sair com Ctrl+C durante a espera por uma jogada também salva o histórico.

## Executar sem janela de gráfico

Em ambientes sem interface gráfica, configure `MPLBACKEND=Agg` antes de abrir o menu. Os experimentos continuam salvando os arquivos em `resultados/` e `graficos/`, mas não abrem janelas. O matplotlib pode emitir um aviso de que o backend não é interativo.

No Windows (PowerShell):

```powershell
$env:MPLBACKEND = "Agg"
.\.venv\Scripts\python.exe maquina_estatistica.py
Remove-Item Env:MPLBACKEND
```

No Linux ou macOS:

```bash
MPLBACKEND=Agg ./.venv/bin/python maquina_estatistica.py
```

Para executar um experimento diretamente, substitua `maquina_estatistica.py` por `experimento-4.py` ou `experimento-5.py` nesses comandos.

Se aparecer `ModuleNotFoundError`, instale o `requirements.txt` usando o mesmo Python que abre o menu. Para verificar conflitos na instalação, execute `.\.venv\Scripts\python.exe -m pip check` no Windows ou `./.venv/bin/python -m pip check` no Linux/macOS.

## Uso de IA

O método salvar_historico foi implementado com auxílio da IA. 

As exportações dos resultados dos experimentos para arquivos csv também.

Ao final de cada experimento.py tem um fragmento de codigo responsável por gerar os gráficos utilizados. Esse código foi feito com o auxílio de IA. 

Também utilizamos para correções gramaticais e ortográficas no relatório.

Isso não significa que foi "vibecodado". Na verdade, todo prompt e código gerado foi revisado e avaliado pelo grupo.