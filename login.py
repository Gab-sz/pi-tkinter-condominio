import tkinter as tk
from tkinter import messagebox

# Função de login
def fazer_login():
    administrador = entrada_adm.get()
    senha = entrada_senha.get()

    if administrador == "ADM.COND.123" and senha == "12345678":
        messagebox.showinfo("LOGIN", "LOGIN BEM-SUCEDIDO!")
    else:
        messagebox.showerror("ERRO", "ADMINISTRADOR OU SENHA INCORRETOS")

# Criando a janela
interface = tk.Tk()
interface.title("TELA DE LOGIN")
interface.geometry("500x300")

# Título
tk.Label(interface, text="LOGIN DO SISTEMA", font=("Arial",14)).pack(pady=10)

# Campo Administrador
tk.Label(interface, text="ADMINISTRADOR:").pack()
entrada_adm = tk.Entry(interface)
entrada_adm.pack()

# Campo Senha
tk.Label(interface, text="Senha:").pack()
entrada_senha = tk.Entry(interface, show="*")
entrada_senha.pack()

# Botão
tk.Button(interface, text="Entrar", command=fazer_login).pack(pady=10)

# Loop da janela
interface.mainloop()

