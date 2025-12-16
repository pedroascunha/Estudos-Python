"""
PyBank Next - Sistema bancário modular em Python.

Funcionalidades:
- Cadastro de usuários (clientes) com validação de CPF único
- Criação de contas correntes vinculadas a usuários
- Depósito, saque e extrato com regras de argumentos:
    - saque: keyword-only
    - depósito: positional-only
    - extrato: saldo posicional, extrato keyword-only
- Listagem de contas
"""

from dataclasses import dataclass, field
from datetime import datetime
from textwrap import dedent
from typing import List, Optional


# ==========================
# Modelos de domínio
# ==========================

@dataclass
class Usuario:
    nome: str
    nascimento: str  # poderia ser datetime, mantido como string para simplicidade
    cpf: str         # apenas números
    endereco: str    # "logradouro, nro - bairro - cidade/UF"


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
# Casos de uso principais
# ==========================

def criar_usuario() -> None:
    print("\n=== Novo usuário ===")
    nome = input("Nome completo: ").strip()
    nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    cpf_raw = input("CPF (apenas números): ").strip()
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    cpf = limpar_cpf(cpf_raw)

    if not cpf or len(cpf) < 11:
        print("✗ CPF inválido.")
        return

    if encontrar_usuario_por_cpf(cpf):
        print("✗ Já existe usuário com esse CPF.")
        return

    usuario = Usuario(
        nome=nome,
        nascimento=nascimento,
        cpf=cpf,
        endereco=endereco,
    )
    USUARIOS.append(usuario)
    print("✓ Usuário criado com sucesso.")


def criar_conta_corrente() -> None:
    print("\n=== Nova conta corrente ===")
    cpf_raw = input("Informe o CPF do usuário: ").strip()
    usuario = encontrar_usuario_por_cpf(cpf_raw)

    if not usuario:
        print("✗ Usuário não encontrado para esse CPF.")
        return

    numero_conta = len(CONTAS) + 1

    conta = ContaCorrente(
        agencia=AGENCIA_PADRAO,
        numero=numero_conta,
        usuario_cpf=usuario.cpf,
    )
    CONTAS.append(conta)

    print(
        f"✓ Conta criada com sucesso.\n"
        f"  Agência: {conta.agencia} | Conta: {conta.numero} | Titular: {usuario.nome}"
    )


def listar_contas() -> None:
    print("\n=== Contas cadastradas ===")
    if not CONTAS:
        print("Nenhuma conta cadastrada.")
        return

    for conta in CONTAS:
        usuario = encontrar_usuario_por_cpf(conta.usuario_cpf)
        nome = usuario.nome if usuario else "Usuário não encontrado"
        print(
            f"Agência: {conta.agencia} | "
            f"Conta: {conta.numero:04d} | "
            f"Titular: {nome} ({conta.usuario_cpf})"
        )


# ==========================
# Operações bancárias
# ==========================

def saque(*, saldo: float, valor: float, extrato: List[str],
          limite: float, numero_saques: int, limite_saques: int):
    """Saque - argumentos apenas por nome (keyword-only)."""
    if valor <= 0:
        print("✗ Valor inválido para saque.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("✗ Operação negada. Saldo insuficiente.")
        return saldo, extrato, numero_saques

    if valor > limite:
        print("✗ Operação negada. Valor excede o limite por saque.")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("✗ Operação negada. Limite diário de saques atingido.")
        return saldo, extrato, numero_saques

    saldo -= valor
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    extrato.append(f"[{timestamp}] Saque: -{formatar_moeda(valor)}")
    numero_saques += 1
    print("✓ Saque realizado com sucesso.")

    return saldo, extrato, numero_saques


def deposito(saldo: float, valor: float, extrato: List[str], /):
    """Depósito - argumentos apenas posicionais (positional-only)."""
    if valor <= 0:
        print("✗ Valor inválido para depósito.")
        return saldo, extrato

    saldo += valor
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    extrato.append(f"[{timestamp}] Depósito: +{formatar_moeda(valor)}")
    print("✓ Depósito realizado com sucesso.")
    return saldo, extrato


def extrato_(saldo: float, /, *, extrato: List[str]):
    """Extrato - saldo posicional, extrato keyword-only."""
    print("\n=========== EXTRATO ===========")
    if not extrato:
        print("Não foram registradas movimentações.")
    else:
        for linha in extrato:
            print(linha)
    print(f"\nSaldo atual: {formatar_moeda(saldo)}")
    print("================================\n")


# ==========================
# Fluxo de operações em conta
# ==========================

def selecionar_conta_existente() -> Optional[ContaCorrente]:
    try:
        numero = int(input("Número da conta: ").strip())
    except ValueError:
        print("✗ Número de conta inválido.")
        return None

    conta = encontrar_conta_por_numero(numero)
    if not conta:
        print("✗ Conta não encontrada.")
    return conta


def operacao_deposito() -> None:
    print("\n=== Depósito ===")
    conta = selecionar_conta_existente()
    if not conta:
        return

    try:
        valor = float(input("Valor do depósito: ").replace(",", "."))
    except ValueError:
        print("✗ Valor inválido.")
        return

    conta.saldo, conta.extrato = deposito(conta.saldo, valor, conta.extrato)


def operacao_saque() -> None:
    print("\n=== Saque ===")
    conta = selecionar_conta_existente()
    if not conta:
        return

    try:
        valor = float(input("Valor do saque: ").replace(",", "."))
    except ValueError:
        print("✗ Valor inválido.")
        return

    conta.saldo, conta.extrato, conta.num_saques = saque(
        saldo=conta.saldo,
        valor=valor,
        extrato=conta.extrato,
        limite=LIMITE_SAQUE_VALOR,
        numero_saques=conta.num_saques,
        limite_saques=LIMITE_SAQUES,
    )


def operacao_extrato() -> None:
    print("\n=== Extrato ===")
    conta = selecionar_conta_existente()
    if not conta:
        return

    extrato_(conta.saldo, extrato=conta.extrato)


# ==========================
# Interface principal
# ==========================

def menu() -> str:
    return dedent(
        """
        ───────────────────────────────
              PyBank Next  💳
        ───────────────────────────────
        [1] Criar usuário
        [2] Criar conta corrente
        [3] Listar contas
        [4] Depósito
        [5] Saque
        [6] Extrato
        [0] Sair
        ───────────────────────────────
        Escolha uma opção: """
    )


def main() -> None:
    while True:
        opcao = input(menu()).strip()

        match opcao:
            case "1":
                criar_usuario()
            case "2":
                criar_conta_corrente()
            case "3":
                listar_contas()
            case "4":
                operacao_deposito()
            case "5":
                operacao_saque()
            case "6":
                operacao_extrato()
            case "0":
                print("Encerrando PyBank Next. Até logo!")
                break
            case _:
                print("✗ Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
