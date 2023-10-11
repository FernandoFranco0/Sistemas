"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
import os
import socket
import sys
from _thread import *

from Constantes.Respostas import Repostas
from Repository.banco_de_dados import *
from Server.RequisicoesServer import manipula_requisicoes

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


def gerenciar_cliente_thread(conexao, _endereco):
    conexao.send(str.encode(Repostas.CONNECTED.value))
    while True:
        dados = conexao.recv(BUFFER_SIZE)
        requisicao = dados.decode('utf-8')
        cabecalho = str(requisicao).split('#')

        if not dados:
            break

        manipula_requisicoes(cabecalho, conexao)

    conexao.close()


while True:
    client_socket, address = server_socket.accept()
    start_new_thread(gerenciar_cliente_thread, (client_socket, address))
    cont_thread += 1
    print("Evento: " + str(cont_thread) + " realizado.")
