import os
from sqlite3 import Error, connect
from tkinter import messagebox
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
            messagebox.showerror(f"Erro ao conectar: {e}")
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
                messagebox.showerror(f"Erro ao desconectar: {e}")

    # =========== FUNÇÕES DE CRIAÇÃO DE TABELAS ================

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
                messagebox.showerror(f"Erro ao criar tabela Administracao: {e}")

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
                messagebox.showerror(f"Erro ao criar tabela Morador: {e}")

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
                messagebox.showerror(f"Erro ao criar tabela Ocorrencias: {e}")

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
                messagebox.showerror(f"Erro ao criar tabela Visitas: {e}")

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
            messagebox.showerror("Falha ao criar tabelas")

    #=========== FUNÇÕES DE MORADORES ================

    def listar_moradores_ativos(self):
        """
        Busca todos os moradores registrados no banco de dados.
        :return: lista com moradores ativos no sistema.
        """
        moradores = []
        if not self.conectar():
            messagebox.showerror("Falha no banco de dados")
            return moradores

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, nome, bloco, apartamento, ativo
                FROM morador
                WHERE ativo=1
            """)
            moradores = cursor.fetchall()
        except Error as e:
            messagebox.showerror(f"Erro ao listar moradores: {e}")
        finally:
            self.desconectar()
        return moradores

    def listar_todos_moradores(self):
        """
        Busca todos os moradores registrados no banco de dados.
        :return: lista com moradores ativos no sistema.
        """
        moradores = []
        if not self.conectar():
            messagebox.showerror("Falha no banco de dados")
            return moradores

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, nome, bloco, apartamento, ativo
                FROM morador
            """)
            moradores = cursor.fetchall()
        except Error as e:
            messagebox.showerror(f"Erro ao listar moradores: {e}")
        finally:
            self.desconectar()
        return moradores

    def modificar_status_morador(self, morador_id):
        """
        Modifica o status do morador entre 0 e 1.
        :param morador_id: ID do morador que será modificado.
        :return: Retorna True se alguma linha for modificada, False se nada for modificado.
        """
        if not self.conectar():
            messagebox.showerror("ERRO DE CONEXAO")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE morador 
                SET ativo = CASE 
                    WHEN ativo = 1 THEN 0 
                        ELSE 1 
                END
                WHERE id = ?
            """, (morador_id,))
            self.conn.commit()

            if cursor.rowcount>0:
                messagebox.showinfo("STATUS MODIFICADO")
                return True
            else:
                messagebox.showinfo("NENHUM MORADOR MODIFICADO")
                return False
        except Error as e:
            messagebox.showerror(f"Erro ao modificar status: {e}")
            return False
        finally:
            self.desconectar()

    # =========== FUNÇÕES DE OCORRENCIAS ================

    def registrar_ocorrencia_db(self, motivo, descricao, morador_id, adm_id):
        """
        Registra uma ocorrencia no banco de dados.
        :param motivo: O motivo da ocorrencia.
        :param descricao: A descrição da ocorrencia.
        :param morador_id: O ID do morador que está solicitando a abertura da ocorrencia.
        :param adm_id: O ID do admin que esta logado no sistema.
        :return: Retorna True se o registro for realizado, False se ocorrer algum erro.
        """
        if not self.conectar():
            messagebox.showerror("ERRO DE CONEXAO")
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
            messagebox.showerror(f"Erro ao inserir ocorrência: {e}")
            return False
        finally:
            self.desconectar()

    def listar_ocorrencias(self):
        """
        Lista todas as ocorrencias registradas no banco de dados.
        :return: Retorna a lista de ocorrencias.
        """
        ocorrencias = []
        if not self.conectar():
            return ocorrencias
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.id, o.motivo, o.descricao, m.nome, o.data_hora, o.status
                FROM ocorrencias o
                JOIN morador m ON o.morador_id = m.id
            """)
            ocorrencias = cursor.fetchall()
        except Error as e:
            messagebox.showerror(f"Erro ao listar ocorrências: {e}")
        finally:
            self.desconectar()
            return ocorrencias

    def listar_ocorrencias_por_morador(self, morador_id):
        """
        Lista todas as ocorrencias de um morador especifico.
        :param morador_id: O ID do morador que sera feito o filtro.
        :return: Lista de ocorrencia do morador.
        """
        ocorrencias = []
        if not self.conectar(): return ocorrencias
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT motivo, status FROM ocorrencias WHERE morador_id = ? ORDER BY data_hora DESC",
                           (morador_id,))
            ocorrencias = cursor.fetchall()
        except Error as e:
            messagebox.showerror(f"Erro ao listar ocorrências do morador: {e}")
        finally:
            self.desconectar()
        return ocorrencias

    def modificar_status_ocorrencia(self, novo_status, ocorrencia_id):
        """
        Altera o status da ocorrencia para outra escolhida.
        :param novo_status: O novo status que sera dado a ocorrencia.
        :param ocorrencia_id: O id da ocorrencia que será modificado.
        :return: Retorna True se alguma linha for modificada, False se nada for modificado.
        """
        if not self.conectar():
            messagebox.showerror("ERRO DE CONEXAO")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE ocorrencias
                SET status = ?
                WHERE id=?
            """, (novo_status, ocorrencia_id))
            self.conn.commit()

            if cursor.rowcount>0:
                messagebox.showinfo(f"Status da ocorrencia ID:{ocorrencia_id} modificado para '{novo_status}'.")
                return True
            else:
                messagebox.showinfo(f"Nenhuma ocorrencia foi modificada.")
                return False
        except Error as e:
            messagebox.showerror(f"Erro ao modificar status= {e}")
            return False
        finally:
            self.desconectar()

    # =========== FUNÇÕES DE VISITAS ================

    def listar_visitas(self):
        """
        Obtem uma lista de todos os visitantes
        :return: Lista contendo todos os registros de visitas registrados
        """
        visitas = []
        if not self.conectar():
            return visitas

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT v.id, v.visitante_nome, v.visitante_cpf, m.nome, entrada
                FROM visitas v
                JOIN morador m ON v.morador_id = m.id
                ORDER BY v.entrada DESC
            """)
            visitas = cursor.fetchall()
        except Error as e:
            messagebox.showerror(f"Erro ao listar visitas: {e}")
        finally:
            self.desconectar()
            return visitas

    def listar_visitantes_por_morador(self, morador_id):
        """
        Lista todas as visitas de um morador especifico.
        :param morador_id: O ID do morador que sera feito o filtro.
        :return: Lista de visitas do morador.
        """
        visitantes = []
        if not self.conectar():
            return visitantes

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT visitante_nome, visitante_cpf
                FROM visitas
                WHERE morador_id = ?
            """, (morador_id,))
            visitantes = cursor.fetchall()
        except Error as e:
            messagebox.showerror(f"Erro ao listar visitantes do morador: {e}")
        finally:
            self.desconectar()
        return visitantes

    def registrar_visita_db(self, nome_visita, cpf_visita, morador_id, adm_id):
        """
        Registra uma visita no banco de dados.
        :param nome_visita: Nome do visitante.
        :param cpf_visita: CPF do visitante.
        :param morador_id: ID do morador visitado.
        :param adm_id: ID do administrador logado no banco de dados.
        :return: True se o registro for realizado, False caso contrario.
        """
        if not self.conectar():
            messagebox.showerror("ERRO DE CONEXAO")
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
            messagebox.showerror(f"Erro ao inserir ocorrência: {e}")
            return False
        finally:
            self.desconectar()

    # =========== FUNÇÕES DE ADMINISTRAÇÃO ================

    def buscar_administrador(self, login):
        admin_logado = []

        if not self.conectar():
            messagebox.showinfo("Falha no banco de dados")
            return admin_logado

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM administracao
                WHERE login = ?
            """, (login,))
            admin_logado = cursor.fetchone()
            messagebox.showinfo(admin_logado)
            return admin_logado
        except Error as e:
            messagebox.showerror(f"Erro ao buscar administrador: {e}")
            return admin_logado
        finally:
            self.desconectar()

    def listar_adm(self):
        """
        Busca uma lista com todos os adm do sistema
        """
        adm = []
        if not self.conectar():
            return adm

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, nome, telefone, tipo, ativo
                FROM administracao
            """)
            adm = cursor.fetchall()
        except Error as e:
            print(f"Erro ao listar administradores: {e}")
        finally:
            self.desconectar()
            return adm

    def modificar_status_administrador(self, admin_id):
        if not self.conectar():
            print("ERRO DE CONEXAO")
            return False

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE administracao
                SET ativo = CASE
                    WHEN ativo = 1 THEN 0
                    ELSE 1
                END
                WHERE id = ?
            """, (admin_id,))
            self.conn.commit()

            if cursor.rowcount > 0:
                print(f"Status do administrador ID:{admin_id} modificado.")
                return True
            else:
                print(f"Nenhum administrador com ID {admin_id} encontrado ou status já era o desejado.")
                return False
        except Error as e:
            print(f"Erro ao modificar status do administrador: {e}")
            return False

        finally:
            self.desconectar()

if __name__ == '__main__':
    db = Banco_de_dados()
    db.conectar()
    db.buscar_administrador(login='admin')