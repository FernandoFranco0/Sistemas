import socket

def receiveInt(c:socket):
    """Int via socket sempre será um inteiro de oito bytes com sinal"""
    recv_int =  c.recv(8)
    return int.from_bytes(recv_int, 'little')

def sendInt(c:socket, num:int):
    """Envia inteiro via socket"""
    c.send(int.to_bytes(num, 8, 'little'))

def receiveString(c:socket, dencoder:str='utf-8'):
    """String via socket sempre será uma string menor que 4096 bytes. Por padrão o encoder é ascii"""
    try:
        tam_str = receiveInt(c)
        msg = c.recv(tam_str)
        return msg.decode(dencoder)
    except Exception as e:
            raise e

def sendString(c:socket, string:str, encoder:str='utf-8'):
    """Envia string via socket"""
    encoded_string = string.encode(encoder)
    len_string = len(encoded_string)
    sendInt(c, len_string)
    c.send(encoded_string)