"""Vendas da Morabeza em Python idiomático (Sessão 2).

Cada venda passa a ser um objeto Venda (dataclass) em vez de um dicionário.
Linhas com erros levantam VendaInvalida e são postas de parte na leitura.
"""
from __future__ import annotations

import csv
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date

ILHAS_SERVIDAS = {"Santiago", "São Vicente", "Sal", "Boa Vista", "Fogo", "Santo Antão"}


class VendaInvalida(Exception):
    """Uma linha do ficheiro de vendas não pode ser transformada numa Venda."""


@dataclass(frozen=True)
class Venda:
    venda_id: str
    data: date
    cliente_id: str
    ilha: str
    categoria: str
    quantidade: int
    preco_unitario: int

    @property
    def total(self) -> int:
        return self.quantidade * self.preco_unitario



def criar_venda(linha: dict[str, str]) -> Venda:
    """Converte uma linha do CSV numa venda válida."""

    try:
        quantidade = int(linha["quantidade"])
        preco = int(linha["preco_unitario"])
        data_venda = date.fromisoformat(linha["data"])

    except ValueError as erro:
        raise VendaInvalida(
            f"{linha['venda_id']}: valor impossível"
        ) from erro

    if quantidade <= 0:
        raise VendaInvalida("Quantidade inválida")

    if preco <= 0:
        raise VendaInvalida("Preço inválido")

    if linha["ilha"] not in ILHAS_SERVIDAS:
        raise VendaInvalida("Ilha não servida")

    return Venda(
        venda_id=linha["venda_id"],
        data=data_venda,
        cliente_id=linha["cliente_id"],
        ilha=linha["ilha"],
        categoria=linha["categoria"],
        quantidade=quantidade,
        preco_unitario=preco
    )


def ler_vendas(caminho: str):
    with open(caminho, encoding="utf-8") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            try:
                yield criar_venda(linha)

            except VendaInvalida:
                continue


def contar_invalidas(caminho: str) -> int:
    contador = 0

    with open(caminho, encoding="utf-8") as ficheiro:
        for linha in csv.DictReader(ficheiro):
            try:
                criar_venda(linha)

            except VendaInvalida:
                contador += 1

    return contador



def vendas_acima(vendas: Iterable[Venda], limite: int) -> list[Venda]:
    return [venda for venda in vendas if venda.total > limite]


def total_por(vendas, chave):
    totais = {}

    for venda in vendas:
        grupo = chave(venda)
        totais[grupo] = totais.get(grupo, 0) + venda.total

    return totais


# ---------------------------------------------------------------- Extensão (opcional)

def top_n(totais: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Os n pares (chave, total) com maior total, do maior para o menor."""
    # EXTENSÃO: sorted(totais.items(), key=lambda par: ..., reverse=True) e depois [:n]
    raise NotImplementedError("Extensão por fazer")


@contextmanager
def cronometro(nome: str):
    """Mede o tempo de um bloco. Uso: with cronometro("leitura"): ..."""
    # EXTENSÃO: guarda time.perf_counter() antes do yield e, num finally,
    #           imprime f"{nome}: {segundos:.3f} s".
    raise NotImplementedError("Extensão por fazer")
    yield
