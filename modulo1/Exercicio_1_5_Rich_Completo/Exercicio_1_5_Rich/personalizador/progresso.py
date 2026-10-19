from time import sleep

from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.text import Text

from . import obter_texto


def por_palavras(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    palavras = conteudo.split()
    console = Console()
    with Progress(TextColumn("Palavras"), BarColumn(), TaskProgressColumn(), console=console) as barra:
        tarefa = barra.add_task("Palavras", total=max(len(palavras), 1))
        for palavra in palavras:
            sleep(min(0.05, 0.6 / max(len(palavras), 1)))
            barra.advance(tarefa)
        if not palavras:
            barra.advance(tarefa)
    console.print(Text(conteudo))


def por_linhas(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    linhas = conteudo.splitlines() or [""]
    console = Console()
    with Progress(TextColumn("Linhas"), BarColumn(), TaskProgressColumn(), console=console) as barra:
        tarefa = barra.add_task("Linhas", total=len(linhas))
        for linha in linhas:
            sleep(min(0.08, 0.6 / len(linhas)))
            barra.advance(tarefa)
    console.print(Text(conteudo))
