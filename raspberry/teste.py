from conectarBD import Conect

conexao = Conect()

conexao.doQuery("select", "nome", "tb_cliente", "true")

conexao.closeCon
