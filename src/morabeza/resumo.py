"""Resumo das vendas da Morabeza Distribuição (Sessão 1).

Lê um ficheiro CSV de vendas e mostra a faturação total e por ilha.
Só usa a biblioteca padrão do Python: o pandas chega na Sessão 4.
"""
import csv
import sys



def ler_vendas(caminho: str) -> list[dict]:
    """Lê o CSV e devolve uma lista de vendas."""

    vendas = []

    with open(caminho, encoding="utf-8") as ficheiro:
        leitor = csv.DictReader(ficheiro)

        for linha in leitor:
            linha["quantidade"] = int(linha["quantidade"])
            linha["preco_unitario"] = int(linha["preco_unitario"])

            vendas.append(linha)

    return vendas


def total_venda(venda: dict) -> int:
    resultado = venda["quantidade"] * venda["preco_unitario"]
    return resultado

#venda = {"quantidade": 3, "preco_unitario": 50}
#valor = total_venda(venda)
#print(valor)


def faturacao_total(vendas: list[dict]) -> int:
    total = 0

    for venda in vendas:
        total += total_venda(venda)

    return total


def faturacao_por_ilha(vendas: list[dict]) -> dict[str, int]:
    por_ilha = {}

    for venda in vendas:
        ilha = venda["ilha"]
        valor = total_venda(venda)

        por_ilha[ilha] = por_ilha.get(ilha, 0) + valor

    return por_ilha



def ilha_top(por_ilha: dict[str, int]) -> str:
    return max(por_ilha, key=por_ilha.get)

#por_ilha = {
#    "Sal": 450,
 #   "Santiago": 700,
  #  "Fogo": 100
#}

# ---------------------------------------------------------------- Extensão (opcional)

def faturacao_mensal(vendas: list[dict]) -> dict[str, int]:
    """Dicionário {"AAAA-MM": faturação}, ordenado por mês."""
    # EXTENSÃO: igual a faturacao_por_ilha, mas a chave é o mês. O mês são os
    # 7 primeiros caracteres da data: venda["data"][:7] dá "2025-01".
    # No fim devolve o dicionário ordenado: dict(sorted(por_mes.items())).
    raise NotImplementedError("Extensão por fazer")


def formatar_cve(valor: int) -> str:
    """Formata um valor em escudos com espaço a separar os milhares: 1530740 -> '1 530 740 CVE'."""
    # EXTENSÃO: f"{valor:,}" dá "1,530,740". Troca as vírgulas por espaços e junta " CVE".
    raise NotImplementedError("Extensão por fazer")


# ---------------------------------------------------------------- Programa principal

def main(argv: list[str]) -> None:
    if len(argv) != 2:
        print("Uso: python -m morabeza.resumo <ficheiro.csv>")
        sys.exit(1)

    caminho = argv[1]
    vendas = ler_vendas(caminho)
    por_ilha = faturacao_por_ilha(vendas)

    print(f"Resumo de vendas: {caminho}")
    print(f"Número de vendas: {len(vendas)}")
    print(f"Faturação total: {faturacao_total(vendas)} CVE")
    print("Faturação por ilha:")
    for ilha, valor in sorted(por_ilha.items(), key=lambda par: par[1], reverse=True):
        print(f"  {ilha}: {valor} CVE")
    print(f"Ilha com maior faturação: {ilha_top(por_ilha)}")


if __name__ == "__main__":
    main(sys.argv)
