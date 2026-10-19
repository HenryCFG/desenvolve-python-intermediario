from rich.console import Console
from rich.text import Text

from . import obter_texto


def destaque(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    Console().print(Text(conteudo, style="bold underline magenta"))


def alternado(texto: str, isArquivo: bool = False) -> None:
    conteudo = obter_texto(texto, isArquivo)
    resultado = Text(conteudo)
    posicao = 0
    indice = 0
    for parte in conteudo.split():
        posicao = conteudo.find(parte, posicao)
        cor = "bright_cyan" if indice % 2 == 0 else "bright_yellow"
        resultado.stylize(cor, posicao, posicao + len(parte))
        posicao += len(parte)
        indice += 1
    Console().print(resultado)
