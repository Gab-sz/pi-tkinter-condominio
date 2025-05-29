import tkinter as tk
from autenticacao import Autenticacao

# Variáveis globais para usar nos metodos
lbl_login = None
txt_senha = None
janela = None

def autenticar_usuario():
    login = lbl_login.get()
    senha = txt_senha.get()

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
    global lbl_login, txt_senha

    janela = tk.Tk()
    janela.title("Sistema condominio - Tela inicial")
    janela.geometry("350x200")

    # Título
    tk.Label(janela, text="Bem vindo(a)!", font=("Arial",14)).pack(pady=10)

    # Campo Administrador
    tk.Label(janela, text="Login:").pack()
    lbl_login = tk.Entry(janela)
    lbl_login.pack()

    # Campo Senha
    tk.Label(janela, text="Senha:").pack()
    txt_senha = tk.Entry(janela, show="*")
    txt_senha.pack()

    # Botão
    tk.Button(janela, text="Entrar", command=autenticar_usuario).pack(pady=10)

    # Loop da janela
    janela.mainloop()

# Chamar a função para iniciar a janela
if __name__ == '__main__':
    criar_janela_login()
