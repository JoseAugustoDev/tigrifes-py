# Tigrifes — Experimentos em Python - Jose Augusto, Matheus e Rodolfo.

Projeto de análise de resultados de rodadas, com tabelas e gráficos em Python.

O arquivo `maquina_estatistica.py` oferece um menu para jogar individualmente com créditos fictícios ou executar os experimentos.

```text
tigrifes-py/
├── maquina_estatistica.py
├── experimentos/     # Scripts dos cinco experimentos
├── planilhas/        # Planilhas de entrada
├── resultados/       # Tabelas e histórico do jogo
└── graficos/         # Gráficos gerados
```

## Estado do projeto

O **Experimento 1 — Frequências e probabilidades** compara os seis lucros possíveis nas 10.000 rodadas de `planilhas/rodadas.xlsx` com as probabilidades teóricas, além de calcular lucro médio, RTP e desvio-padrão amostral.

O **Experimento 2 — Tamanho da amostra** compara as médias acumuladas das sequências de 10.000 rodadas com sementes 10, 2026 e 123456, usando as planilhas exportadas pela macro.

O **Experimento 3 — Saldo limitado** simula 100 participantes com 100 créditos iniciais, até 500 rodadas por sessão ou até o saldo se esgotar.

O **Experimento 4 — Probabilidade condicional** analisa 10.000 rodadas e compara a proporção de prêmios na rodada seguinte conforme a rodada anterior tenha sido premiada ou não. São analisados 9.999 pares consecutivos, com uma referência teórica de vitória de 4%.

O **Experimento 5 — Comparação de pagamentos** compara a configuração base com prêmios aumentados em 10%, usando as mesmas rodadas.

## Pré-requisitos

- Python 3 com `pip` e suporte a ambientes virtuais (`venv`). Utilize Python 3.12 ou superior como base para a instalação.
- Arquivo `planilhas/rodadas.xlsx` na pasta do projeto, necessário para os experimentos 1, 4 e 5.
- Arquivos `planilhas/exp-2-seed-10.xlsx`, `planilhas/exp-2-seed-2026.xlsx` e `planilhas/exp-2-seed-123456.xlsx` para o experimento 2. `planilhas/rodadas.xlsx` também permite conferir a reutilização da sequência do experimento 1.
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
| `pandas` | Leitura e análise dos dados e exportação de tabelas CSV/XLSX. | Experimentos 1 a 5. |
| `openpyxl` | Suporte ao pandas para ler as planilhas e gravar `experimento5_rodadas.xlsx`. | Leitura nos experimentos 1, 2, 4 e 5; escrita no 5. |
| `matplotlib` | Exibição dos gráficos e salvamento das imagens PNG. | Experimentos 1 a 5. |

O `requirements.txt` contém as três dependências externas necessárias aos experimentos, sem fixar versões. `openpyxl` precisa estar instalado mesmo sem um `import openpyxl` nos scripts, pois é utilizado pelo pandas nas operações com Excel. Não é necessário instalar Microsoft Excel para analisar as planilhas e gerar os gráficos.

Os módulos `argparse`, `csv`, `datetime`, `pathlib`, `random`, `secrets`, `statistics`, `subprocess` e `sys` fazem parte da biblioteca padrão do Python e não precisam ser instalados com `pip`. As dependências adicionais dos pacotes são instaladas automaticamente pelo `pip`.

A instalação foi validada no Windows com Python **3.14.6**, pandas **3.1.0**, matplotlib **3.11.2** e openpyxl **3.1.5**. O comando `pip check` não encontrou conflitos, e o menu, o jogo e os experimentos 1 a 5 foram executados. Essas são as versões verificadas, não versões fixadas pelo projeto.

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
| `1` | Executar `experimentos/experimento-1.py`. |
| `2` | Executar `experimentos/experimento-2.py`. |
| `3` | Executar `experimentos/experimento-3.py`. |
| `4` | Executar `experimentos/experimento-4.py`. |
| `5` | Executar `experimentos/experimento-5.py`. |
| `6` | Jogar individualmente. |
| `0` | Encerrar o programa. |

