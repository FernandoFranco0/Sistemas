import sqlite3 as sql

def criar_estrutura_banco():
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        cur.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='clientes' ''')
        if cur.fetchone()[0] != 1:
            cur.execute("""
                        CREATE TABLE if not exists clientes (
                            id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            nome    TEXT NOT NULL,
                            rg  VARCHAR(13) NOT NULL,
                            senha VARCHAR(6),
                            saldo   REAL
                            );
                        """)
        if not cliente_existe_por_nome('adm'):
            cur.execute("INSERT INTO clientes(nome, rg, senha, saldo) VALUES ('adm', '11.111.111-11', '123456', 0)")
        con.commit()


def cliente_existe_por_nome(nome_cliente):
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        exists = True
        cur.execute(''' SELECT count(*) FROM clientes WHERE nome=? ''', (nome_cliente,))
        query_result = cur.fetchone()[0]
        if query_result == 0:
            exists = False
        return exists


def criar_cliente(cliente):
    print("Criacao de cliente")
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        ( n, r, s ) = cliente
        info_cliente = (n, r, s, 0)
        if not cliente_existe_por_nome( n ):
            cur.execute(''' INSERT INTO clientes(nome, rg, senha, saldo) VALUES (?,?,?,?) ''', info_cliente)
        con.commit()


def verifica_por_rg_senha(rg, senha):
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        eh_habilitado = True
        if cliente_existe_por_rg(rg):
            cur.execute(''' SELECT count(*) FROM clientes WHERE rg=? AND senha=? ''', (rg, senha))
        query_result = cur.fetchall()
        if query_result is not None:
            eh_habilitado = False
        return eh_habilitado


def cliente_existe_por_rg(rg):
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        existe = True

        cur.execute(''' SELECT count(*) FROM clientes WHERE rg=? ''', (rg,))

        resultado = cur.fetchone()[0]

        if resultado == 0:
            existe = False

        return existe

def get_nome_cliente(rg):
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        cur.execute(''' SELECT nome, saldo FROM clientes WHERE rg=? ''', (rg,))
        nome, saldo = cur.fetchall()[0]
        return nome, saldo


def get_saldo(rg):
    with sql.connect('clientes.db') as con:
        cur = con.cursor()

        cur.execute(''' SELECT saldo from clientes where rg=? ''', (rg,))
        saldo = cur.fetchall()[0]

        return saldo[0]


def atualizar_saldo(valor, rg):
    with sql.connect('clientes.db') as con:
        cur = con.cursor()
        cur.execute(''' UPDATE clientes SET saldo=? WHERE rg=? ''', (valor, rg,))
        con.commit()
