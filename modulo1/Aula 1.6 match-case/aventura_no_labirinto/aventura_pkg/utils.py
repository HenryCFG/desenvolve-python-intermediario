"""Formata menus, instruções de arquivo, placar e resultado da partida."""

from pathlib import Path

from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from .jogador import Jogador
from .labirinto import Labirinto, imprimir_labirinto


def imprime_instrucoes(console) -> None:
    """Lê o arquivo de instruções junto ao pacote e imprime Markdown com Rich."""
    arquivo = Path(__file__).with_name("instrucoes.md")
    console.print(Panel(Markdown(arquivo.read_text(encoding="utf-8")), title="Como jogar"))


def imprimir_menu(console, nome: str, cor: str) -> None:
    """Mostra opções que serão tratadas por match-case no programa principal."""
    texto = Text(f"Olá, {nome}!\n\n1  Instruções\n2  Jogar\n3  Assistir à solução recursiva\n0  Sair")
    console.print(Panel(texto, title="AVENTURA NO LABIRINTO", border_style=cor))


def montar_tela(labirinto: Labirinto, jogador: Jogador, cor: str,
                limite: int, mensagem: str = "") -> Group:
    """Combina mapa, placar e legenda sem interpretar o nome como markup."""
    placar = Text(f"{jogador.nome}  |  Pontos: {jogador.pontos}  |  "
                  f"Passos: {jogador.movimentos}/{limite}  |  Tesouros: {jogador.coletados}")
    return Group(imprimir_labirinto(labirinto, jogador.posicao, cor), placar,
                 Text("@ você   S saída   * tesouro   WASD/setas mover   Q/Esc sair"),
                 Text(mensagem, style=cor))


def imprimir_resultado(console, jogador: Jogador, venceu: bool, motivo: str) -> None:
    """Apresenta vitória ou derrota e despede-se do jogador com seu placar."""
    titulo = "VITÓRIA!" if venceu else "FIM DE JOGO"
    texto = Text(f"{jogador.nome}, {motivo}\nPontos: {jogador.pontos} | "
                 f"Passos: {jogador.movimentos} | Tesouros: {jogador.coletados}\n"
                 "Até a próxima aventura!")
    console.print(Panel(texto, title=titulo, border_style="green" if venceu else "red"))
