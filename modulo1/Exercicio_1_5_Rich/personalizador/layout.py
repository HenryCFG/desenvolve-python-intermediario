from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import obter_texto


def centralizado(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    console = Console()
    console.print(Align.center(Panel(Text(conteudo), title="Texto centralizado", expand=False)))


def colunas(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    partes = conteudo.splitlines()
    if len(partes) <= 1:
        palavras = conteudo.split()
        metade = max(1, (len(palavras) + 1) // 2)
        partes = [" ".join(palavras[:metade]), " ".join(palavras[metade:])]
    partes = [parte for parte in partes if parte]
    if not partes:
        partes = [""]
    itens = [Panel(Text(parte), border_style="cyan") for parte in partes]
    Console().print(Columns(itens, equal=True, expand=True))
