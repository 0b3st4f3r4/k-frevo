"""Gráficos: o que o caderno precisa para gravar figura nos dois formatos."""
from pathlib import Path

DESTINO = Path("livro/figuras")

__all__ = ["DESTINO", "salvar"]


def salvar(fig, identificador: str, indice: int = 1,
           destino: Path = DESTINO) -> list:
    r"""Grava a figura em \emph{pdf} (para o livro) e em \emph{png} (para ser olhada).

    Os dois formatos não são duplicação: o pdf é vetorial e entra no livro sem borrar; o png
    é raster e é o que um agente com entrada de imagem abre para dizer o que a figura
    mostra (AGENTS.md §9). Devolve os caminhos gravados, na ordem.
    """
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    caminhos = []
    for sufixo in ("pdf", "png"):
        caminho = destino / ("%s_%d.%s" % (identificador, indice, sufixo))
        fig.savefig(caminho, dpi=150)
        caminhos.append(caminho)
    return caminhos
