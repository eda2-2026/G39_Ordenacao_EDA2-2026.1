import random
import os
from datetime import date

class Aniversariante:
    def __init__(self, nome: str, dia: int, mes: int, ano: int):
        self.nome  = nome
        self.dia   = dia
        self.mes   = mes
        self.ano   = ano
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
        return (f"{self.nome:<22} | {self.dia:02d}/{self.mes:02d}/{self.ano} "
                f"| {self.idade:>3} anos")

    def to_csv_line(self) -> str:
        return f"{self.nome},{self.dia},{self.mes},{self.ano}"

    @classmethod
    def from_csv_line(cls, linha: str):
        partes = linha.strip().split(",")
        if len(partes) != 4:
            raise ValueError(f"Linha inválida: {linha}")
        nome, dia, mes, ano = partes
        return cls(nome.strip(), int(dia), int(mes), int(ano))


def bubble_sort(lista: list, chave, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            deve_trocar = (chave(arr[j]) > chave(arr[j+1])) if not reverso \
                     else (chave(arr[j]) < chave(arr[j+1]))
            if deve_trocar:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                trocou = True
        if not trocou:
            break
    return arr


def insertion_sort(lista: list, chave, reverso=False) -> list:
    arr = lista[:]
    for i in range(1, len(arr)):
        atual = arr[i]
        j = i - 1
        while j >= 0 and (
            (chave(arr[j]) > chave(atual)) if not reverso
            else (chave(arr[j]) < chave(atual))
        ):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = atual
    return arr


def selection_sort(lista: list, chave, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        idx = i
        for j in range(i+1, n):
            cond = chave(arr[j]) < chave(arr[idx]) if not reverso \
                   else chave(arr[j]) > chave(arr[idx])
            if cond:
                idx = j
        arr[i], arr[idx] = arr[idx], arr[i]
    return arr


def shell_sort(lista: list, chave, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and (
                (chave(arr[j-gap]) > chave(temp)) if not reverso
                else (chave(arr[j-gap]) < chave(temp))
            ):
                arr[j] = arr[j-gap]
                j -= gap
            arr[j] = temp
    return arr


def merge_sort(lista: list, chave, reverso=False) -> list:
    if len(lista) <= 1:
        return lista[:]

    meio = len(lista) 
    esq  = merge_sort(lista[:meio], chave, reverso)
    dir_ = merge_sort(lista[meio:], chave, reverso)

    resultado, i, j = [], 0, 0
    while i < len(esq) and j < len(dir_):
        cond = (chave(esq[i]) <= chave(dir_[j])) if not reverso \
               else (chave(esq[i]) >= chave(dir_[j]))
        if cond:
            resultado.append(esq[i]); i += 1
        else:
            resultado.append(dir_[j]); j += 1
    resultado.extend(esq[i:])
    resultado.extend(dir_[j:])
    return resultado


def quick_sort(lista: list, chave, reverso=False) -> list:
    arr = lista[:]
    _quick_sort_rec(arr, 0, len(arr)-1, chave, reverso)
    return arr


def _pivot_mediana_tres(arr, baixo, alto, chave):
    meio = (baixo + alto) // 2
    tripla = [(chave(arr[baixo]), baixo),
              (chave(arr[meio]),  meio),
              (chave(arr[alto]),  alto)]
    tripla.sort()
    return tripla[1][1]   # índice do valor do meio


def _quick_sort_rec(arr, baixo, alto, chave, reverso):
    if baixo < alto:
        idx_pivo = _pivot_mediana_tres(arr, baixo, alto, chave)
        arr[idx_pivo], arr[alto] = arr[alto], arr[idx_pivo]
        pivo_val = chave(arr[alto])
        i = baixo - 1
        for j in range(baixo, alto):
            cond = (chave(arr[j]) <= pivo_val) if not reverso \
                   else (chave(arr[j]) >= pivo_val)
            if cond:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[alto] = arr[alto], arr[i+1]
        p = i + 1
        _quick_sort_rec(arr, baixo, p-1, chave, reverso)
        _quick_sort_rec(arr, p+1, alto, chave, reverso)


def heap_sort(lista: list, chave, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)

    def heapify(arr, n, i):
        maior = i
        esq, dir_ = 2*i+1, 2*i+2
        if esq < n:
            cond = (chave(arr[esq]) > chave(arr[maior])) if not reverso \
                   else (chave(arr[esq]) < chave(arr[maior]))
            if cond:
                maior = esq
        if dir_ < n:
            cond = (chave(arr[dir_]) > chave(arr[maior])) if not reverso \
                   else (chave(arr[dir_]) < chave(arr[maior]))
            if cond:
                maior = dir_
        if maior != i:
            arr[i], arr[maior] = arr[maior], arr[i]
            heapify(arr, n, maior)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


banco: list[Aniversariante] = []

NOMES_MOCK = [
    "Ana Lima","Bruno Souza","Carla Mendes","Diego Rocha","Elena Ferreira",
    "Fábio Nunes","Gisele Castro","Henrique Vaz","Isabela Pinto","João Alves",
    "Kátia Ramos","Lucas Teixeira","Mariana Gomes","Nelson Dias","Olívia Lopes",
    "Paulo Barbosa","Queila Santos","Roberto Silva","Sara Moura","Tiago Freitas",
]


def popular_aleatorio(n: int = 15):
    global banco
    banco = []
    nomes_disponiveis = NOMES_MOCK[:]
    random.shuffle(nomes_disponiveis)
    usados = set()
    for i in range(min(n, len(nomes_disponiveis))):
        nome = nomes_disponiveis[i]
        if nome in usados:
            continue
        usados.add(nome)
        dia = random.randint(1, 28)
        mes = random.randint(1, 12)
        ano = random.randint(1960, 2010)
        banco.append(Aniversariante(nome, dia, mes, ano))
    print(f"\n  ✔ {len(banco)} registros gerados com sucesso.")


def popular_arquivo(caminho: str):
    global banco
    if not os.path.exists(caminho):
        print(f"  ✗ Arquivo não encontrado: {caminho}")
        return
    banco = []
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if linha.strip() and not linha.startswith("#"):
                try:
                    banco.append(Aniversariante.from_csv_line(linha))
                except ValueError as e:
                    print(f"  Aviso: {e}")
    print(f"\n  ✔ {len(banco)} registros carregados de '{caminho}'.")


def cadastrar():
    print("\n  ── Novo Cadastro ──")
    nome = input("  Nome: ").strip()
    if not nome:
        print("  Nome não pode ser vazio."); return
    try:
        dia = int(input("  Dia de nascimento  (1-31): "))
        mes = int(input("  Mês de nascimento  (1-12): "))
        ano = int(input("  Ano de nascimento  (ex: 1990): "))
        if not (1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2026):
            raise ValueError
    except ValueError:
        print("  Data inválida."); return
    banco.append(Aniversariante(nome, dia, mes, ano))
    print(f"  ✔ '{nome}' cadastrado com sucesso.")


ALGORITMOS = {
    "1": ("Bubble Sort",    bubble_sort),
    "2": ("Insertion Sort", insertion_sort),
    "3": ("Selection Sort", selection_sort),
    "4": ("Shell Sort",     shell_sort),
    "5": ("Merge Sort",     merge_sort),
    "6": ("Quick Sort",     quick_sort),
    "7": ("Heap Sort",      heap_sort),
}

CHAVES = {
    "1": ("Nome",                        lambda p: p.nome.lower()),
    "2": ("Data Completa (ano/mês/dia)", lambda p: p.data_tuple()),
    "3": ("Apenas Dia",                  lambda p: p.dia),
    "4": ("Apenas Mês",                  lambda p: p.mes),
    "5": ("Apenas Ano",                  lambda p: p.ano),
    "6": ("Idade",                       lambda p: p.idade),
}


def exibir(lista: list, titulo: str = ""):
    sep = "─" * 58
    if titulo:
        print(f"\n{sep}")
        print(f"  {titulo}")
    print(sep)
    print(f"  {'NOME':<22} | {'DATA':<12} | IDADE")
    print(sep)
    for p in lista:
        print(f"  {p}")
    print(f"  {sep}\n  Total: {len(lista)} registro(s)")
    print(sep)


def menu_ordenar():
    if not banco:
        print("\n  Nenhum registro cadastrado. Use 'Popular' ou 'Cadastrar' primeiro.")
        return

    print("\n  ── Algoritmos ──")
    for k, (nome, _) in ALGORITMOS.items():
        print(f"    [{k}] {nome}")
    alg_k = input("  Escolha: ").strip()
    if alg_k not in ALGORITMOS:
        print("  Inválido."); return
    alg_nome, alg_fn = ALGORITMOS[alg_k]

    print("\n  ── Chave de Ordenação ──")
    for k, (nome, _) in CHAVES.items():
        print(f"    [{k}] {nome}")
    ch_k = input("  Escolha: ").strip()
    if ch_k not in CHAVES:
        print("  Inválido."); return
    ch_nome, ch_fn = CHAVES[ch_k]

    dir_ = input("\n  Direção [1] Crescente  [2] Decrescente: ").strip()
    reverso = (dir_ == "2")

    resultado = alg_fn(banco, ch_fn, reverso)
    dir_label = "Decrescente" if reverso else "Crescente"
    exibir(resultado, f"{alg_nome}  |  Chave: {ch_nome}  |  {dir_label}")


def main():
    while True:
        print("\n" + "═"*58)
        print("   SISTEMA DE ANIVERSARIANTES  —  COMMIT 2")
        print(f"   Registros em memória: {len(banco)}")
        print("═"*58)
        print("  [1] Cadastrar manualmente")
        print("  [2] Popular (aleatório)")
        print("  [3] Popular (arquivo CSV)")
        print("  [4] Visualizar lista atual")
        print("  [5] Ordenar")
        print("  [0] Sair")
        op = input("\n  Opção: ").strip()

        if op == "1":
            cadastrar()
        elif op == "2":
            qtd = input("  Quantos registros? [Enter = 15]: ").strip()
            popular_aleatorio(int(qtd) if qtd.isdigit() else 15)
        elif op == "3":
            caminho = input("  Caminho do arquivo CSV: ").strip()
            popular_arquivo(caminho)
        elif op == "4":
            if banco:
                exibir(banco, "Lista atual (sem ordenação)")
            else:
                print("\n  Nenhum registro.")
        elif op == "5":
            menu_ordenar()
        elif op == "0":
            print("\n  Encerrando. Até mais!\n")
            break
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    main()