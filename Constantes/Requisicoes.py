"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
from enum import Enum


class Requisicoes(Enum):
    LOGIN = '1'
    CADASTRO = '2'
    SAQUE = '3'
    DEPOSITO = '4'
    CONSULTA_SALDO = '5'
    TRANSFERENCIA = '6'
    OBTER_LISTA_CLIENTES = '7'
