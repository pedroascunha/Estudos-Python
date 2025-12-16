<h1 align="center">PyBank Next 💳</h1>

<p align="center">
  Sistema bancário modular em Python, focado em boas práticas, tipagem e uso de argumentos posicionais/nominais.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="Status">
</p>

---

## ✨ Funcionalidades

- 👤 Cadastro de usuários (clientes) com **validação de CPF único**
- 🏦 Criação de contas correntes vinculadas a um usuário
- 💰 Operações bancárias:
  - Depósito (argumentos **apenas posicionais**)
  - Saque (argumentos **apenas nomeados**)
  - Extrato (saldo posicional, extrato keyword-only)
- 📋 Listagem de contas cadastradas
- 🔐 Controle de limite diário de saques e valor máximo por saque
- 🕒 Registro de movimentações com data e hora no extrato

---

## 🧱 Tecnologias utilizadas

- Python 3.10+
- `dataclasses` para modelar Usuário e ContaCorrente
- Tipagem com `typing`
- CLI (interface de linha de comando) via terminal

---

## 🚀 Como executar

1. Certifique-se de ter o **Python 3.10 ou superior** instalado.
2. Clone este repositório:

git clone https://github.com/seu-usuario/pybank-next.git
cd pybank-next

texto

3. Execute o script principal:

python pybank_next.py

texto

4. Use o menu interativo:

───────────────────────────────
PyBank Próximo 💳
───────────────────────────────
Criar usuárioCriar
conta correnteListar
contas
Depósito
Saque
Extrato
Sair
───────────────────────────────

texto

---

## 🧪 Regras das funções principais

def saque(
*, saldo, valor, extrato,
limite, numero_saques, limite_saques
):
"""Saque - argumentos somente palavra-chave."""

texto
undefined
def deposito(saldo, valor, extrato, /):
"""Depósito - argumentos posicionais apenas."""

texto
undefined
def extrato_(saldo, /, *, extrato):
"""Extrato - saldo posicional, extrato somente palavra-chave."""

texto

- `saque` → só aceita argumentos **nomeados**.  
- `deposito` → só aceita argumentos **posicionais**.  
- `extrato_` → mistura saldo posicional com extrato keyword-only.

---

## 🗂 Estrutura de dados

- `Usuario`
  - `nome`, `nascimento`, `cpf` (apenas números), `endereco`
- `ContaCorrente`
  - `agencia`, `numero`, `usuario_cpf`, `saldo`, `extrato` (lista de strings), `num_saques`

---

## 💡 Próximos passos (ideias)

- Persistir dados em arquivo (JSON/SQLite)
- Autenticação por usuário/conta
- Suporte a múltiplas agências
- Testes automatizados com `pytest`