Os experimentos usam o mesmo Python do menu e leem as planilhas de `planilhas/`. As tabelas são salvas em `resultados/` e as imagens em `graficos/`, dentro da pasta do projeto. Essas pastas são criadas automaticamente. Feche a janela do gráfico para retornar ao menu e escolher outra opção. As configurações de execução sem janela descritas abaixo também se aplicam ao menu.

### Jogar individualmente

O menu e o jogo usam somente a biblioteca padrão do Python. Para jogar, também é possível abrir o menu com `py -3 maquina_estatistica.py` no Windows ou `python3 maquina_estatistica.py` no Linux/macOS, sem instalar as dependências dos experimentos.

Após escolher `6`, pressione **ENTER** para jogar uma rodada ou digite **S** para voltar ao menu. Cada rodada custa 1 crédito e apenas três símbolos iguais na linha central concedem prêmio. O saldo inicial é de 100 créditos; a sessão termina quando você sai ou fica sem saldo.

As opções `--saldo`, `--semente` e `--saida` se aplicam ao jogo individual: ajustam o saldo inicial, permitem repetir uma sequência de sorteios e escolhem a pasta do histórico. Exemplo no Windows:

```powershell
.\.venv\Scripts\python.exe maquina_estatistica.py --saldo 50 --semente 2026 --saida resultados
```

Se houver alguma rodada, o histórico será salvo em `resultados/jogador/sessao_<data>_seed<semente>.csv` (ou na pasta indicada por `--saida`). Sair com Ctrl+C durante a espera por uma jogada também salva o histórico.

## Experimento 1

O script lê as 10.000 rodadas de `planilhas/rodadas.xlsx`, geradas anteriormente pela macro com semente 2026 e sem regra de parada. Os rolos contêm as **paradas sorteadas**, de 0 a 4. O símbolo premiado na linha central é `(parada + 1) % 5`: 0 → 1, 1 → 2, 2 → 3, 3 → 4 e 4 → 0. Assim, três paradas iguais pagam, respectivamente, 10, 15, 25, 50 ou 5 créditos. A chance de prêmio continua 4%, mas os lucros observados mudam. A aposta é de 1 crédito e os lucros possíveis são −1, 4, 9, 14, 24 e 49 créditos.

Execute pela opção **1** do menu ou diretamente:

```powershell
.\.venv\Scripts\python.exe experimentos/experimento-1.py
```

No Linux ou macOS:

```bash
./.venv/bin/python experimentos/experimento-1.py
```

O script salva `resultados/experimento1_frequencias.csv` com os seis lucros, probabilidades teóricas, contagens e frequências relativas; `resultados/experimento1_resumo.csv` com lucro médio, RTP observado em porcentagem, proporção premiada e desvio-padrão amostral; e `graficos/experimento1_frequencias.png` com as frequências teóricas e observadas.

O **lucro médio** representa o resultado líquido por rodada: um valor negativo significa perda média em créditos. O **desvio-padrão amostral** mede quanto os lucros das rodadas se dispersam em torno dessa média, também em créditos; utiliza o divisor (N - 1). O RTP é o prêmio médio dividido pela aposta de 1 crédito e apresentado em porcentagem. O script confere que as seis contagens somam 10.000.

## Experimento 2

Coloque as três planilhas `exp-2-seed-10.xlsx`, `exp-2-seed-2026.xlsx` e `exp-2-seed-123456.xlsx` em `planilhas/`. Cada primeira aba deve conter 10.000 rodadas com este cabeçalho:

| Roleta 1 | Roleta 2 | Roleta 3 | Lucro | Lucro médio |
| --- | --- | --- | --- | --- |

