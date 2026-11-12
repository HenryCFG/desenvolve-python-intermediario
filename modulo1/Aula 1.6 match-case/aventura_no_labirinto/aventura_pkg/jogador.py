"""Controla estado, pontuação, movimentos e leitura de teclado com pynput."""

from dataclasses import dataclass
from queue import Queue

from .labirinto import DIRECOES, Labirinto, Posicao


@dataclass
class Jogador:
    """Mantém nome, posição, pontos, movimentos e quantidade de tesouros."""

    nome: str
    posicao: Posicao
    pontos: int = 100
    movimentos: int = 0
    coletados: int = 0


def iniciar_jogador(nome: str, labirinto: Labirinto) -> Jogador:
    """Cria o jogador na entrada com cem pontos e nenhum movimento."""
    return Jogador(nome, labirinto.inicio)


def pontuar(jogador: Jogador, evento: str) -> None:
    """Aplica -1 por passo, -2 por parede, +25 por tesouro e +100 por vitória.

    A pontuação nunca é negativa e não determina o fim da partida.
    """
    valores = {"passo": -1, "parede": -2, "tesouro": 25, "vitoria": 100}
    jogador.pontos = max(0, jogador.pontos + valores[evento])


def mover(jogador: Jogador, labirinto: Labirinto, comando: str) -> str:
    """Aplica um comando e retorna ignorado, parede, passo, tesouro ou vitoria.

    Somente movimentos válidos consomem o limite; a vitória pontua uma vez.
    """
    if comando not in DIRECOES or jogador.posicao == labirinto.saida:
        return "ignorado"
    dl, dc = DIRECOES[comando]
    destino = (jogador.posicao[0] + dl, jogador.posicao[1] + dc)
    if not labirinto.livre(destino):
        pontuar(jogador, "parede")
        return "parede"
    jogador.posicao = destino
    jogador.movimentos += 1
    pontuar(jogador, "passo")
    evento = "passo"
    if destino in labirinto.tesouros:
        labirinto.tesouros.remove(destino)
        jogador.coletados += 1
        pontuar(jogador, "tesouro")
        evento = "tesouro"
    if destino == labirinto.saida:
        pontuar(jogador, "vitoria")
        evento = "vitoria"
    return evento


def iniciar_teclado(fila: Queue):
    """Inicia um Listener pynput que envia WASD, setas e Q/Esc à fila.

    O chamador deve parar o listener em finally. Não bloqueia teclas do sistema.
    A importação tardia permite executar a demonstração sem servidor gráfico.
    """
    from pynput import keyboard

    mapa = {keyboard.Key.up: "w", keyboard.Key.down: "s",
            keyboard.Key.left: "a", keyboard.Key.right: "d",
            keyboard.Key.esc: "q"}

    def ao_pressionar(tecla):
        """Traduz teclas reconhecidas sem desenhar na thread do listener."""
        comando = mapa.get(tecla, getattr(tecla, "char", ""))
        comando = (comando or "").lower()
        if comando in (*DIRECOES, "q"):
            fila.put(comando)

    listener = keyboard.Listener(on_press=ao_pressionar)
    listener.start()
    listener.wait()
    return listener
