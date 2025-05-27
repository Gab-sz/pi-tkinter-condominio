import tkinter as tk
from tkinter import messagebox

# Função de login
def autenticar_login():
    administrador = entrada_adm.get()
    senha = entrada_senha.get()

    if administrador == "admin" and senha == "admin":
        messagebox.showinfo("Login efetuado!", "LOGIN BEM-SUCEDIDO!")
    else:
        messagebox.showerror("Login nao efetuado!", "ADMINISTRADOR OU SENHA INCORRETOS")

# Criando a janela
def criar_janela_login():
    global entrada_adm, entrada_senha

    janela = tk.Tk()
    janela.title("TELA DE LOGIN")
    janela.geometry("500x300")

    # Título
    tk.Label(janela, text="LOGIN DO SISTEMA", font=("Arial",14)).pack(pady=10)

    # Campo Administrador
    tk.Label(janela, text="ADMINISTRADOR:").pack()
    entrada_adm = tk.Entry(janela)
    entrada_adm.pack()

    # Campo Senha
    tk.Label(janela, text="Senha:").pack()
    entrada_senha = tk.Entry(janela, show="*")
    entrada_senha.pack()

    # Botão
    tk.Button(janela, text="Entrar", command=fazer_login).pack(pady=10)

    # Loop da janela
    janela.mainloop()

# Chamar a função para iniciar a janela
criar_janela()
