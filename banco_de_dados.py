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

    def tabela_administracao(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS administracao(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        login TEXT UNIQUE NOT NULL,
                        senha TEXT NOT NULL,
                        tipo TEXT NOT NULL CHECK (tipo IN ('porteiro', 'sindico'))
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criat tabela Administracao: {e}")