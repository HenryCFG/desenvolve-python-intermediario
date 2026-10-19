import argparse

from personalizador import estilo, layout, painel, progresso


MODULOS = {
    "layout": {"1": layout.centralizado, "centralizado": layout.centralizado,
               "2": layout.colunas, "colunas": layout.colunas},
    "painel": {"1": painel.simples, "simples": painel.simples,
               "2": painel.duplo, "duplo": painel.duplo},
    "progresso": {"1": progresso.por_palavras, "por_palavras": progresso.por_palavras,
                 "2": progresso.por_linhas, "por_linhas": progresso.por_linhas},
    "estilo": {"1": estilo.destaque, "destaque": estilo.destaque,
               "2": estilo.alternado, "alternado": estilo.alternado},
}


IDS_MODULOS = {"1": "layout", "2": "painel", "3": "progresso", "4": "estilo"}


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Personaliza textos usando a biblioteca Rich.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("texto", help="Texto a formatar ou caminho do arquivo de texto.")
    parser.add_argument("-a", "--arquivo", action="store_true",
                        help="Interpreta o argumento texto como um caminho de arquivo UTF-8.")
    parser.add_argument("-m", "--modulo", default="layout",
                        help="Módulo por nome ou ID: 1=layout, 2=painel, 3=progresso, 4=estilo.\n"
                             "Padrão: layout.")
    parser.add_argument("-f", "--funcao", default="1",
                        help="Função por nome ou ID dentro do módulo:\n"
                             "layout: 1=centralizado, 2=colunas\n"
                             "painel: 1=simples, 2=duplo\n"
                             "progresso: 1=por_palavras, 2=por_linhas\n"
                             "estilo: 1=destaque, 2=alternado\n"
                             "Padrão: 1.")
    return parser


def main() -> None:
    parser = criar_parser()
    args = parser.parse_args()
    nome_modulo = IDS_MODULOS.get(args.modulo.lower(), args.modulo.lower())
    if nome_modulo not in MODULOS:
        parser.error("Módulo inválido. Use layout, painel, progresso, estilo ou IDs de 1 a 4.")
    funcao = MODULOS[nome_modulo].get(args.funcao.lower())
    if funcao is None:
        parser.error(f"Função inválida para {nome_modulo}. Consulte python main.py -h.")
    try:
        funcao(args.texto, args.arquivo)
    except (OSError, UnicodeError) as erro:
        parser.error(f"Não foi possível ler o arquivo: {erro}")


if __name__ == "__main__":
    main()
