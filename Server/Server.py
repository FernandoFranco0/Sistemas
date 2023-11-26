"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""

import socket
from _thread import *

import sys, os
sys.path.append('../')

from Utils.Requisicoes import Requisicoes
from Utils.Respostas import Respostas
from Repository.banco_de_dados import *
from Utils.SocketUtils import *

""" 
AF_INET = Tipo da família de endereços, que no caso é o host:port
SOCK_STREAM = O socket é do tipo TCP 
"""
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
"""
Por convenção, adotaremos essa porta
"""
PORT = 1233
cont_thread = 0

criar_estrutura_banco()

"""
Liga o servidor via soquete, passando o endereço do host e a porta e faz o tratamento dos possíveis erros
"""
try:
    server_socket.bind((HOST, PORT))
except socket.error as error:
    print(str(error))

"""
Quantidade de conexões simultâneas que o socket aceita
"""
server_socket.listen(5)

BUFFER_SIZE = 4096


class Server:
    def __init__(self, ):
        self.LogicalClock = 0

    def manipula_requisicoes(self, cabecalho, conexao):
        """
        :param cabecalho:
        :param conexao:
        :return:
        - Direciona o tipo de requisição
        """

        self.LogicalClock += 1

        if Requisicoes( cabecalho[0] ) == Requisicoes.LOGIN:
            self.login( conexao, cabecalho)
        elif Requisicoes( cabecalho[0] ) == Requisicoes.CADASTRO:
            self.cadastro( conexao, cabecalho)
        elif Requisicoes( cabecalho[0] ) == Requisicoes.SAQUE:
            self.saque( conexao, cabecalho)
        elif Requisicoes( cabecalho[0] ) == Requisicoes.DEPOSITO:
            self.deposito( conexao, cabecalho)
        elif Requisicoes( cabecalho[0] ) == Requisicoes.TRANSFERENCIA:
            self.transferencia( conexao, cabecalho)
        elif Requisicoes( cabecalho[0] ) == Requisicoes.CONSULTA_SALDO:
            self.saldo_cliente( conexao, cabecalho)
        else:
            print("Algo deu errado | LOG")
    
    def cadastro(self, conexao, cabecalho):
        """
        - Cadastra um novo cliente no banco
        """
        criar_cliente( ( cabecalho[1], cabecalho[2], cabecalho[3] ) )
        sendString( conexao, f"{Respostas.SUCCESS.value}#{str(self.LogicalClock)}" )

    def saldo_cliente(self, conexao, cabecalho):
        """
        - Consulta o saldo do cliente
        """
        saldo = get_saldo(cabecalho[1])
        sendString( conexao, f"{Respostas.SUCCESS.value}#{str(saldo)}#{str(self.LogicalClock)}" )

    def transferencia(self, conexao, cabecalho):
        """
        - Faz uma transferência entre conta de clientes do banco
        """
        valor = float(cabecalho[1])
        rg = cabecalho[2]
        rg_favorecido = cabecalho[3]
        saldo_atual = get_saldo(rg)
        saldo_atual_favorecido = get_saldo(rg_favorecido)
        if saldo_atual < valor:
            sendString( conexao, f"{Respostas.FORBIDDEN.value}#Saldo insuficiente#{str(self.LogicalClock)}" )
        else:
            saldo_novo = saldo_atual - valor
            atualizar_saldo(saldo_novo, rg)
            saldo_novo_favorecido = saldo_atual_favorecido + valor
            atualizar_saldo(saldo_novo_favorecido, rg_favorecido)
            sendString( conexao, f"{Respostas.SUCCESS.value}#{str(saldo_novo)}#{str(saldo_novo_favorecido)}#{str(self.LogicalClock)}" )

    def deposito(self, conexao, cabecalho):
        """
        - Faz a operação de depósito na conta do cliente
        """
        valor = float(cabecalho[1])
        rg = cabecalho[2]
        saldo_atual = get_saldo(rg)
        saldo_novo = saldo_atual + valor
        atualizar_saldo(saldo_novo, rg)
        sendString( conexao, f"{Respostas.SUCCESS.value}#{str(saldo_novo)}#{str(self.LogicalClock)}" )

    def saque(self, conexao, cabecalho):
        """
        - Faz a operação de saque para o cliente
        """
        valor = float(cabecalho[1])
        rg = cabecalho[2]
        saldo_atual = get_saldo(rg)
        if saldo_atual < valor:
            sendString( conexao, f"{Respostas.FORBIDDEN.value}#Saldo insuficiente#{str(self.LogicalClock)}" )
        else:
            saldo_novo = saldo_atual - valor
            atualizar_saldo(saldo_novo, rg)
            sendString( conexao, f"{Respostas.SUCCESS.value}#{str(saldo_novo)}#{str(self.LogicalClock)}" )

    def login(self, conexao, cabecalho):
        """
        - Faz o login de um usuário no contexto do sistema
        """
        if not verifica_por_rg_senha(rg=cabecalho[1], senha=cabecalho[2]):
            cliente_nome, cliente_saldo = get_nome_cliente(rg=cabecalho[1])
            sendString( conexao, f"{Respostas.SUCCESS.value}#{cliente_nome}#{str(cliente_saldo)}#{str(self.LogicalClock)}" )
        else:
            sendString( conexao, f"{Respostas.FORBIDDEN.value}#Dados de usuário incorretos#{str(self.LogicalClock)}" )

    def Run(self):
        while True:
            client_socket, address = server_socket.accept()
            start_new_thread(self.gerenciar_cliente_thread, (client_socket, address))

    def gerenciar_cliente_thread(self, conexao, _endereco):
        print(f"Conectado com: {_endereco[0]}:{_endereco[1]} Clock logico do servidor : {self.LogicalClock}")
        self.LogicalClock += 1
        sendString( conexao, f"{Respostas.CONNECTED.value}#{str( self.LogicalClock )}" )
        
        req = receiveString( conexao ).split('#')
        self.LogicalClock = max( self.LogicalClock, int( req[-1] ) ) 

        self.manipula_requisicoes(req, conexao)

        print(f"Relogio do servidor : {self.LogicalClock}")

        conexao.close()

if __name__ == '__main__':
    server = Server()
    server.Run()