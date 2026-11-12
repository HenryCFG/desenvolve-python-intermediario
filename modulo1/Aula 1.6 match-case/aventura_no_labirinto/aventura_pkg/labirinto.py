"""Gera labirintos aleatórios conectados e os apresenta com Rich."""

from dataclasses import dataclass
from random import Random

from rich.panel import Panel
from rich.text import Text

Posicao = tuple[int, int]
DIRECOES = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
TAMANHOS = {"facil": 9, "medio": 15, "dificil": 21}


@dataclass
class Labirinto:
    """Guarda a matriz de paredes, entrada, saída e tesouros restantes."""

    grade: list[list[str]]
    inicio: Posicao
    saida: Posicao
    tesouros: set[Posicao]

    def livre(self, posicao: Posicao) -> bool:
        """Indica se a posição está dentro do mapa e pode ser atravessada."""
        linha, coluna = posicao
        return (0 <= linha < len(self.grade)
                and 0 <= coluna < len(self.grade[linha])
                and self.grade[linha][coluna] != "#")


def criar_labirinto(dificuldade: str = "facil", seed: int | None = None) -> Labirinto:
    """Escava corredores por busca em profundidade com pilha e sorteia tesouros.

    A semente permite repetir um mapa. Todos os corredores ficam conectados;
    a entrada e a saída nunca recebem tesouros. Não usa mapas pré-escritos.
    """
    if dificuldade not in TAMANHOS:
        raise ValueError("Dificuldade deve ser facil, medio ou dificil.")
    rng = Random(seed)
    tamanho = TAMANHOS[dificuldade]
    grade = [["#"] * tamanho for _ in range(tamanho)]
    inicio, saida = (1, 1), (tamanho - 2, tamanho - 2)
    grade[1][1] = " "
    pilha = [inicio]
    while pilha:
        linha, coluna = pilha[-1]
        vizinhos = [(linha + 2 * dl, coluna + 2 * dc)
                    for dl, dc in DIRECOES.values()
                    if 0 < linha + 2 * dl < tamanho - 1
                    and 0 < coluna + 2 * dc < tamanho - 1
                    and grade[linha + 2 * dl][coluna + 2 * dc] == "#"]
        if not vizinhos:
            pilha.pop()
            continue
        nl, nc = rng.choice(vizinhos)
        grade[(linha + nl) // 2][(coluna + nc) // 2] = " "
        grade[nl][nc] = " "
        pilha.append((nl, nc))
    candidatos = [(l, c) for l in range(tamanho) for c in range(tamanho)
                  if grade[l][c] == " " and (l, c) not in (inicio, saida)]
    return Labirinto(grade, inicio, saida, set(rng.sample(candidatos, tamanho // 3)))


def resolver_labirinto(labirinto: Labirinto, inicio: Posicao | None = None) -> list[str] | None:
    """Retorna comandos WASD até a saída usando busca RECURSIVA com retrocesso.

    Retorna None se não existir caminho e [] se já estiver na saída.
    A solução prioriza chegar à saída; não busca todos os tesouros.
    """
    visitados: set[Posicao] = set()

    def buscar(posicao: Posicao) -> list[str] | None:
        """Explora uma posição e visita recursivamente os vizinhos livres."""
        if not labirinto.livre(posicao) or posicao in visitados:
            return None
        if posicao == labirinto.saida:
            return []
        visitados.add(posicao)
        for comando, (dl, dc) in DIRECOES.items():
            caminho = buscar((posicao[0] + dl, posicao[1] + dc))
            if caminho is not None:
                return [comando] + caminho
        return None

    return buscar(labirinto.inicio if inicio is None else inicio)


def imprimir_labirinto(labirinto: Labirinto, posicao: Posicao, cor: str = "cyan") -> Panel:
    """Monta um painel Rich do mapa, com jogador, saída e tesouros distintos."""
    desenho = Text()
    for l, linha in enumerate(labirinto.grade):
        for c, celula in enumerate(linha):
            ponto = (l, c)
            if ponto == posicao:
                desenho.append("@ ", f"bold {cor}")
            elif ponto == labirinto.saida:
                desenho.append("S ", "bold green")
            elif ponto in labirinto.tesouros:
                desenho.append("* ", "bold yellow")
            elif celula == "#":
                desenho.append("██", "bright_black")
            else:
                desenho.append("  ")
        desenho.append("\n" if l < len(labirinto.grade) - 1 else "")
    return Panel(desenho, title="AVENTURA NO LABIRINTO", border_style=cor, expand=False)
