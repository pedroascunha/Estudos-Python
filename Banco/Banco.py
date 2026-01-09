"""
PyBank Next - Sistema bancário modular em Python.

Funcionalidades:
- Cadastro de usuários com CPF único
- Criação de contas correntes
- Depósito (positional-only)
- Saque (keyword-only)
- Extrato (saldo posicional, extrato keyword-only)
- Decorador de log
- Gerador de relatórios
- Iterador personalizado de contas
"""

from dataclasses import dataclass, field
from datetime import datetime
from textwrap import dedent
from typing import List, Optional


# ==========================
# Decorador de log
# ==========================

def log_transacao(tipo_transacao: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[LOG] {timestamp} - Transação: {tipo_transacao}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ==========================
# Modelos de domínio
# ==========================

@dataclass
class Usuario:
    nome: str
    nascimento: str
    cpf: str
    endereco: str


@dataclass
class ContaCorrente:
    agencia: str
    numero: int
    usuario_cpf: str
    saldo: float = 0.0
    extrato: List[str] = field(default_factory=list)
    num_saques: int = 0


# ==========================
# Estado da aplicação
# ==========================

USUARIOS: List[Usuario] = []
CONTAS: List[ContaCorrente] = []

AGENCIA_PADRAO = "0001"
LIMITE_SAQUES = 3
LIMITE_SAQUE_VALOR = 500.0


# ==========================
# Funções utilitárias
# ==========================

def limpar_cpf(cpf: str) -> str:
    return "".join(filter(str.isdigit, cpf))


def encontrar_usuario_por_cpf(cpf: str) -> Optional[Usuario]:
    cpf = limpar_cpf(cpf)
    return next((u for u in USUARIOS if u.cpf == cpf), None)


def encontrar_conta_por_numero(numero: int) -> Optional[ContaCorrente]:
    return next((c for c in CONTAS if c.numero == numero), None)


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ==========================
# Gerador de relatórios
# ==========================

def gerador_transacoes(extrato: List[str], tipo: Optional[str] = None):
    for transacao in extrato:
        if tipo:
            if tipo.lower() in transacao.lower():
                yield transacao
        else:
            yield transacao


# ==========================
# Iterador personalizado
# ==========================

class ContaIterador:
    def __init__(self, contas: List[ContaCorrente]):
        self._contas = contas
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._indice >= len(self._contas):
            raise StopIteration

        conta = self._contas[self._indice]
        self._indice += 1

        return {
            "agencia": conta.agencia,
            "numero": conta.numero,
            "cpf": conta.usuario_cpf,
            "saldo": conta.saldo,
        }


# ==========================
# Casos de uso
# ==========================

def criar_usuario() -> None:
    print("\n=== Novo usuário ===")
    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    cpf_raw = input("CPF: ").strip()
    endereco = input("Endereço: ").strip()

    cpf = limpar_cpf(cpf_raw)

    if not cpf or len(cpf) < 11:
        print("✗ CPF inválido.")
        return

    if encontrar_usuario_por_cpf(cpf):
        print("✗ Já existe usuário com esse CPF.")
        return

    USUARIOS.append(Usuario(nome, nascimento, cpf, endereco))
    print("✓ Usuário criado com sucesso.")


def criar_conta_corrente() -> None:
    print("\n=== Nova conta corrente ===")
    cpf_raw = input("CPF do usuário: ").strip()
    usuario = encontrar_usuario_por_cpf(cpf_raw)

    if not usuario:
        print("✗ Usuário não encontrado.")
        return

    numero_conta = len(CONTAS) + 1
    conta = ContaCorrente(AGENCIA_PADRAO, numero_conta, usuario.cpf)
    CONTAS.append(conta)

    print(f"✓ Conta criada | Agência: {conta.agencia} | Conta: {conta.numero}")


def listar_contas() -> None:
    print("\n=== Contas cadastradas ===")
    if not CONTAS:
        print("Nenhuma conta cadastrada.")
        return

    for info in ContaIterador(CONTAS):
        usuario = encontrar_usuario_por_cpf(info["cpf"])
        nome = usuario.nome if usuario else "Usuário não encontrado"

        print(
            f"Agência: {info['agencia']} | "
            f"Conta: {info['numero']:04d} | "
            f"Titular: {nome} | "
            f"Saldo: {formatar_moeda(info['saldo'])}"
        )


# ==========================
# Operações bancárias
# ==========================

@log_transacao("DEPÓSITO")
def deposito(saldo: float, valor: float, extrato: List[str], /):
    if valor <= 0:
        print("✗ Valor inválido.")
        return saldo, extrato

    saldo += valor
    extrato.append(
        f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Depósito: +{formatar_moeda(valor)}"
    )
    print("✓ Depósito realizado.")
    return saldo, extrato


@log_transacao("SAQUE")
def saque(*, saldo: float, valor: float, extrato: List[str],
          limite: float, numero_saques: int, limite_saques: int):
    if valor <= 0 or valor > saldo or valor > limite or numero_saques >= limite_saques:
        print("✗ Saque não permitido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    extrato.append(
        f"[{datetime.now().strftime('%d/%m/%Y %H:%M')}] Saque: -{formatar_moeda(valor)}"
    )
    print("✓ Saque realizado.")
    return saldo, extrato, numero_saques + 1


def extrato_(saldo: float, /, *, extrato: List[str]):
    print("\n=========== EXTRATO ===========")
    if not extrato:
        print("Sem movimentações.")
    else:
        for linha in gerador_transacoes(extrato):
            print(linha)
    print(f"\nSaldo atual: {formatar_moeda(saldo)}")
    print("==============================\n")


# ==========================
# Fluxo de operações
# ==========================

def selecionar_conta_existente() -> Optional[ContaCorrente]:
    try:
        numero = int(input("Número da conta: "))
    except ValueError:
        print("✗ Número inválido.")
        return None

    conta = encontrar_conta_por_numero(numero)
    if not conta:
        print("✗ Conta não encontrada.")
    return conta


def operacao_deposito():
    conta = selecionar_conta_existente()
    if not conta:
        return
    valor = float(input("Valor: ").replace(",", "."))
    conta.saldo, conta.extrato = deposito(conta.saldo, valor, conta.extrato)


def operacao_saque():
    conta = selecionar_conta_existente()
    if not conta:
        return
    valor = float(input("Valor: ").replace(",", "."))
    conta.saldo, conta.extrato, conta.num_saques = saque(
        saldo=conta.saldo,
        valor=valor,
        extrato=conta.extrato,
        limite=LIMITE_SAQUE_VALOR,
        numero_saques=conta.num_saques,
        limite_saques=LIMITE_SAQUES,
    )


def operacao_extrato():
    conta = selecionar_conta_existente()
    if conta:
        extrato_(conta.saldo, extrato=conta.extrato)


# ==========================
# Interface principal
# ==========================

def menu() -> str:
    return dedent("""
    ───────────────────────────────
          PyBank Next
    ───────────────────────────────
    [1] Criar usuário
    [2] Criar conta
    [3] Listar contas
    [4] Depósito
    [5] Saque
    [6] Extrato
    [0] Sair
    ───────────────────────────────
    Escolha: """)


def main():
    while True:
        opcao = input(menu()).strip()
        match opcao:
            case "1": criar_usuario()
            case "2": criar_conta_corrente()
            case "3": listar_contas()
            case "4": operacao_deposito()
            case "5": operacao_saque()
            case "6": operacao_extrato()
            case "0":
                print("Encerrando o sistema.")
                break
            case _:
                print("✗ Opção inválida.")


if __name__ == "__main__":
    main()
