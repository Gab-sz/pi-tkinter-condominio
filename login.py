import tkinter as tk
from autenticacao import Autenticacao

# Variáveis globais para usar nos metodos
campo_login = None
campo_senha = None
janela = None

def autenticar_usuario():
    login = campo_login.get()
    senha = campo_senha.get()

    if not login or not senha:
        print("Campos vazios!")
        return False

    autenticador = Autenticacao()
    sucesso, inf_usuario = autenticador.autenticar_usuario(login, senha)

    if sucesso:
        print(f"Bem vindo, {inf_usuario['nome']}!!!")
    else:
        print("Login ou senha incorretos!")

def criar_janela_login():
    global campo_login, campo_senha

    janela = tk.Tk()
    janela.title("Sistema condominio - Tela inicial")
    janela.geometry("350x200")

    # Título
    tk.Label(janela, text="Bem vindo(a)!", font=("Arial",14)).pack(pady=10)

    # Campo Administrador
    tk.Label(janela, text="Login:").pack()
    campo_login = tk.Entry(janela)
    campo_login.pack()

    # Campo Senha
    tk.Label(janela, text="Senha:").pack()
    campo_senha = tk.Entry(janela, show="*")
    campo_senha.pack()

    # Botão
    tk.Button(janela, text="Entrar", command=autenticar_usuario).pack(pady=10)

    # Loop da janela
    janela.mainloop()

# Chamar a função para iniciar a janela
if __name__ == '__main__':
    criar_janela_login()
