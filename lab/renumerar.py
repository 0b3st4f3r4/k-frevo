#!/usr/bin/env python3
r"""A renumeracao: abrir a casa para um capitulo novo, numa passada so.

O numero do arquivo E a posicao do capitulo na ordem de leitura, e isso e conferido por portao:
inserir no meio obriga a deslocar todos os posteriores. A operacao toca quatro lugares, e cada um ja
se mostrou capaz de ficar pela metade --- os arquivos, os `\input` do `livro.tex` (metade deles com
`.tex` e metade sem), os comentarios `% O capitulo N` do mesmo arquivo (que usam UM digito abaixo de
dez), e as colunas `aterrou` e `exemplo` do registro do aterramento.

Sem `--aplicar` ele nao escreve nada: imprime o que faria. Com `--aplicar`, confere tudo antes de
tocar em qualquer arquivo e so entao anda. `--conferir` responde se a arvore esta consistente.

    lab/renumerar.py --inserir 09            # ensaio
    lab/renumerar.py --inserir 09 --aplicar  # abre a casa
    lab/renumerar.py --conferir
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CAPITULOS = RAIZ / "livro" / "capitulos"
LIVRO = RAIZ / "livro" / "livro.tex"
REGISTRO = RAIZ / "dados" / "aterramento.tsv"
COLUNAS = (4, 6)


def arquivos() -> list:
    return sorted(CAPITULOS.glob("[0-9][0-9]_*.tex"))


def numeros() -> list:
    return [int(f.name[:2]) for f in arquivos()]


def conferir(esperando: int = None) -> list:
    """O estado da arvore. `esperando` e a posicao deixada aberta para o capitulo novo."""
    problemas = []
    ns = numeros()
    if esperando is None:
        esperado = list(range(1, len(ns) + 1))
    else:
        esperado = [n for n in range(1, len(ns) + 2) if n != esperando]
    if ns != esperado:
        problemas.append("os numeros dos arquivos nao sao %s: %s" % (esperado, ns))
    texto = LIVRO.read_text(encoding="utf-8")
    for f in arquivos():
        nome = f.name[:-4]
        if ("\\input{capitulos/%s}" % nome) not in texto and ("\\input{capitulos/%s.tex}" % nome) not in texto:
            problemas.append("livro.tex nao aponta para %s" % nome)
    for m in re.finditer(re.escape("\\input{capitulos/") + r"([0-9]{2})_", texto):
        if int(m.group(1)) not in ns:
            problemas.append("livro.tex aponta para o capitulo %s, que nao existe" % m.group(1))
    for m in re.finditer(r"^% O cap[ií]tulo ([0-9]+) ", texto, re.M):
        if int(m.group(1)) not in ns:
            problemas.append("comentario para o capitulo %s, que nao existe" % m.group(1))
    return problemas


def deslocamento(inserir: int) -> list:
    ns = numeros()
    if inserir < 1 or inserir > len(ns) + 1:
        raise SystemExit("ABORTA: a posicao %d nao existe (ha %d capitulos)" % (inserir, len(ns)))
    return [f for f in arquivos() if int(f.name[:2]) >= inserir]


def ensaio(inserir: int) -> None:
    movem = deslocamento(inserir)
    texto = LIVRO.read_text(encoding="utf-8")
    print("inserir o capitulo novo na posicao %02d" % inserir)
    print("  arquivos que andam uma casa: %d" % len(movem))
    sem_input = []
    for f in movem:
        velho, novo = f.name[:-4], "%02d%s" % (int(f.name[:2]) + 1, f.name[2:-4])
        achou = any(("\\input{capitulos/%s%s}" % (velho, s)) in texto for s in ("", ".tex"))
        if not achou:
            sem_input.append(velho)
        print("    %s -> %s%s" % (velho, novo, "" if achou else "   <<< SEM INPUT"))
    if sem_input:
        raise SystemExit("ABORTA: %d arquivos sem input: %s" % (len(sem_input), sem_input))
    linhas = REGISTRO.read_text(encoding="utf-8").split(chr(10))
    n = 0
    for linha in linhas:
        if linha.startswith("#") or not linha.strip():
            continue
        c = linha.split(chr(9))
        if len(c) < 7:
            continue
        n += sum(1 for col in COLUNAS if c[col].strip().isdigit() and int(c[col]) >= inserir)
    print("  numeros do registro a deslocar: %d" % n)
    print("  comentarios no livro.tex: %d (os de numero >= %d andam)"
          % (len(re.findall(r"^% O cap[ií]tulo ([0-9]+) ", texto, re.M)), inserir))
    print("  o capitulo novo ocupa a posicao %02d, com o input antes do %02d_" % (inserir, inserir + 1))


def aplicar(inserir: int) -> None:
    movem = deslocamento(inserir)
    texto = LIVRO.read_text(encoding="utf-8")
    for f in reversed(movem):
        novo = CAPITULOS / ("%02d%s" % (int(f.name[:2]) + 1, f.name[2:]))
        if novo.exists():
            raise SystemExit("ABORTA: %s ja existe" % novo.name)
        subprocess.run(["git", "mv", str(f), str(novo)], cwd=RAIZ, check=True)
    print("  %d arquivos deslocados" % len(movem))
    for f in movem:
        velho, novo = f.name[:-4], "%02d%s" % (int(f.name[:2]) + 1, f.name[2:-4])
        for s in ("", ".tex"):
            texto = texto.replace("\\input{capitulos/%s%s}" % (velho, s), "\\input{capitulos/%s%s}" % (novo, s))
    # Os comentários sobem em UMA passada, com callback que só sobe o número a partir da
    # posição de inserção. Em laço ascendente, cada passada re-casava o que a anterior
    # acabou de escrever ("% O capítulo 11" virava 12, depois 13, ... até 27) --- o segundo
    # defeito que a produção da posição 10 achou; a passada única não tem com quem cascatear.
    def _sobe_comentario(m):
        return "%s%02d " % (m.group(1), int(m.group(2)) + 1) if int(m.group(2)) >= inserir else m.group(0)
    texto = re.sub(r"^(% O cap[ií]tulo )(\d+) ", _sobe_comentario, texto, flags=re.M)
    LIVRO.write_text(texto, encoding="utf-8")
    print("  livro.tex: inputs e comentarios")
    linhas = REGISTRO.read_text(encoding="utf-8").split(chr(10))
    mudados = 0
    for i, linha in enumerate(linhas):
        if linha.startswith("#") or not linha.strip():
            continue
        c = linha.split(chr(9))
        if len(c) < 7:
            continue
        for col in COLUNAS:
            if c[col].strip().isdigit() and int(c[col]) >= inserir:
                c[col] = str(int(c[col]) + 1)
                mudados += 1
        linhas[i] = chr(9).join(c)
    REGISTRO.write_text(chr(10).join(linhas), encoding="utf-8")
    print("  registro: %d numeros deslocados" % mudados)
    problemas = conferir(esperando=inserir)
    if problemas:
        for p in problemas:
            print("   - %s" % p)
        raise SystemExit(1)
    print("  conferencia limpa: a casa esta aberta, e a %02d espera o capitulo novo" % inserir)


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description="abre a casa para um capitulo novo")
    ap.add_argument("--inserir", type=int)
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--conferir", action="store_true")
    args = ap.parse_args(argv)
    if args.conferir or not args.inserir:
        problemas = conferir()
        for p in problemas:
            print("  - %s" % p)
        print("conferencia: %s" % ("limpa" if not problemas else "%d problema(s)" % len(problemas)))
        return 1 if problemas else 0
    if args.aplicar:
        aplicar(args.inserir)
    else:
        ensaio(args.inserir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
