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
                        telefone TEXT UNIQUE NOT NULL,
                        login TEXT UNIQUE NOT NULL,
                        senha TEXT NOT NULL,
                        tipo TEXT NOT NULL CHECK (tipo IN ('porteiro', 'sindico')),
                        ativo INTEGER DEFAULT 1
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Administracao: {e}")

    def tabela_morador(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS morador(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        telefone TEXT UNIQUE NOT NULL,
                        bloco TEXT NOT NULL,
                        apartamento TEXT NOT NULL,
                        ativo INTEGER DEFAULT 1
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Morador: {e}")

    def tabela_visitante(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visitante(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT UNIQUE NOT NULL,
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Visitante: {e}")

    def tabela_ocorrencias(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ocorrencias(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        motivo TEXT NOT NULL,
                        descricao TEXT NOT NULL,
                        morador_id INTEGER,
                        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
                        status INTEGER CHECK (status IN ('aberto', 'em andamento', 'fechado')) DEFAULT 'aberto',
                        administracao_id INTEGER,
                        
                        FOREIGN KEY (morador_id) REFERENCES Morador(id),
                        FOREIGN KEY (administracao_id) REFERENCES administracao(id),
                    )"""
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Ocorrencias: {e}")

    def tabela_visitas(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visitas(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        visitante_id INTEGER NOT NULL,
                        entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
                        morador_id INTEGER NOT NULL,
                        administracao_id INTEGER NOT NULL,

                        FOREIGN KEY (visitante_id) REFERENCES visitante(id),
                        FOREIGN KEY (morador_id) REFERENCES morador(id),
                        FOREIGN KEY (administracao_id) REFERENCES administracao(id)
                    )"""
                               )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Erro ao criar tabela Visitas: {e}")

    def criar_tabelas(self):
        self.tabela_administracao()
        self.tabela_morador()
        self.tabela_visitante()
        self.tabela_ocorrencias()
        self.tabela_visitas()