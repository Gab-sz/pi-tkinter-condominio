import os
import sqlite3

class Banco_de_dados:
    def __init__(self, nome="condominio"):
        self.nome = os.path.join(os.path.dirname(__file__), nome)
        self.conn = None

    def conectar(self):
        try:
            self.conn = sqlite3.connect(self.nome)
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def criar