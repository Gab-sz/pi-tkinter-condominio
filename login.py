import tkinter as tk
from tkinter import messagebox
from webbrowser import Error

from autenticacao import Autenticacao
from banco_de_dados import Banco_de_dados
from janela_menu import InterfaceListagens

# Variáveis globais para usar nos metodos
campo_login = None
campo_senha = None
janela_login = None

def autenticar_usuario():
    global janela_login
    login = campo_login.get()
    senha = campo_senha.get()

    if not login or not senha:
        tk.messagebox.showwarning("Atenção", "Preencha todos os campos.", parent=janela_login)
        return False

    autenticador = Autenticacao()
    sucesso, inf_usuario = autenticador.autenticar_usuario(login, senha)

    if sucesso:
        janela_login.destroy()
        root_menu = tk.Tk()
        menu = InterfaceListagens(root_menu, inf_usuario)
        root_menu.mainloop()
    else:
        tk.messagebox.showerror("Erro de Login", "Login ou senha incorretos!", parent=janela_login)

def criar_janela_login():
    global campo_login, campo_senha, janela_login

    try:
        db = Banco_de_dados()
        db.conectar(criar_tabelas=True)
    except Error as e:
        print(f"Erro: {e}")
    finally:
        db.desconectar()

    janela_login = tk.Tk()
    janela_login.title("Sistema condominio - Tela inicial")
    janela_login.geometry("350x200")

    # Título
    tk.Label(janela_login, text="Bem vindo(a)!", font=("Arial",14)).pack(pady=10)

    # Campo Administrador
    tk.Label(janela_login, text="Login:").pack()
    campo_login = tk.Entry(janela_login)
    campo_login.pack()
    campo_login.focus()

    # Campo Senha
    tk.Label(janela_login, text="Senha:").pack()
    campo_senha = tk.Entry(janela_login, show="*")
    campo_senha.pack()

    # Botão
    tk.Button(janela_login, text="Entrar", command=autenticar_usuario).pack(pady=10)

    # Loop da janela
    janela_login.mainloop()

# Chamar a função para iniciar a janela
if __name__ == '__main__':
    criar_janela_login()
