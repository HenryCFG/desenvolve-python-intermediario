# Aventura no Labirinto

Trabalho Prático I — Python II / Projeto Desenvolve.
Um jogo de terminal em que você explora um labirinto gerado aleatoriamente,
coleta tesouros e encontra a saída. Inclui uma demonstração que resolve o
mapa por uma função recursiva de busca em profundidade com retrocesso.

![Tela do jogo, renderizada a partir da execução real](docs/jogo.svg)

![Tela de vitória da demonstração](docs/vitoria.svg)

## Instalação e execução

Requer **Python 3.10 ou superior** (usa `match-case`). Descompacte o projeto,
abra um terminal na pasta que contém `main.py` e crie seu ambiente virtual:

```powershell
# Windows / PowerShell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --name Ana
```

```bash
# Linux / macOS
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py --name Ana
```

Não é necessário ativar o ambiente: os comandos acima usam seu interpretador
diretamente. O `requirements.txt` foi exportado com `pip freeze` do ambiente
utilizado no desenvolvimento em Windows. Dependências específicas de outros
sistemas são resolvidas pelo próprio `pynput` durante a instalação.

Exemplos (use o Python do ambiente virtual):

```bash
python main.py --name "Maria Silva" --color magenta --dificuldade medio --seed 42
python main.py --name Ana --demo --velocidade 0.08
python main.py --name Ana --teclado linha --max-movimentos 200
python main.py --help
```

## Como jogar

O menu oferece **1: instruções**, **2: jogar**, **3: assistir à solução
recursiva** e **0: sair**. Após cada partida, você volta ao menu.

| Símbolo ou controle | Significado |
| --- | --- |
| `@` | Jogador |
| `S` | Saída |
| `*` | Tesouro opcional |
| Bloco cinza | Parede |
| W / A / S / D ou setas | Cima / esquerda / baixo / direita |
| Q / Esc | Abandonar a partida |
| Ctrl+C | Encerrar o programa, inclusive a demonstração |

Mantenha o terminal em foco. O listener `pynput` funciona somente durante
a partida manual e é encerrado ao sair dela. A biblioteca monitora eventos
do teclado do sistema; não bloqueia as teclas de outros aplicativos.

Você começa com **100 pontos**. Um passo custa 1, bater na parede custa 2,
um tesouro rende 25 e a vitória rende 100. A pontuação não fica negativa.
Você vence ao chegar à saída e perde ao abandonar ou atingir o limite de
passos válidos. Colisões não consomem passos. Tesouros não são obrigatórios.
A solução automática busca a saída, sem otimizar pontuação ou tesouros.

## Opções da CLI

| Opção | Padrão | Uso |
| --- | --- | --- |
| `--name NOME` | Obrigatória | Nome visível do jogador |
| `--color COR` | cyan | cyan, green, magenta, yellow ou blue |
| `--dificuldade NIVEL` | facil | facil (9×9), medio (15×15), dificil (21×21) |
| `--seed NUMERO` | Aleatória | Repete o mesmo mapa e tesouros |
| `--max-movimentos N` | 500 | Limite positivo de passos válidos |
| `--velocidade SEGUNDOS` | 0.12 | Intervalo de 0 a 2 segundos na solução |
| `--teclado MODO` | pynput | pynput ou linha (com Enter) |
| `--demo` | Desligado | Inicia a solução sem abrir o menu |
| `--help` | — | Exibe ajuda |

## Estrutura e requisitos do trabalho

```text
aventura_no_labirinto/
├── aventura_pkg/
│   ├── __init__.py
│   ├── labirinto.py
│   ├── jogador.py
│   ├── utils.py
│   └── instrucoes.md
├── docs/
│   ├── jogo.svg
│   └── vitoria.svg
├── tests/
│   └── test_jogo.py
├── main.py
├── gerar_documentacao.py
├── requirements.txt
├── aventura_pkg.html
└── README.md
```

| Requisito | Implementação |
| --- | --- |
| Função recursiva | `resolver_labirinto()` → função interna `buscar()` |
| match-case | Seleção do menu em `main.py` |
| Bibliotecas externas | Rich (interface) e pynput (teclado) |
| Labirinto sem mapa pré-escrito | Geração aleatória por escavação com pilha em `criar_labirinto()` |
| Modularização | `labirinto.py`, `jogador.py`, `utils.py` |
| Docstrings e HTML | Todos os módulos/funções documentados; `aventura_pkg.html` contém o pacote e seus módulos |
| CLI com opção obrigatória | Nome obrigatório e oito opções adicionais, incluindo ajuda |
| Duas funções utilitárias | Instruções de arquivo, menu, tela de jogo e resultado |

## Testes e documentação

Dentro da pasta do projeto, execute com o Python do ambiente virtual:

```bash
python -m unittest discover -s tests -v
python gerar_documentacao.py
python -m pip freeze > requirements.txt
```

Abra `aventura_pkg.html` no navegador para consultar as docstrings exportadas
com `pydoc`, sem precisar instalar um gerador de documentação.

## Compatibilidade do teclado

O `pynput` exige uma sessão gráfica compatível. Em Linux, normalmente precisa
de X e `DISPLAY`; ambientes Wayland podem restringir a captura. Em macOS,
o terminal pode precisar de permissão de Acessibilidade/Monitoramento de Entrada.
Em servidores, notebooks e terminais sem suporte, use `--teclado linha`;
digite uma letra WASD ou Q por vez, seguida de Enter. `--demo` não importa
nem inicia o `pynput`. Não há dependência de áudio.

Referências das bibliotecas: [Rich](https://rich.readthedocs.io/) e
[pynput](https://pynput.readthedocs.io/en/latest/keyboard.html).
