"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
from enum import Enum


class Requisicoes(Enum):
    LOGIN = '1'
    CADASTRO = '2'
    SAQUE = '1'
    DEPOSITO = '2'
    CONSULTA_SALDO = '3'
    TRANSFERENCIA = '4'
    OBTER_LISTA_CLIENTES = '5'
