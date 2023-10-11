"""
@author: Álvaro Souza Oliveira
@author: Carlos Mosselman Cabral Neto
@author: Vanessa Machado Araújo
"""
from InterfaceLinhaDeComando import escolhe_operacao

"""
- Contador do relógio lógico
"""
count_event = 0


def __main__():
    """
    - Função principal do programa Client, a interface do usuário.
    - Faz um loop na interface de linha de comando e lê as entradas do usuário.
    """
    continuar = True
    while continuar:
        count, continuar = escolhe_operacao(count_event)
        print("Relógio principal: " + str(count))


if __name__ == '__main__':
    __main__()
