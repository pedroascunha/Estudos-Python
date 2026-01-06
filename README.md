<h1 align="center">PyBank Next 💳</h1> <p align="center"> Sistema bancário em Python utilizando <b>Programação Orientada a Objetos</b>, com foco em modelagem de domínio, encapsulamento e histórico de transações. </p> <p align="center"> <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+"> <img src="https://img.shields.io/badge/status-em%20desenvolvimento-yellow" alt="Status"> </p>
✨ Funcionalidades
👤 Cadastro de clientes pessoas físicas com CPF, nome, data de nascimento e endereço.
​

🏦 Criação de contas correntes vinculadas a um cliente, com agência, número e saldo.

💰 Operações bancárias:

Depósito em conta corrente.

Saque com limite de valor por operação e limite de quantidade de saques.

Extrato com listagem das movimentações e saldo atual.

📋 Listagem de contas cadastradas, exibindo agência, número, titular e saldo.

🕒 Registro de movimentações com data, hora, tipo e valor no histórico da conta.

🧱 Tecnologias e conceitos
Python 3.10+

Orientação a Objetos:

Classes de domínio: Cliente, PessoaFisica, Conta, ContaCorrente, Historico.

Hierarquia de transações: classe abstrata Transacao e subclasses Deposito e Saque.

Uso de @classmethod, herança e composição para modelar o sistema bancário.
​

CLI (interface de linha de comando) via terminal.

🚀 Como executar
Certifique-se de ter o Python 3.10 ou superior instalado.
​

Clone este repositório:

bash
git clone https://github.com/seu-usuario/pybank-next.git
cd pybank-next
Execute o script principal (ajuste o nome do arquivo, se necessário):

bash
python Banco_OO.py
Use o menu interativo no terminal:

text
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q] Sair
=> 
🗂 Estrutura de classes
Historico

Armazena a lista de transações da conta e formata o extrato.

Conta

Base para contas bancárias: saldo, numero, agencia, cliente, historico.

ContaCorrente

Herda de Conta e adiciona limite, limite_saques e controle de número de saques.

Cliente

Possui endereco e uma lista de contas.

PessoaFisica

Herda de Cliente e adiciona nome, data_nascimento, cpf.

Transacao (abstrata)

Interface para operações com propriedade valor e método registrar.

Deposito e Saque

Implementam transações concretas, atualizando saldo e histórico.

💡 Próximos passos (ideias)
Persistir dados em arquivo (JSON/SQLite) ou banco de dados.
​

Permitir múltiplas contas por cliente na interface (escolha da conta ao transacionar).

Separar o código em módulos (domínio, serviços, interface) para maior organização.

Adicionar testes automatizados com pytest.
