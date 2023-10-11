"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
from enum import Enum


class Repostas(Enum):
    INTERNAL_ERROR = '0'
    CONNECTED = '1'
    SUCCESS = '2'
    FORBIDDEN = '3'
