from pathlib import Path


def obter_texto(texto: str, isArquivo: bool) -> str:
    if isArquivo:
        return Path(texto).read_text(encoding="utf-8")
    return texto