As roletas contêm as paradas inteiras de 0 a 4. A coluna `Lucro` contém o lucro acumulado calculado pela versão anterior da macro, que não avançava o símbolo da linha central. O script preserva os sorteios e recalcula o lucro acumulado com `(parada + 1) % 5` antes de calcular as médias.

A média acumulada é calculada pelo lucro acumulado corrigido dividido pelo número de rodadas. A coluna `Lucro médio` também não é usada, pois os percentuais exportados estão arredondados.

Execute pela opção **2** do menu ou diretamente:

```powershell
.\.venv\Scripts\python.exe experimentos/experimento-2.py
```

No Linux ou macOS:

```bash
./.venv/bin/python experimentos/experimento-2.py
```

São gerados:

- `resultados/experimento2_resultados.csv`: tabela 3 × 3 das médias após 100, 1.000 e 10.000 rodadas, com as sementes identificando as linhas.
- `graficos/experimento2_grafico.png`: três trajetórias e referência horizontal em −0,16.

Quando `planilhas/rodadas.xlsx` está presente, o script compara seus dez primeiros sorteios com os da planilha `planilhas/exp-2-seed-2026.xlsx` e informa **SIM** ou **NÃO**. Sem esse arquivo, a conferência não é feita.

### Reprodução da semente 2026

Para testar a reprodução no aplicativo original, execute novamente a macro `Experimento2` nesse aplicativo com semente 2026 e compare os dez primeiros sorteios das duas execuções. O script Python apenas compara as planilhas já exportadas.

## Experimento 3

O script inicia `random.Random(42)` uma única vez e mantém a sequência de sorteios entre os 100 participantes. Cada um começa com 100 créditos e aposta 1 por rodada. A sessão termina após 500 rodadas ou quando o saldo fica abaixo de 1. O saldo é atualizado pelo lucro de cada rodada, usando o símbolo central `(parada + 1) % 5`, sem empréstimos ou reposição. Este experimento não precisa de planilha de entrada.

Execute pela opção **3** do menu ou diretamente:

```powershell
.\.venv\Scripts\python.exe experimentos/experimento-3.py
```

No Linux ou macOS:

```bash
./.venv/bin/python experimentos/experimento-3.py
```

O script salva `resultados/experimento3_sessoes.csv` com saldo final, número de rodadas, resultado e ocorrência de esgotamento de cada participante; `resultados/experimento3_resumo.csv` com proporções de ganho, empate, perda e esgotamento, além da média e mediana dos saldos finais; e `graficos/experimento3_trajetorias.png` com as trajetórias dos cinco primeiros participantes. Depois que uma sessão termina, sua linha permanece no último saldo até a rodada 500. As proporções de ganho, empate e perda somam 100%; o esgotamento é contado entre as perdas.

O gerador do Python permite reproduzir os resultados deste script com a mesma versão de Python. Ele pode gerar uma sequência diferente da macro em Excel/LibreOffice, mesmo com a semente 42.

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

Para executar um experimento diretamente, substitua `maquina_estatistica.py` por `experimentos/experimento-1.py`, `experimentos/experimento-2.py`, `experimentos/experimento-3.py`, `experimentos/experimento-4.py` ou `experimentos/experimento-5.py` nesses comandos.

Se aparecer `ModuleNotFoundError`, instale o `requirements.txt` usando o mesmo Python que abre o menu. Para verificar conflitos na instalação, execute `.\.venv\Scripts\python.exe -m pip check` no Windows ou `./.venv/bin/python -m pip check` no Linux/macOS.

## Uso de IA

O método salvar_historico foi implementado com auxílio da IA. 

As exportações dos resultados dos experimentos para arquivos csv também.

Ao final de cada experimento.py tem um fragmento de codigo responsável por gerar os gráficos utilizados. Esse código foi feito com o auxílio de IA. 

Também utilizamos para correções gramaticais e ortográficas no relatório.

Isso não significa que foi "vibecodado". Na verdade, todo prompt e código gerado foi revisado e avaliado pelo grupo.
