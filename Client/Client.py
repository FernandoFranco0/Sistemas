"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
import socket

from Utils.Requisicoes import Requisicoes
from Utils.Respostas import Respostas
from Utils.SocketUtils import *

class Client:
    BUFFER_SIZE = 4096
    MENSAGEM_ERRO_DESCONHECIDO = 'Erro desconhecido'
    MENSAGEM_SERVIDOR_SEM_RESPOSTA = 'Erro de conexão com o servidor: sem resposta'
    
    def __init__(self, rg, senha, host='127.0.0.1', port=1233):
        self.rg = rg
        self.senha = senha
        self.host = host
        self.port = port
        self.LogicalClock = 0

    def requisicao_cadastro(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect( (self.host, self.port) )
                if Respostas( receiveString( client_socket ) ) == Respostas.CONNECTED:

                    request = Requisicoes.CADASTRO.value + '#' + self.nome + '#' + self.rg + '#' + self.senha
                    
                    resposta = self.request( request, client_socket )
                    
                    status = Respostas( resposta )
                    if status == Respostas.SUCCESS:
                        return Respostas.SUCCESS,

                    return status, self.MENSAGEM_ERRO_DESCONHECIDO

                return Respostas.INTERNAL_ERROR, self.MENSAGEM_ERRO_DESCONHECIDO
            
            except socket.error as error:
                print( str(error) )
                return  Respostas.INTERNAL_ERROR, str(error) 


    def requisicao_login(self):
        """
        Contecta-se com o servidor e faz uma requisição para validar o usuário para fazer o login na aplicação
        rg: rg do usuário
        senha: senha do usuário
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.host, self.port))
                if Respostas( receiveString( client_socket ) ) == Respostas.CONNECTED:

                    request = Requisicoes.LOGIN.value + '#' + self.rg + '#' + self.senha

                    resposta = self.request( request, client_socket )

                    resposta = resposta.split('#')

                    status = Respostas( resposta[0] )

                    if status == Respostas.SUCCESS:
                        self.nome = resposta[1]
                        self.saldo = resposta[2]

                        return status, self.nome, self.saldo
                    
                    return status, self.MENSAGEM_ERRO_DESCONHECIDO
                
                return Respostas.INTERNAL_ERROR, self.MENSAGEM_SERVIDOR_SEM_RESPOSTA

            except socket.error as error:
                print(str(error))
                return Respostas.INTERNAL_ERROR, str(error)


    def requisicao_saque(self, valor):
        """
        Contecta-se com o servidor e faz uma requisição para realizar o saque
        valor: valor que será retirado
        rg: rg do cliente que está realizando a ação
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.host, self.port))
                if Respostas( receiveString( client_socket ) ) == Respostas.CONNECTED:

                    request = Requisicoes.SAQUE.value + '#' + str(valor) + '#' + self.rg

                    resposta = self.request( request, client_socket )

                    resposta = resposta.split('#')

                    status = Respostas( resposta[0] )

                    if status == Respostas.SUCCESS:
                        self.saldo = resposta[1]
                        return status, self.saldo
                    
                    return status, resposta[1]

                return Respostas.INTERNAL_ERROR, self.MENSAGEM_SERVIDOR_SEM_RESPOSTA

            except socket.error as error:
                print(str(error))
                return Respostas.INTERNAL_ERROR, str(error)


    def requisicao_deposito(self, valor):
        """
        Contecta-se com o servidor e faz uma requisição para realiazr o depósito
        valor: valor que será adicionado à conta
        rg: rg do cliente que receberá o valor
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.host, self.port))
                if Respostas(client_socket.recv(self.BUFFER_SIZE).decode('utf-8')) == Respostas.CONNECTED:

                    request = Requisicoes.DEPOSITO.value + '#' + str(valor) + '#' + self.rg

                    resposta = self.request( request, client_socket )

                    resposta = resposta.split('#')

                    status = Respostas( resposta[0] )
                    
                    if status == Respostas.SUCCESS:
                        self.saldo = resposta[1]
                        return status, self.saldo
                        
                    return status, resposta[1]
                else:
                    return Respostas.INTERNAL_ERROR, self.MENSAGEM_SERVIDOR_SEM_RESPOSTA
            except socket.error as error:
                print(str(error))
                return Respostas.INTERNAL_ERROR, str(error)


    def requisicao_transferencia(self, valor : int, rg_favorecido : str):
        """
        Contecta-se com o servidor e faz uma requisição para realizar uma transferência entre clientes
        valor: valor que será transferido
        rg: rg do cliente que está realizando a operação de transferência
        rg_favorecido: rg do cliente que foi selecionado para receber o valor da transferência
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.host, self.port))
                if Respostas(client_socket.recv(self.BUFFER_SIZE).decode('utf-8')) == Respostas.CONNECTED:

                    request = Requisicoes.TRANSFERENCIA.value + '#' + str(valor) + '#' + self.rg + '#' + rg_favorecido

                    resposta = self.request( request, client_socket )

                    resposta = resposta.split('#')

                    status = Respostas( resposta[0] )

                    if status == Respostas.SUCCESS:
                        self.saldo = resposta[1]
                        novo_saldo_favorecido = resposta[2]
                        return status, self.saldo, novo_saldo_favorecido
                    
                    return status, resposta[1]
                else:
                    return Respostas.INTERNAL_ERROR, self.MENSAGEM_SERVIDOR_SEM_RESPOSTA
            except socket.error as error:
                print(str(error))
                return Respostas.INTERNAL_ERROR, str(error)


    def requisicao_consultar_saldo(self):
        """
        Contecta-se com o servidor e faz uma requisição para obter o saldo atual do cliente
        rg: rg do cliente
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.host, self.port))
                if Respostas(client_socket.recv(self.BUFFER_SIZE).decode('utf-8')) == Respostas.CONNECTED:

                    request = Requisicoes.CONSULTA_SALDO.value + '#' + self.rg

                    resposta = self.request( request, client_socket )
                   
                    resposta = resposta.split('#')

                    status = Respostas( resposta[0] )

                    if status == Respostas.SUCCESS:
                        self.saldo = resposta[1]
                    
                    return status, resposta[1]
                else:
                    return Respostas.INTERNAL_ERROR, self.MENSAGEM_SERVIDOR_SEM_RESPOSTA

            except socket.error as error:
                print(str(error))
                return (Respostas.INTERNAL_ERROR, str(error))
            
    def request(self,  request : str , clientSocket : socket ):
        self.LogicalClock += 1

        sendInt( clientSocket, self.LogicalClock )
        sendString( clientSocket, request ) 
        
        self.LogicalClock = max( self.LogicalClock, receiveInt( clientSocket ) )
        resposta = receiveString( clientSocket )

        return resposta
