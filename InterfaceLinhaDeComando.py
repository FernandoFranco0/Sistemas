"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""

from Client.Client import requisicao_cadastro, requisicao_login, requisicao_saque, requisicao_deposito, \
    requisicao_transferencia, requisicao_consultar_saldo
from Constantes.Requisicoes import Requisicoes
from Constantes.Respostas import Repostas
from models.Cliente import Cliente


def switch_main_menu(opcao, count_event):
    """
    :param opcao: int
    :param count_event: int
    :return: int, bool

    - Faz uma requisição ao servidor para encontrar o cliente na base de dados
    - Caso a resposta seja sucesso, abre uma sessão para o usuário
    - Caso não exista o usuário na base, volta para o menu principal
    """
    if opcao == Requisicoes.CADASTRO.value:
        count_event += 1
        cliente_cadastro = cadastrar_cliente()
        requisicao_cadastro(cliente_cadastro.get_rg(), cliente_cadastro.get_nome(), cliente_cadastro.get_senha())
        return count_event, True

    elif opcao == Requisicoes.LOGIN.value:
        count_event += 1
        rg_cliente, senha_cliente = digitar_informacoes_login()
        resposta_requisicao, nome_cliente, saldo_cliente = requisicao_login(rg_cliente, senha_cliente)
        if resposta_requisicao == Repostas.SUCCESS:
            count_event = menu_sessao(rg_cliente, count_event)
            return count_event, True
        else:
            print(resposta_requisicao)
            return count_event, True
    else:
        count_event += 1
        return count_event, True


def menu_sessao(rg_cliente, count_event):
    """
    :param rg_cliente: str
    :param count_event: int
    :return: int

    - Interface do menu da sessão.
    - Esse menu funciona quando o usuário está logado no sistema, para fazer as seguintes operações
        - Saque
        - Depósito
        - Consultar Saldo
        - Transferência
        - Listar Clientes
    """
    continuar = True
    while continuar:
        count_event += 1
        print_operacoes_sessao()
        operacao_desejada = input("Opção: ")
        continuar = switch_operacao(operacao_desejada, rg_cliente)
        print("Relógio: " + str(count_event))
    return count_event


def switch_operacao(operacao, rg_cliente):
    """
    :param operacao: str
    :param rg_cliente: str
    :return: bool
    - Direciona a operação desejada no menu da sessão
    """
    if operacao == Requisicoes.SAQUE.value:
        valor_saque = digitar_valor_transacao()
        menssagem_requisicao, novo_saldo = requisicao_saque(valor_saque, rg_cliente)
        mensagem_saque = "Saque de " + str(valor_saque) + " na conta. Novo Saldo: " + novo_saldo + "."
        print(mensagem_saque)
        return True
    elif operacao == Requisicoes.DEPOSITO.value:
        valor_deposito = digitar_valor_transacao()
        menssagem_requisicao, novo_saldo = requisicao_deposito(valor_deposito, rg_cliente)
        mensagem_deposito = "Depósito de " + str(valor_deposito) + " na conta. Novo Saldo: " + novo_saldo + "."
        print(mensagem_deposito)
        return True
    elif operacao == Requisicoes.CONSULTA_SALDO.value:
        menssagem_requisicao, saldo = requisicao_consultar_saldo(rg_cliente)
        mensagem_saldo = "O seu saldo é: " + saldo + "."
        print(mensagem_saldo)
        return True
    elif operacao == Requisicoes.TRANSFERENCIA.value:
        rg_destino, valor_transferencia = informacoes_transferencia()
        mensagem, novo_saldo, novo_saldo_favorecido = requisicao_transferencia(valor_transferencia, rg_cliente,
                                                                               rg_destino)
        mensagem_transferencia = "Transferência com valor de " + str(valor_transferencia) + " feita de: " + \
                                 rg_cliente + " para: " + rg_destino + \
                                 ". Novo Saldo: " + str(novo_saldo) + "."
        print(mensagem_transferencia)
        return True
    else:
        return False


def cadastrar_cliente():
    """
    :param count_event:
    :return: int
    - Cria um cliente do banco e o cadastra, persistindo-o no banco de dados
    """
    rg_cliente = input("Digite o rg: ")
    nome_cliente = input("Digite o nome: ")
    senha_cliente = input("Digite a sua senha: ")

    return Cliente(rg_cliente, nome_cliente, senha_cliente)


def digitar_informacoes_login():
    """
    :return: str, str
    - Entrada das informações de login, sendo elas, respectivamente, rg e senha
    """
    rg_cliente = input("Digite o rg: ")
    senha_cliente = input("Digite a sua senha: ")
    return rg_cliente, senha_cliente


def informacoes_transferencia():
    """
    :return: str, float
    -  Entrada das informações da transferencia, sendo elas o rg do usuário de destino e o valor da tranferência
    """
    rg_destino = input("Digite o rg do usuario da conta de destino: ")
    valor_transferencia = digitar_valor_transacao()
    return rg_destino, valor_transferencia


def digitar_valor_transacao():
    """
    :return: float
    - Entrada do valor das operações saque e tranferência
    """
    valor_transacao = float(input("Digite o valor desejado: "))
    return valor_transacao


def main_menu():
    """
    - Imprime no terminal as opções do menu principal
    """
    print("Login/Cadastro digite o que deseja fazer: ")
    print("1 - Login")
    print("2 - Cadastro")
    print("Outro - Sair")


def print_operacoes_sessao():
    """
   - Imprime no terminal as opções de sessão, quando o usuário está logado no sistema
   """
    print("3 - Saque")
    print("4 - Depósito")
    print("5 - Consultar Saldo")
    print("6 - Transferência")
    print("Outro - Sai da Sessão")


def escolhe_operacao(count_event):
    """
    :param count_event: Contador de eventos do relógio
    - Primeiro imprime na tela as opções para o usuário de login/cadastro.
    - Se o usuário escolher cadastro, ele cria um cadastro no banco e volta para a tela.
    - Se o usuário escolher login, deve entrar com seu rg e senha para se autenticar no sistema.
    """
    main_menu()
    operacao_desejada = input("Opção: ")
    count, continuar = switch_main_menu(operacao_desejada, count_event)
    return count, continuar
