import os
from sqlite3 import Error, connect

class Banco_de_dados:
    def __init__(self, db_nome="condominio.sqlite"):
        """
        Cria o arquivo na pasta do projeto
        :param db_nome: Nome do banco de dados
        """
        self.db_nome = os.path.join(os.path.dirname(__file__), db_nome)
        self.conn = None

    def conectar(self, criar_tabelas=False):
        """
        Abre uma conexão com o banco de dados.
        :param criar_tabelas: Define se será criado as tabelas ao realizar a conexão (True ou False).
        :return: Retorna True se conextar com sucesso, False se não.
        """
        try:
            self.conn = connect(self.db_nome)
            if criar_tabelas:
                self.criar_tabelas()
            return True
        except Error as e:
            print(f"Erro ao conectar: {e}")
            return False

    def tabela_administracao(self):
        """
        Cria a tabela "administracao" no banco de dados.
        """
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
            except Error as e:
                print(f"Erro ao criar tabela Administracao: {e}")

    def tabela_morador(self):
        """
        Cria a tabela "morador" referente aos moradores do condominio.
        """
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS morador(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        telefone TEXT UNIQUE NOT NULL,
                        cpf TEXT UNIQUE NOT NULL,
                        bloco TEXT NOT NULL,
                        apartamento TEXT NOT NULL,
                        ativo INTEGER DEFAULT 1
                    )"""
                )
                self.conn.commit()
            except Error as e:
                print(f"Erro ao criar tabela Morador: {e}")

    def tabela_visitante(self):
        """
        Cria a tabela "visitante" referente aos visitantes do condominio.
        """
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visitante(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT UNIQUE NOT NULL
                    )"""
                )
                self.conn.commit()
            except Error as e:
                print(f"Erro ao criar tabela Visitante: {e}")

    def tabela_ocorrencias(self):
        """
        Cria a tabela "ocorrencias" para registrar as ocorrencias feitas no condominio.
        """
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ocorrencias(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        motivo TEXT NOT NULL,
                        descricao TEXT NOT NULL,
                        morador_id INTEGER,
                        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status TEXT CHECK (status IN ('aberto', 'em andamento', 'fechado')) DEFAULT 'aberto',
                        administracao_id INTEGER,
                        
                        FOREIGN KEY (morador_id) REFERENCES Morador(id),
                        FOREIGN KEY (administracao_id) REFERENCES administracao(id)
                    )"""
                )
                self.conn.commit()
            except Error as e:
                print(f"Erro ao criar tabela Ocorrencias: {e}")

    def tabela_visitas(self):
        """
        Cria a tabela "visitas" para registrar as visitas feitas no condominio.
        :return:
        """
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
            except Error as e:
                print(f"Erro ao criar tabela Visitas: {e}")

    def criar_tabelas(self):
        """
        Cria todas as tabelas necessárias no banco de dados.
        """
        self.tabela_administracao()
        self.tabela_morador()
        self.tabela_visitante()
        self.tabela_ocorrencias()
        self.tabela_visitas()