"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
class Cliente:
    def __init__(self, nome, rg, senha, saldo=0):
        self.nome = nome
        self.rg = rg
        self.senha = senha
        self.saldo = saldo

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_rg(self):
        return self.rg

    def set_rg(self, rg):
        self.rg = rg

    def get_senha(self):
        return self.senha

    def set_senha(self, senha):
        self.senha = senha

    def get_saldo(self):
        return self.saldo

    def set_saldo(self, saldo):
        self.saldo = saldo
