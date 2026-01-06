<h1 align="center">PyBank Next 💳</h1> <p align="center"> Sistema bancário em Python usando <b>Programação Orientada a Objetos</b>, com foco em modelagem de domínio, histórico de transações e boas práticas de código. </p> <p align="center"> <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+"> <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="Status"> </p>
📚 Sobre o projeto
O PyBank Next é um sistema bancário de linha de comando que permite cadastrar clientes, criar contas correntes e realizar operações financeiras básicas (depósito, saque e extrato) utilizando um modelo orientado a objetos.
​

✨ Funcionalidades
Cadastro de clientes pessoas físicas (nome, CPF, data de nascimento e endereço).
​

Criação de contas correntes vinculadas a um cliente.

Depósito em conta corrente.

Saque com:

Limite de valor por operação.

Limite de quantidade de saques.

Emissão de extrato com:

Lista de transações (data, hora, tipo e valor).

Exibição do saldo atual.

Listagem de contas cadastradas (agência, número, titular e saldo).

🧱 Tecnologias e conceitos
Linguagem: Python 3.10+

Paradigma: Programação Orientada a Objetos

Conceitos aplicados:

Classes de domínio (Cliente, PessoaFisica, Conta, ContaCorrente, Historico).

Classe abstrata de transações (Transacao) e implementações concretas (Deposito, Saque).

Herança, composição, encapsulamento e métodos de classe (@classmethod).
​

Interface: aplicação em modo texto (CLI) executada no terminal.

🚀 Como executar
Verifique se o Python 3.10 ou superior está instalado na máquina.
​

Clone o repositório e acesse a pasta do projeto:

bash
git clone https://github.com/seu-usuario/pybank-next.git
cd pybank-next
Execute o script principal (ajuste o nome se necessário):

bash
python Banco_OO.py
Interaja pelo menu exibido no terminal:

text
================ MENU ================
[d]  Depositar
[s]  Sacar
[e]  Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q]  Sair
=> 
🗂 Estrutura de classes (resumo)
Historico

Armazena as transações realizadas na conta.

Gera o texto do extrato com data, tipo e valor.

Conta

Representa uma conta genérica com saldo, número, agência, cliente e histórico.

Possui operações básicas de depósito e saque.

ContaCorrente (Conta)

Especialização de Conta com limite de valor por saque e limite de quantidade de saques.

Cliente

Mantém endereço e lista de contas associadas.

PessoaFisica (Cliente)

Adiciona nome, data de nascimento e CPF.

Transacao (abstrata)

Define a interface para operações (valor e registrar).

Deposito / Saque (Transacao)

Implementam a lógica de registrar depósitos e saques na conta e no histórico.

🛠 Estrutura do código
Um possível layout de arquivos para o projeto:

text
pybank-next/
├─ Banco_OO.py        # Script principal com o loop do menu
├─ README.md          # Documentação do projeto
└─ (futuros módulos)  # domínio/, services/, etc.
💡 Próximos passos
Persistir dados em arquivo (JSON/CSV/SQLite) para manter clientes e contas entre execuções.
​

Permitir múltiplas contas por cliente na interface (escolha da conta ao operar).

Separar o código em módulos (domínio, serviços, interface) para facilitar manutenção e testes.

Adicionar testes automatizados com pytest e integrar a um fluxo de CI.
