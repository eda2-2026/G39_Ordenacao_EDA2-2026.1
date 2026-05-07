from datetime import date

class Aniversariante:
    def __init__(self, nome: str, dia: int, mes: int, ano: int):
        self.nome = nome
        self.dia  = dia
        self.mes  = mes
        self.ano  = ano
        self.idade = self._calcular_idade()

    def _calcular_idade(self) -> int:
        hoje = date(2026, 1, 1)
        anos = hoje.year - self.ano
        if (self.mes, self.dia) > (hoje.month, hoje.day):
            anos -= 1
        return max(anos, 0)

    def data_tuple(self):
        return (self.ano, self.mes, self.dia)

    def __repr__(self):
        return (f"{self.nome:<20} | {self.dia:02d}/{self.mes:02d}/{self.ano} "
                f"| {self.idade} anos")

def bubble_sort(lista: list, chave, reverso: bool = False) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            a, b = chave(arr[j]), chave(arr[j + 1])
            deve_trocar = (a > b) if not reverso else (a < b)
            if deve_trocar:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocou = True
        if not trocou:
            break
    return arr


def insertion_sort(lista: list, chave, reverso: bool = False) -> list:
    arr = lista[:]
    for i in range(1, len(arr)):
        atual = arr[i]
        j = i - 1
        while j >= 0 and (
            (chave(arr[j]) > chave(atual)) if not reverso
            else (chave(arr[j]) < chave(atual))
        ):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = atual
    return arr


def selection_sort(lista: list, chave, reverso: bool = False) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        idx_alvo = i
        for j in range(i + 1, n):
            menor = chave(arr[j]) < chave(arr[idx_alvo])
            if (menor if not reverso else not menor):
                idx_alvo = j
        arr[i], arr[idx_alvo] = arr[idx_alvo], arr[i]
    return arr


def exibir_lista(lista: list, titulo: str = ""):
    sep = "─" * 52
    if titulo:
        print(f"\n{sep}")
        print(f"  {titulo}")
    print(sep)
    print(f"  {'NOME':<20} | {'DATA':<12} | IDADE")
    print(sep)
    for p in lista:
        print(f"  {p}")
    print(sep)


ALGORITMOS = {
    "1": ("Bubble Sort",    bubble_sort),
    "2": ("Insertion Sort", insertion_sort),
    "3": ("Selection Sort", selection_sort),
}

CHAVES = {
    "1": ("Data Completa (ano/mês/dia)", lambda p: p.data_tuple()),
    "2": ("Apenas Mês",                  lambda p: p.mes),
    "3": ("Apenas Dia",                  lambda p: p.dia),
    "4": ("Apenas Ano",                  lambda p: p.ano),
}


def carregar_csv(caminho: str) -> list:
    dados = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if linha.strip() and not linha.startswith("#"):
                partes = linha.strip().split(",")
                nome, dia, mes, ano = partes
                dados.append(Aniversariante(nome.strip(), int(dia), int(mes), int(ano)))
    return dados


def menu(dados: list):
    print("\n" + "═" * 52)
    print("   SISTEMA DE ORDENAÇÃO DE ANIVERSARIANTES")
    print("   COMMIT 1 — Ordenação por Data")
    print("═" * 52)

    exibir_lista(dados, "Lista original")

    print("\n  Algoritmos disponíveis:")
    for k, (nome, _) in ALGORITMOS.items():
        print(f"    [{k}] {nome}")
    alg_key = input("  Escolha o algoritmo: ").strip()
    if alg_key not in ALGORITMOS:
        print("  Opção inválida.")
        return
    alg_nome, alg_fn = ALGORITMOS[alg_key]

    print("\n  Chaves de ordenação:")
    for k, (nome, _) in CHAVES.items():
        print(f"    [{k}] {nome}")
    chave_key = input("  Escolha a chave: ").strip()
    if chave_key not in CHAVES:
        print("  Opção inválida.")
        return
    chave_nome, chave_fn = CHAVES[chave_key]

    direcao = input("\n  Direção — [1] Crescente  [2] Decrescente: ").strip()
    reverso = (direcao == "2")

    resultado = alg_fn(dados, chave_fn, reverso)
    dir_label = "Decrescente" if reverso else "Crescente"
    exibir_lista(resultado,
                 f"{alg_nome} | Chave: {chave_nome} | {dir_label}")


if __name__ == "__main__":
    caminho = input("Caminho do arquivo CSV: ").strip()
    dados = carregar_csv(caminho)
    print(f"\n  ✔ {len(dados)} registros carregados.")
    menu(dados)