from Client.Client import Client
from Utils.Consts import Requisicoes
from Utils.Consts import Respostas

def switch_main_menu(opcao : int):
    """
    - Faz uma requisição ao servidor para encontrar o cliente na base de dados
    - Caso a resposta seja sucesso, abre uma sessão para o usuário
    - Caso não exista o usuário na base, volta para o menu principal
    """
    if opcao == Requisicoes.CADASTRO.value:
        rg_cliente = input("Digite o rg: ")
        nome_cliente = input("Digite o nome: ")
        senha_cliente = input("Digite a sua senha: ")

        client = Client( rg_cliente, nome_cliente, senha_cliente)
        client.requisicao_cadastro()
        
    elif opcao == Requisicoes.LOGIN.value:
        rg_cliente = input("Digite o rg: ")
        senha_cliente = input("Digite a sua senha: ")

        client = Client(rg_cliente,senha_cliente)
        resposta_requisicao, mensagem = client.requisicao_login()
        if resposta_requisicao == Respostas.SUCCESS:
            return True, client, True
        else:
            print(f"{resposta_requisicao} {mensagem}")

    else:
        return False, None, False
    
    return True, None, False

def switch_operacao(operacao : str, client : Client):
    """
    - Direciona a operação desejada no menu da sessão
    """
    if operacao == Requisicoes.SAQUE.value:
        valor_saque = float(input("Digite o valor desejado: "))
        menssagem_requisicao, novo_saldo = client.requisicao_saque(valor_saque)
        print(f"Saque de {str(valor_saque)} na conta. Novo Saldo: {novo_saldo}.")
    
    elif operacao == Requisicoes.DEPOSITO.value:
        valor_deposito = float(input("Digite o valor desejado: "))
        menssagem_requisicao, novo_saldo = client.requisicao_deposito(valor_deposito)
        print(f"Depósito de  {str(valor_deposito)} na conta. Novo Saldo: {novo_saldo}.")

    elif operacao == Requisicoes.CONSULTA_SALDO.value:
        menssagem_requisicao, saldo = client.requisicao_consultar_saldo()
        print(f"O seu saldo é: {saldo}.")
    
    elif operacao == Requisicoes.TRANSFERENCIA.value:
        rg_destino = input("Digite o rg do usuario da conta de destino: ")
        valor_transferencia = float(input("Digite o valor desejado: "))
        mensagem, novo_saldo, novo_saldo_favorecido = client.requisicao_transferencia(valor_transferencia, rg_destino)
        print(f"Transferência com valor de {str(valor_transferencia)} feita de: {client.rg} para: {rg_destino}. Novo Saldo: {str(novo_saldo)}.")

    else:
        return False
    
    return True


if __name__ == '__main__':

    continuar = True
    loggedIn = False

    while continuar:
        if loggedIn:
            print("Digite o número do que deseja fazer: ")
            print("3 - Saque")
            print("4 - Depósito")
            print("5 - Consultar Saldo")
            print("6 - Transferência")
            print("Outro - Sai da Sessão")
            operacao_desejada = input("Opção: ")

            loggedIn  = switch_operacao(operacao_desejada, loggedClient )
        else: 
            print("Digite o número do que deseja fazer: ")
            print("1 - Login")
            print("2 - Cadastro")
            print("Outro - Sair")
            operacao_desejada = input("Opção: ")
            
            continuar, loggedClient, loggedIn = switch_main_menu(operacao_desejada)
            
        if( loggedClient ):
            print(f"Relogio do client com rg {loggedClient.rg} : {loggedClient.LogicalClock}")