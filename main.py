import random
import os
import time
from datetime import date
from typing import Callable


class Aniversariante:
    def __init__(self, nome: str, dia: int, mes: int, ano: int):
        self.nome  = nome
        self.dia   = int(dia)
        self.mes   = int(mes)
        self.ano   = int(ano)
        self.idade = self._calcular_idade()

    def _calcular_idade(self) -> int:
        hoje = date.today()
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
        return cls(partes[0].strip(), int(partes[1]), int(partes[2]), int(partes[3]))


def bubble_sort(lista: list, chave: Callable, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            if (chave(arr[j]) > chave(arr[j+1])) != reverso:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                trocou = True
        if not trocou:
            break
    return arr


def insertion_sort(lista: list, chave: Callable, reverso=False) -> list:
    arr = lista[:]
    for i in range(1, len(arr)):
        atual = arr[i]
        j = i - 1
        while j >= 0 and ((chave(arr[j]) > chave(atual)) != reverso):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = atual
    return arr


def selection_sort(lista: list, chave: Callable, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        idx = i
        for j in range(i+1, n):
            if (chave(arr[j]) < chave(arr[idx])) != reverso:
                idx = j
        arr[i], arr[idx] = arr[idx], arr[i]
    return arr

def shell_sort(lista: list, chave: Callable, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)
    for gap in [701, 301, 132, 57, 23, 10, 4, 1]:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and ((chave(arr[j-gap]) > chave(temp)) != reverso):
                arr[j] = arr[j-gap]
                j -= gap
            arr[j] = temp
    return arr


def merge_sort(lista: list, chave: Callable, reverso=False) -> list:
    if len(lista) <= 1:
        return lista[:]
    meio = len(lista) // 2
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


def quick_sort(lista: list, chave: Callable, reverso=False) -> list:
    arr = lista[:]
    _qs(arr, 0, len(arr)-1, chave, reverso)
    return arr
 
 
def _qs(arr, low, high, chave, reverso):
    if low < high:
        meio = (low + high) // 2
        candidatos = [(chave(arr[low]), low), (chave(arr[meio]), meio), (chave(arr[high]), high)]
        candidatos.sort(key=lambda x: x[0])
        pi = candidatos[1][1]
        arr[pi], arr[high] = arr[high], arr[pi]
        pivo = chave(arr[high])
        i = low - 1
        for j in range(low, high):
            if (chave(arr[j]) <= pivo) != reverso:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        p = i + 1
        _qs(arr, low, p-1, chave, reverso)
        _qs(arr, p+1, high, chave, reverso)


def heap_sort(lista: list, chave: Callable, reverso=False) -> list:
    arr = lista[:]
    n = len(arr)

    def heapify(arr, n, i):
        topo = i
        esq, dir_ = 2*i+1, 2*i+2
        for filho in [esq, dir_]:
            if filho < n:
                cond = (chave(arr[filho]) > chave(arr[topo])) if not reverso \
                       else (chave(arr[filho]) < chave(arr[topo]))
                if cond:
                    topo = filho
        if topo != i:
            arr[i], arr[topo] = arr[topo], arr[i]
            heapify(arr, n, topo)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


def counting_sort(lista: list, chave: Callable, reverso=False) -> list:
    if not lista:
        return []
    try:
        vals = [int(chave(p)) for p in lista]
    except (TypeError, ValueError):
        print("Counting Sort requer chave inteira. Usando Merge Sort como fallback.")
        return merge_sort(lista, chave, reverso)

    minv, maxv = min(vals), max(vals)
    k = maxv - minv + 1
    contagem = [[] for _ in range(k)]
    for p, v in zip(lista, vals):
        contagem[v - minv].append(p)

    resultado = []
    ordem = range(k) if not reverso else range(k-1, -1, -1)
    for i in ordem:
        resultado.extend(contagem[i])
    return resultado


def bucket_sort(lista: list, chave: Callable, reverso=False) -> list:
    if not lista:
        return []
    try:
        vals = [int(chave(p)) for p in lista]
    except (TypeError, ValueError):
        print("Bucket Sort requer chave inteira. Usando Merge Sort como fallback.")
        return merge_sort(lista, chave, reverso)

    minv, maxv = min(vals), max(vals)
    n_baldes = maxv - minv + 1
    baldes = [[] for _ in range(n_baldes)]
    for p, v in zip(lista, vals):
        baldes[v - minv].append(p)

    # ordena dentro de cada balde (para chave composta)
    resultado = []
    ordem = range(n_baldes) if not reverso else range(n_baldes-1, -1, -1)
    for i in ordem:
        if baldes[i]:
            resultado.extend(insertion_sort(baldes[i], chave))
    return resultado


def radix_sort(lista: list, chave: Callable, reverso=False) -> list:
    if not lista:
        return []
    try:
        vals = [int(chave(p)) for p in lista]
    except (TypeError, ValueError):
        print("Radix Sort requer chave inteira. Usando Merge Sort como fallback.")
        return merge_sort(lista, chave, reverso)
 
    offset = min(vals)
    vals = [v - offset for v in vals]
 
    max_val = max(vals) if vals else 0
    exp = 1
    arr = list(zip(lista, vals))
 
    while max_val // exp > 0:
        baldes = [[] for _ in range(10)]
        for obj, v in arr:
            baldes[(v // exp) % 10].append((obj, v))
        arr = []
        for b in baldes:
            arr.extend(b)
        exp *= 10
 
    resultado = [obj for obj, _ in arr]
    return resultado if not reverso else resultado[::-1]


banco: list[Aniversariante] = []

_NOMES_MOCK = [
    "Ana Lima","Bruno Souza","Carla Mendes","Diego Rocha","Elena Ferreira",
    "Fábio Nunes","Gisele Castro","Henrique Vaz","Isabela Pinto","João Alves",
    "Kátia Ramos","Lucas Teixeira","Mariana Gomes","Nelson Dias","Olívia Lopes",
    "Paulo Barbosa","Queila Santos","Roberto Silva","Sara Moura","Tiago Freitas",
    "Úrsula Costa","Vítor Melo","Wanda Cunha","Xênia Borges","Yago Pires",
    "Zara Monteiro","Alexandre Cruz","Beatriz Araujo","César Tavares","Daniela Braga",
]


def popular_aleatorio(n: int = 20):
    global banco
    banco = []
    nomes = _NOMES_MOCK[:]
    random.shuffle(nomes)
    for nome in nomes[:min(n, len(nomes))]:
        dia = random.randint(1, 28)
        mes = random.randint(1, 12)
        ano = random.randint(1955, 2008)
        banco.append(Aniversariante(nome, dia, mes, ano))
    print(f"\n  ✔ {len(banco)} registros gerados.")


def popular_arquivo(caminho: str):
    global banco
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}"); return
    banco = []
    erros = 0
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            if linha.strip() and not linha.startswith("#"):
                try:
                    banco.append(Aniversariante.from_csv_line(linha))
                except ValueError:
                    erros += 1
    print(f"{len(banco)} registros carregados. Erros ignorados: {erros}.")


def exportar_csv(caminho: str = "aniversariantes.csv"):
    if not banco:
        print("  Nenhum dado para exportar."); return
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("# nome,dia,mes,ano\n")
        for p in banco:
            f.write(p.to_csv_line() + "\n")
    print(f"Exportado para '{caminho}' ({len(banco)} registros).")


def cadastrar():
    print("\n  ── Novo Cadastro ──")
    nome = input("  Nome: ").strip()
    if not nome:
        print("  Nome obrigatório."); return
    try:
        dia = int(input("  Dia  (1-31): "))
        mes = int(input("  Mês  (1-12): "))
        ano = int(input("  Ano  (ex: 1990): "))
        if not (1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2026):
            raise ValueError
    except ValueError:
        print("  Data inválida."); return
    banco.append(Aniversariante(nome, dia, mes, ano))
    print(f"'{nome}' cadastrado.")


def teste_estabilidade():
    if not banco:
        print("\n  Popule o banco antes de testar.")
        return

    print("\n" + "═"*58)
    print("  TESTE DE ESTABILIDADE — Ordenação Encadeada")
    print("  Passo 1: Insertion Sort por Mês")
    print("  Passo 2: Insertion Sort por Ano")
    print("  Resultado: dentro do mesmo Ano, a ordem por Mês é mantida.")
    print("═"*58)

    passo1 = insertion_sort(banco, lambda p: p.mes)
    passo2 = insertion_sort(passo1, lambda p: p.ano)

    sep = "─"*58
    print(f"\n  {'NOME':<22} | {'DATA':<12} | IDADE")
    print(sep)
    for p in passo2:
        print(f"  {p}")
    print(sep)
    print("Estabilidade verificada: meses preservados dentro de cada ano.")

def benchmark():
    if not banco:
        print("\n  Popule o banco antes do benchmark.")
        return
 
    chave_comp    = lambda p: p.data_tuple()
    chave_distrib = lambda p: p.ano
 
    print(f"\n  Benchmark — {len(banco)} registros")
    print(f"  Comparação: chave=Data Completa | Distribuição: chave=Ano\n")
    print(f"  {'Algoritmo':<20} {'Tempo (ms)':>12}")
    print("  " + "─"*34)
    for k, (nome, fn) in ALGORITMOS.items():
        chave = chave_distrib if k in _DISTRIB else chave_comp
        inicio = time.perf_counter()
        for _ in range(100):
            fn(banco, chave)
        elapsed = (time.perf_counter() - inicio) / 100 * 1000
        print(f"  {nome:<20} {elapsed:>10.4f} ms")


ALGORITMOS = {
    "1":  ("Bubble Sort",    bubble_sort),
    "2":  ("Insertion Sort", insertion_sort),
    "3":  ("Selection Sort", selection_sort),
    "4":  ("Shell Sort",     shell_sort),
    "5":  ("Merge Sort",     merge_sort),
    "6":  ("Quick Sort",     quick_sort),
    "7":  ("Heap Sort",      heap_sort),
    "8":  ("Bucket Sort",    bucket_sort),
    "9":  ("Counting Sort",  counting_sort),
    "10": ("Radix Sort",     radix_sort),
}

CHAVES = {
    "1": ("Nome",                        lambda p: p.nome.lower()),
    "2": ("Data Completa (ano/mês/dia)", lambda p: p.data_tuple()),
    "3": ("Apenas Dia",                  lambda p: p.dia),
    "4": ("Apenas Mês",                  lambda p: p.mes),
    "5": ("Apenas Ano",                  lambda p: p.ano),
    "6": ("Idade",                       lambda p: p.idade),
}

_DISTRIB = {"8", "9", "10"}
_CHAVES_INT = {"3", "4", "5", "6"}

def exibir(lista: list, titulo: str = ""):
    sep = "─"*58
    if titulo:
        print(f"\n{sep}\n  {titulo}")
    print(sep)
    print(f"  {'NOME':<22} | {'DATA':<12} | IDADE")
    print(sep)
    for p in lista:
        print(f"  {p}")
    print(f"  {sep}\n  Total: {len(lista)} registro(s)")
    print(sep)


def menu_ordenar():
    if not banco:
        print("\n  Banco vazio. Cadastre ou popule primeiro.")
        return

    print("\n  ── Algoritmos ──")
    for k, (nome, _) in ALGORITMOS.items():
        sufixo = ""
        if k in {"1","2","3"}:  sufixo = " [O(n²)]"
        elif k in {"4","5","6","7"}: sufixo = " [O(n log n)]"
        else: sufixo = " [Distribuição]"
        print(f"    [{k:>2}] {nome}{sufixo}")
    alg_k = input("  Escolha: ").strip()
    if alg_k not in ALGORITMOS:
        print("  Inválido."); return
    alg_nome, alg_fn = ALGORITMOS[alg_k]

    print("\n  ── Chave de Ordenação ──")
    for k, (nome, _) in CHAVES.items():
        aviso = "(recomendado para distribuição)" if (alg_k in _DISTRIB and k in _CHAVES_INT) else ""
        print(f"    [{k}] {nome}{aviso}")
    if alg_k in _DISTRIB:
        print("Algoritmos de distribuição funcionam melhor com chaves inteiras (3-6).")
    ch_k = input("  Escolha: ").strip()
    if ch_k not in CHAVES:
        print("  Inválido."); return
    ch_nome, ch_fn = CHAVES[ch_k]

    dir_ = input("\n  Direção [1] Crescente  [2] Decrescente: ").strip()
    reverso = (dir_ == "2")
    dir_label = "Decrescente" if reverso else "Crescente"

    inicio = time.perf_counter()
    resultado = alg_fn(banco, ch_fn, reverso)
    elapsed = (time.perf_counter() - inicio) * 1000

    exibir(resultado, f"{alg_nome}  |  {ch_nome}  |  {dir_label}  |  {elapsed:.3f} ms")


def main():
    while True:
        print("\n" + "═"*58)
        print("   SISTEMA DE ANIVERSARIANTES  ")
        print(f"   Registros carregados: {len(banco)}")
        print("═"*58)
        print("  [1]  Cadastrar manualmente")
        print("  [2]  Popular (geração aleatória)")
        print("  [3]  Popular (arquivo CSV)")
        print("  [4]  Exportar CSV")
        print("  [5]  Visualizar lista atual")
        print("  [6]  Ordenar")
        print("  [7]  Teste de estabilidade")
        print("  [8]  Benchmark de algoritmos")
        print("  [0]  Sair")
        op = input("\n  Opção: ").strip()

        if op == "1":
            cadastrar()
        elif op == "2":
            qtd = input("  Quantidade [Enter = 20]: ").strip()
            popular_aleatorio(int(qtd) if qtd.isdigit() else 20)
        elif op == "3":
            caminho = input("  Caminho do arquivo CSV: ").strip()
            popular_arquivo(caminho)
        elif op == "4":
            caminho = input("  Nome do arquivo [Enter = aniversariantes.csv]: ").strip()
            exportar_csv(caminho if caminho else "aniversariantes.csv")
        elif op == "5":
            if banco:
                exibir(banco, "Lista atual (sem ordenação)")
            else:
                print("\n  Banco vazio.")
        elif op == "6":
            menu_ordenar()
        elif op == "7":
            teste_estabilidade()
        elif op == "8":
            benchmark()
        elif op == "0":
            print("\n  Encerrando. Até mais!\n")
            break
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    main()