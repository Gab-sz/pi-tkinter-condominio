import bcrypt
from banco_de_dados import Banco_de_dados

class Autenticacao:
    def __init__(self):
        """
        Inicial a classe de autenticação com um banco de dados.
        """
        self.db = Banco_de_dados()

    def gerar_hash(self, senha):
        if isinstance(senha, str):
            senha_bytes = senha.encode('utf-8')
        else:
            senha_bytes = senha

        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(senha_bytes, salt)

        return hash_senha.decode('utf-8')

    def verificar_senha(self, senha, hash):
        if isinstance(senha, str):
            senha_bytes = senha.encode('utf-8')
        else:
            senha_bytes = senha

        if isinstance(hash, str):
            hash_bytes = hash.encode('utf-8')
        else:
            hash_bytes = hash

        try:
            return bcrypt.checkpw(senha_bytes, hash_bytes)
        except Exception as e:
            print(f"Erro ao verificar senha: {e}")
            return False

    def autenticar_usuario(self, login, senha):
        if self.db.conectar():
            try:
                cursor = self.db.conn.cursor()
                cursor.execute("""
                    SELECT id, nome, login, senha, tipo, ativo
                    FROM administracao
                    WHERE login = ? AND ativo = 1
                """, (login,))

                usuario = cursor.fetchone()
                if usuario is None:
                    return False, None

                id_usuario, nome, login_db, senha_cript, tipo, ativo = usuario

                if self.verificar_senha(senha, senha_cript):
                    inf_usuario = {
                        'id': id_usuario,
                        'nome': nome,
                        'login': login_db,
                        'tipo': tipo
                    }
                    return True, inf_usuario
                else:
                    return False, None

            except Exception as e:
                print(f"Erro na autenticação: {e}")
                return False, None
            finally:
                if self.db.conn:
                    self.db.conn.close()

    def registrar_administrador_db(self, nome, telefone, login, senha, tipo):
        if self.db.conectar():
            try:
                hash_senha = self.gerar_hash(senha)
                cursor = self.db.conn.cursor()
                cursor.execute("""
                    INSERT INTO administracao (nome, telefone, login, senha, tipo)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, telefone, login, hash_senha, tipo))
                self.db.conn.commit()
                print("Administrador criado com sucesso!")
                return True

            except Exception as e:
                print(f"Erro ao cadastrar adm: {e}")
                return False
            finally:
                if self.db.conn:
                    self.db.conn.close()

    def registrar_morador_db(self, nome, telefone, cpf, bloco, apartamento):
        if self.db.conectar():
            try:
                cursor = self.db.conn.cursor()
                cursor.execute("""
                    INSERT INTO morador (nome, telefone, cpf, bloco, apartamento)
                    VALUES (?, ?, ?, ?, ?)
                """, (nome, telefone, cpf, bloco, apartamento))
                self.db.conn.commit()
                print("Morador criado com sucesso!")
                return True

            except Exception as e:
                print(f"Erro ao cadastrar morador: {e}")
                return False
            finally:
                if self.db.conn:
                    self.db.conn.close()
