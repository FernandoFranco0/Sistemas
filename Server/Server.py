"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
import os
import socket
import sys
from _thread import *

from Utils.Requisicoes import Requisicoes
from Utils.Respostas import Respostas
from Repository.banco_de_dados import *
from models.Cliente import Cliente
from Utils.SocketUtils import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

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
        if Requisicoes(cabecalho[0]).value == Requisicoes.LOGIN.value:
            self.login(conexao, cabecalho)
        elif Requisicoes(cabecalho[0]).value == Requisicoes.CADASTRO.value:
            self.cadastro(conexao, cabecalho)
        elif Requisicoes(cabecalho[0]).value == Requisicoes.SAQUE.value:
            self.saque(conexao, cabecalho)
        elif Requisicoes(cabecalho[0]).value == Requisicoes.DEPOSITO.value:
            self.deposito(conexao, cabecalho)
        elif Requisicoes(cabecalho[0]).value == Requisicoes.TRANSFERENCIA.value:
            self.transferencia(conexao, cabecalho)
        elif Requisicoes(cabecalho[0]).value == Requisicoes.CONSULTA_SALDO.value:
            self.saldo_cliente(conexao, cabecalho)
        else:
            print("Algo deu errado | LOG")
    
    def cadastro(self, conexao, cabecalho):
        """
        - Cadastra um novo cliente no banco
        """
        cliente = Cliente(
            nome=cabecalho[1],
            rg=cabecalho[2],
            senha=cabecalho[3])
        criar_cliente(cliente)
        sendString( conexao, Respostas.SUCCESS.value )


    def saldo_cliente(self, conexao, cabecalho):
        """
        - Consulta o saldo do cliente
        """
        saldo = get_saldo(cabecalho[1])
        sendString( conexao, Respostas.SUCCESS.value + '#' + str(saldo) )


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
            sendString( conexao, Respostas.FORBIDDEN.value + '#' + 'Saldo insuficiente' )
        else:
            saldo_novo = saldo_atual - valor
            atualizar_saldo(saldo_novo, rg)
            saldo_novo_favorecido = saldo_atual_favorecido + valor
            atualizar_saldo(saldo_novo_favorecido, rg_favorecido)
            sendString( conexao, Respostas.SUCCESS.value + '#' + str(saldo_novo) + '#' + str(saldo_novo_favorecido) )


    def deposito(self, conexao, cabecalho):
        """
        - Faz a operação de depósito na conta do cliente
        """
        valor = float(cabecalho[1])
        rg = cabecalho[2]
        saldo_atual = get_saldo(rg)
        saldo_novo = saldo_atual + valor
        atualizar_saldo(saldo_novo, rg)
        sendString( conexao, Respostas.SUCCESS.value + '#' + str(saldo_novo) )


    def saque(self, conexao, cabecalho):
        """
        - Faz a operação de saque para o cliente
        """
        valor = float(cabecalho[1])
        rg = cabecalho[2]
        saldo_atual = get_saldo(rg)
        if saldo_atual < valor:
            sendString( conexao, Respostas.FORBIDDEN.value + '#' + 'Saldo insuficiente' )
        else:
            saldo_novo = saldo_atual - valor
            atualizar_saldo(saldo_novo, rg)
            sendString( conexao, Respostas.SUCCESS.value + '#' + str(saldo_novo) )



    def login(self, conexao, cabecalho):
        """
        - Faz o login de um usuário no contexto do sistema
        """
        if not verifica_por_rg_senha(rg=cabecalho[1], senha=cabecalho[2]):
            cliente_nome, cliente_saldo = get_nome_cliente(rg=cabecalho[1])
            sendString( conexao, Respostas.SUCCESS.value + '#' + cliente_nome + '#' + str(cliente_saldo) )
        else:
            sendString( conexao, Respostas.FORBIDDEN.value, 'Dados de usuário incorretos' )

    
    def Run(self):
        while True:
            client_socket, address = server_socket.accept()
            start_new_thread(self.gerenciar_cliente_thread, (client_socket, address))
            cont_thread += 1
            print("Evento: " + str(cont_thread) + " realizado.")

    def gerenciar_cliente_thread(self, conexao, _endereco):
        sendString( conexao, Respostas.CONNECTED.value + '#' + str( self.LogicalClock ) )
        
        req = receiveString( conexao ).split('#')

        self.manipula_requisicoes(req, conexao)

        conexao.close()
