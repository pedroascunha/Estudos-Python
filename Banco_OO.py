import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


# ========= CLASSES DE DOMÍNIO =========

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def extrato(self):
        linhas = ""
        for t in self.transacoes:
            linhas += f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}\n"
        return linhas


class Conta:
    def __init__(self, numero, cliente, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

        if valor > self.saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
            return False

        self.saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! Valor inválido. @@@")
            return False

        self.saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3, agencia="0001"):
        super().__init__(numero, cliente, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! Valor excede o limite. @@@")
            return False

        if excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        if super().sacar(valor):
            self.numero_saques += 1
            return True

        return False


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


# ========= TRANSAÇÕES =========

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        ...

    @abstractmethod
    def registrar(self, conta):
        ...


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


# ========= FUNÇÕES DE INTERFACE (MENU) =========

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    # neste exemplo usa sempre a primeira conta
    return cliente.contas[0]


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(nome, data_nasc, cpf, endereco)
    clientes.append(novo_cliente)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
Agência:\t{conta.agencia}
C/C:\t\t{conta.numero}
Titular:\t{conta.cliente.nome}
Saldo:\t\tR$ {conta.saldo:.2f}
"""
        print("=" * 100)
        print(textwrap.dedent(linha))


def depositar_fluxo(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def sacar_fluxo(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato_fluxo(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = conta.historico.extrato()
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def main():
    clientes = []
    contas = []
    proximo_numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            depositar_fluxo(clientes)

        elif opcao == "s":
            sacar_fluxo(clientes)

        elif opcao == "e":
            exibir_extrato_fluxo(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            criar_conta(proximo_numero_conta, clientes, contas)
            proximo_numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Operação inválida, tente novamente.")


if __name__ == "__main__":
    main()
