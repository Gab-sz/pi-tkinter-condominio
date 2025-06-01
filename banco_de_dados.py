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
        Abre uma conexão com o banco de dados, se ja existir uma, fecha para evitar multiplas conexões.
        :param criar_tabelas: Define se será criado as tabelas ao realizar a conexão (True ou False).
        :return: Retorna True se conextar com sucesso, False se não.
        """
        try:
            if self.conn:
                self.conn.close()
            self.conn = connect(self.db_nome)
            if criar_tabelas:
                self.criar_tabelas()
            return True
        except Error as e:
            print(f"Erro ao conectar: {e}")
            self.conn = None
            return False

    def desconectar(self):
        """
        Fecha a conexao com o banco de dados.
        """
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
            except Error as e:
                print(f"Erro ao desconectar: {e}")

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
                        visitante_nome TEXT NOT NULL,
                        visitante_cpf TEXT NOT NULL,
                        entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
                        morador_id INTEGER NOT NULL,
                        administracao_id INTEGER NOT NULL,

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
        if self.conectar():
            self.tabela_administracao()
            self.tabela_morador()
            self.tabela_ocorrencias()
            self.tabela_visitas()
            self.desconectar()
        else:
            print("Falha ao criar tabelas")

    def listar_moradores_ativos(self):
        """
        Busca todos os moradores registrados no banco de dados.
        :return: lista com moradores ativos no sistema.
        """
        moradores = []
        if not self.conectar():
            print("Falha no banco de dados")
            return moradores

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, nome, bloco, apartamento
                FROM morador
                WHERE ativo=1
                ORDER BY nome ASC
            """)
            moradores = cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar moradores: {e}")
        finally:
            self.desconectar()
        return moradores

    def registrar_ocorrencia_db(self, motivo, descricao, morador_id, adm_id):
        if not self.conectar():
            print("ERRO DE CONEXAO")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO ocorrencias (motivo, descricao, morador_id, administracao_id)
                VALUES (?, ?, ?, ?)
            """, (motivo, descricao, morador_id, adm_id))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Erro ao inserir ocorrência: {e}")
            return False
        finally:
            self.desconectar()

<<<<<<< HEAD
            def listar_visitas_com_detalhes(self):
                """Retorna uma lista de visitas no formato: (visitante_nome, visitante_cpf, morador_nome, data_visita)"""
                visitas = []
                if not self.conectar():
                    return visitas

                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        SELECT v.nome, v.cpf, m.nome, vs.entrada
                        FROM visitas vs
                        JOIN visitante v ON vs.visitante_id = v.id
                        JOIN morador m ON vs.morador_id = m.id
                        ORDER BY vs.entrada DESC
                    """)
                    visitas = cursor.fetchall()
                except Error as e:
                    print(f"Erro ao listar visitas: {e}")
                finally:
                    self.desconectar()
                return visitas

            def listar_ocorrencias(self):
                ocorrencias = []
                if not self.conectar():
                    return ocorrencias
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        SELECT o.id, o.motivo, o.descricao, m.nome, o.status
                        FROM ocorrencias o
                        JOIN morador m ON o.morador_id = m.id
                    """)
                    ocorrencias = cursor.fetchall()
                except Error as e:
                    print(f"Erro ao listar ocorrências: {e}")
                finally:
                    self.desconectar()
                return ocorrencias

            def listar_visitantes_por_morador(self, morador_id):
                visitantes = []
                if not self.conectar():
                    return visitantes
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        SELECT v.nome, v.cpf
                        FROM visitas vs
                        JOIN visitante v ON vs.visitante_id = v.id
                        WHERE vs.morador_id = ?
                    """, (morador_id,))
                    visitantes = cursor.fetchall()
                except Error as e:
                    print(f"Erro ao listar visitantes do morador: {e}")
                finally:
                    self.desconectar()
                return visitantes
=======
    def registrar_visita_db(self, nome_visita, cpf_visita, morador_id, adm_id):
        if not self.conectar():
            print("ERRO DE CONEXAO")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO visitas (visitante_nome, visitante_cpf, morador_id, administracao_id)
                VALUES (?, ?, ?, ?)
            """, (nome_visita, cpf_visita, morador_id, adm_id))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Erro ao inserir ocorrência: {e}")
            return False
        finally:
            self.desconectar()
>>>>>>> adc9b041dcce15d3051b01dae3efaadfe1c9dc38
