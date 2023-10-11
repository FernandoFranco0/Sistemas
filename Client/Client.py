"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
import socket

from Constantes.Requisicoes import Requisicoes
from Constantes.Respostas import Repostas

HOST = '127.0.0.1'
PORT = 1233
BUFFER_SIZE = 4096
MENSAGEM_ERRO_DESCONHECIDO = 'Erro desconhecido'
MENSAGEM_SERVIDOR_SEM_RESPOSTA = 'Erro de conexão com o servidor: sem resposta'
count_event = 0


def requisicao_cadastro(nome, rg, senha):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            if Repostas(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Repostas.CONNECTED:

                request_cadastro = Requisicoes.CADASTRO.value + '#' + nome + '#' + rg + '#' + senha
                client_socket.send(str.encode(request_cadastro))

                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                status = Repostas(resposta)
                if status == Repostas.SUCCESS:
                    return Repostas.SUCCESS,
                else:
                    return Repostas.Responses.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO
            else:
                return (Repostas.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO)
        except socket.error as error:
            print(str(error))
            return (Repostas.INTERNAL_ERROR, str(error))


def requisicao_login(rg, senha):
    """
    Contecta-se com o servidor e faz uma requisição para validar o usuário para fazer o login na aplicação
    rg: rg do usuário
    senha: senha do usuário
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            if Repostas(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Repostas.CONNECTED:
                request_cadastro = Requisicoes.LOGIN.value + '#' + rg + '#' + senha
                client_socket.send(str.encode(request_cadastro))

                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')
                status = Repostas(resposta[0])

                if status == Repostas.SUCCESS:
                    nome = resposta[1]
                    saldo = resposta[2]

                    return Repostas.SUCCESS, nome, saldo
                else:
                    return Repostas.INTERNAL_ERROR, MENSAGEM_ERRO_DESCONHECIDO
            else:
                return Repostas.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA

        except socket.error as error:
            print(str(error))
            return Repostas.INTERNAL_ERROR, str(error)


def requisicao_saque(valor, rg):
    """
    Contecta-se com o servidor e faz uma requisição para realizar o saque
    valor: valor que será retirado
    rg: rg do cliente que está realizando a ação
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            if Repostas(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Repostas.CONNECTED:
                request_saque = Requisicoes.SAQUE.value + '#' + str(valor) + '#' + rg
                client_socket.send(str.encode(request_saque))
                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')

                resposta = resposta.split('#')
                status = Repostas(resposta[0])

                if status == Repostas.SUCCESS:
                    novo_saldo = resposta[1]
                    return Repostas.SUCCESS, novo_saldo
                else:
                    mensagem = resposta[1]
                    return status, mensagem
            else:
                return Repostas.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA

        except socket.error as error:
            print(str(error))
            return Repostas.INTERNAL_ERROR, str(error)


def requisicao_deposito(valor, rg):
    """
    Contecta-se com o servidor e faz uma requisição para realiazr o depósito
    valor: valor que será adicionado à conta
    rg: rg do cliente que receberá o valor
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            if Repostas(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Repostas.CONNECTED:
                request_saque = Requisicoes.DEPOSITO.value + '#' + str(valor) + '#' + rg
                client_socket.send(str.encode(request_saque))

                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')

                status = Repostas(resposta[0])
                if status == Repostas.SUCCESS:
                    novo_saldo = resposta[1]
                    return (Repostas.SUCCESS, novo_saldo)
                else:
                    mensagem = resposta[1]
                    return (status, mensagem)
            else:
                return (Repostas.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA)
        except socket.error as error:
            print(str(error))
            return (Repostas.INTERNAL_ERROR, str(error))


def requisicao_transferencia(valor, rg, rg_favorecido):
    """
    Contecta-se com o servidor e faz uma requisição para realizar uma transferência entre clientes
    valor: valor que será transferido
    rg: rg do cliente que está realizando a operação de transferência
    rg_favorecido: rg do cliente que foi selecionado para receber o valor da transferência
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            if Repostas(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Repostas.CONNECTED:
                request_transf = Requisicoes.TRANSFERENCIA.value + '#' + str(valor) + '#' + rg + '#' + rg_favorecido
                client_socket.send(str.encode(request_transf))

                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')

                status = Repostas(resposta[0])
                if status == Repostas.SUCCESS:
                    novo_saldo = resposta[1]
                    novo_saldo_favorecido = resposta[2]
                    return Repostas.SUCCESS, novo_saldo, novo_saldo_favorecido
                else:
                    mensagem = resposta[1]
                    return status, mensagem
            else:
                return Repostas.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA
        except socket.error as error:
            print(str(error))
            return Repostas.INTERNAL_ERROR, str(error)


def requisicao_consultar_saldo(rg):
    """
    Contecta-se com o servidor e faz uma requisição para obter o saldo atual do cliente
    rg: rg do cliente
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            if Repostas(client_socket.recv(BUFFER_SIZE).decode('utf-8')) == Repostas.CONNECTED:
                request_consulta = Requisicoes.CONSULTA_SALDO.value + '#' + rg
                client_socket.send(str.encode(request_consulta))

                resposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                resposta = resposta.split('#')

                status = resposta[0]
                if status == Repostas.SUCCESS.value:
                    saldo = resposta[1]
                    return Repostas.SUCCESS, saldo
                else:
                    mensagem = resposta[1]
                    return status, mensagem
            else:
                return Repostas.INTERNAL_ERROR, MENSAGEM_SERVIDOR_SEM_RESPOSTA

        except socket.error as error:
            print(str(error))
            return (Repostas.INTERNAL_ERROR, str(error))
