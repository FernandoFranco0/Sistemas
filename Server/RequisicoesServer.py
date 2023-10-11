"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
from Constantes.Requisicoes import Requisicoes
from Constantes.Respostas import Repostas
from Repository.banco_de_dados import criar_cliente, get_saldo, atualizar_saldo, \
    verifica_por_rg_senha, get_nome_cliente
from models.Cliente import Cliente


def manipula_requisicoes(cabecalho, conexao):
    """
    - Manipula as requisições
    """
    switch(cabecalho, conexao)


def switch(cabecalho, conexao):
    """
    :param cabecalho:
    :param conexao:
    :return:
    - Direciona o tipo de requisição
    """
    if Requisicoes(cabecalho[0]).value == Requisicoes.LOGIN.value:
        login(conexao, cabecalho)
    elif Requisicoes(cabecalho[0]).value == Requisicoes.CADASTRO.value:
        cadastro(conexao, cabecalho)
    elif Requisicoes(cabecalho[0]).value == Requisicoes.SAQUE.value:
        saque(conexao, cabecalho)
    elif Requisicoes(cabecalho[0]).value == Requisicoes.DEPOSITO.value:
        deposito(conexao, cabecalho)
    elif Requisicoes(cabecalho[0]).value == Requisicoes.TRANSFERENCIA.value:
        transferencia(conexao, cabecalho)
    elif Requisicoes(cabecalho[0]).value == Requisicoes.CONSULTA_SALDO.value:
        saldo_cliente(conexao, cabecalho)
    else:
        print("Algo deu errado | LOG")


def cadastro(conexao, cabecalho):
    """
    - Cadastra um novo cliente no banco
    """
    cliente = Cliente(
        nome=cabecalho[1],
        rg=cabecalho[2],
        senha=cabecalho[3])
    criar_cliente(cliente)
    conexao.send(str.encode(Repostas.SUCCESS.value))


def saldo_cliente(conexao, cabecalho):
    """
    - Consulta o saldo do cliente
    """
    saldo = get_saldo(cabecalho[1])
    conexao.send(str.encode(Repostas.SUCCESS.value + '#' + str(saldo)))


def transferencia(conexao, cabecalho):
    """
    - Faz uma transferência entre conta de clientes do banco
    """
    valor = float(cabecalho[1])
    rg = cabecalho[2]
    rg_favorecido = cabecalho[3]
    saldo_atual = get_saldo(rg)
    saldo_atual_favorecido = get_saldo(rg_favorecido)
    if saldo_atual < valor:
        conexao.send(str.encode(Repostas.FORBIDDEN.value + '#' + 'Saldo insuficiente'))
    else:
        saldo_novo = saldo_atual - valor
        atualizar_saldo(saldo_novo, rg)
        saldo_novo_favorecido = saldo_atual_favorecido + valor
        atualizar_saldo(saldo_novo_favorecido, rg_favorecido)
        conexao.send(str.encode(Repostas.SUCCESS.value + '#' + str(saldo_novo) + '#' + str(saldo_novo_favorecido)))


def deposito(conexao, cabecalho):
    """
    - Faz a operação de depósito na conta do cliente
    """
    valor = float(cabecalho[1])
    rg = cabecalho[2]
    saldo_atual = get_saldo(rg)
    saldo_novo = saldo_atual + valor
    atualizar_saldo(saldo_novo, rg)
    conexao.send(str.encode(Repostas.SUCCESS.value + '#' + str(saldo_novo)))


def saque(conexao, cabecalho):
    """
    - Faz a operação de saque para o cliente
    """
    valor = float(cabecalho[1])
    rg = cabecalho[2]
    saldo_atual = get_saldo(rg)
    if saldo_atual < valor:
        conexao.send(str.encode(Repostas.FORBIDDEN.value + '#' + 'Saldo insuficiente'))
    else:
        saldo_novo = saldo_atual - valor
        atualizar_saldo(saldo_novo, rg)
        conexao.send(str.encode(Repostas.SUCCESS.value + '#' + str(saldo_novo)))


def login(conexao, cabecalho):
    """
    - Faz o login de um usuário no contexto do sistema
    """
    if not verifica_por_rg_senha(rg=cabecalho[1], senha=cabecalho[2]):
        cliente_nome, cliente_saldo = get_nome_cliente(rg=cabecalho[1])
        conexao.send(str.encode(Repostas.SUCCESS.value + '#' + cliente_nome + '#' + str(cliente_saldo)))
    else:
        conexao.send(str.encode(Repostas.FORBIDDEN.value, 'Dados de usuário incorretos'))
