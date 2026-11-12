"""CLI do jogo Aventura no Labirinto. Execute com Python 3.10 ou superior."""

import argparse
from queue import Empty, Queue
from time import sleep

from rich.console import Console
from rich.live import Live

from aventura_pkg.jogador import iniciar_jogador, iniciar_teclado, mover
from aventura_pkg.labirinto import criar_labirinto, resolver_labirinto
from aventura_pkg.utils import (imprime_instrucoes, imprimir_menu,
                                imprimir_resultado, montar_tela)


def inteiro_positivo(valor: str) -> int:
    """Valida argumentos inteiros estritamente positivos."""
    numero = int(valor)
    if numero <= 0:
        raise argparse.ArgumentTypeError("informe um inteiro maior que zero")
    return numero


def atraso_valido(valor: str) -> float:
    """Aceita um intervalo finito de zero a dois segundos entre passos."""
    numero = float(valor)
    if not 0 <= numero <= 2:
        raise argparse.ArgumentTypeError("informe um número entre 0 e 2")
    return numero


def criar_parser() -> argparse.ArgumentParser:
    """Define a CLI com nome obrigatório, ajuda em português e oito opções."""
    parser = argparse.ArgumentParser(description="Explore mapas aleatórios e encontre a saída!",
                                     epilog="Exemplo: python main.py --name Ana --dificuldade medio --seed 42")
    parser.add_argument("--name", required=True, help="nome do jogador (obrigatório)")
    parser.add_argument("--color", choices=["cyan", "green", "magenta", "yellow", "blue"], default="cyan", help="cor principal")
    parser.add_argument("--dificuldade", choices=["facil", "medio", "dificil"], default="facil", help="mapas 9x9, 15x15 ou 21x21")
    parser.add_argument("--seed", type=int, help="semente para repetir o mapa")
    parser.add_argument("--max-movimentos", type=inteiro_positivo, default=500, help="limite de passos válidos (padrão: 500)")
    parser.add_argument("--velocidade", type=atraso_valido, default=0.12, help="segundos entre passos automáticos: 0 a 2")
    parser.add_argument("--teclado", choices=["pynput", "linha"], default="pynput", help="pynput ou comandos seguidos de Enter")
    parser.add_argument("--demo", action="store_true", help="executa a solução automática sem abrir o menu")
    return parser


def jogar(args: argparse.Namespace, console: Console, automatico: bool = False) -> bool:
    """Executa uma partida e encerra a captura de teclado mesmo após erro."""
    mapa = criar_labirinto(args.dificuldade, args.seed)
    jogador = iniciar_jogador(args.name, mapa)
    caminho = resolver_labirinto(mapa) if automatico else None
    if automatico and caminho is None:
        raise RuntimeError("Não foi encontrada solução para o mapa.")
    fila = Queue()
    listener = None
    mensagem = "Demonstração recursiva — Ctrl+C encerra" if automatico else "Encontre a saída!"
    motivo = "você atingiu o limite de movimentos."
    try:
        if not automatico and args.teclado == "pynput":
            try:
                listener = iniciar_teclado(fila)
            except Exception as erro:
                console.print(texto_erro(erro))
                return False
        with Live(montar_tela(mapa, jogador, args.color, args.max_movimentos, mensagem),
                  console=console, auto_refresh=False) as tela:
            while jogador.movimentos < args.max_movimentos:
                if automatico:
                    comando = caminho[jogador.movimentos]
                    sleep(args.velocidade)
                elif args.teclado == "linha":
                    comando = console.input("Comando (W/A/S/D/Q) + Enter: ").strip().lower()
                else:
                    try:
                        comando = fila.get(timeout=0.1)
                    except Empty:
                        if not listener.is_alive():
                            raise RuntimeError("Captura de teclado interrompida; tente --teclado linha.")
                        continue
                if comando == "q":
                    motivo = "você abandonou a partida."
                    break
                evento = mover(jogador, mapa, comando)
                mensagens = {"parede": "Uma parede bloqueou seu caminho. -2 pontos.",
                             "tesouro": "Tesouro coletado! +25 pontos.",
                             "ignorado": "Use W, A, S, D ou Q.", "passo": "Continue explorando!",
                             "vitoria": "Você encontrou a saída!"}
                tela.update(montar_tela(mapa, jogador, args.color, args.max_movimentos,
                                        mensagens[evento]), refresh=True)
                if jogador.posicao == mapa.saida:
                    motivo = "você encontrou a saída!"
                    break
    finally:
        if listener is not None:
            listener.stop()
            listener.join(timeout=1)
    venceu = jogador.posicao == mapa.saida
    console.print()
    imprimir_resultado(console, jogador, venceu, motivo)
    return venceu


def texto_erro(erro: Exception):
    """Cria mensagem de erro segura com alternativa para captura indisponível."""
    from rich.text import Text
    return Text(f"Não foi possível iniciar o teclado: {erro}\n"
                "Tente executar com --teclado linha.", style="red")


def main(argv: list[str] | None = None) -> int:
    """Valida os argumentos, apresenta o menu match-case e trata interrupções."""
    parser = criar_parser()
    args = parser.parse_args(argv)
    args.name = args.name.strip()
    if not args.name or not args.name.isprintable():
        parser.error("--name deve conter um nome visível, sem caracteres de controle")
    console = Console()
    try:
        if args.demo:
            jogar(args, console, automatico=True)
            return 0
        while True:
            imprimir_menu(console, args.name, args.color)
            match console.input("Escolha uma opção: ").strip():
                case "1":
                    imprime_instrucoes(console)
                case "2":
                    jogar(args, console)
                case "3":
                    jogar(args, console, automatico=True)
                case "0":
                    console.print("Até a próxima aventura!")
                    return 0
                case _:
                    console.print("Opção inválida. Escolha 0, 1, 2 ou 3.")
    except (KeyboardInterrupt, EOFError):
        console.print("\nPartida encerrada. Até a próxima aventura!")
        return 0
    except RuntimeError as erro:
        console.print(texto_erro(erro))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
