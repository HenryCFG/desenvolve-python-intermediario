from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import obter_texto


def simples(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    Console().print(Panel(Text(conteudo), title="Painel simples", border_style="blue"))


def duplo(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    Console().print(Panel(Text(conteudo), title="Painel duplo", box=box.DOUBLE, border_style="green"))
