import tkinter
import tkinter as tk
from tkinter import ttk, messagebox
from autenticacao import Autenticacao
import re

def validar_telefone(telefone):
    padrao = r"^\(\d{2}\) \d{4,5}-\d{4}$"
    if re.match(padrao, telefone):
        return True
    return False

def validar_senha(senha):
    if len(senha)>=6:
        return True
    return False

def criar_janela_cadastro_administrador(master=None):
    if master:
        janela = tk.Toplevel(master)
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Administrador")
    janela.geometry("400x400") #

    # Tela de cadastro
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # titulo
    tk.Label(frame_principal, text="Cadastrar Novo Administrador", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # nome
    tk.Label(frame_principal, text="Nome Completo:", anchor="w").pack(fill=tk.X)
    campo_nome = tk.Entry(frame_principal, width=40)
    campo_nome.pack(pady=(0, 10), fill=tk.X)

    # telefome
    tk.Label(frame_principal, text="Telefone:", anchor="w").pack(fill=tk.X)
    campo_telefone = tk.Entry(frame_principal, width=40)
    campo_telefone.pack(pady=(0, 10), fill=tk.X)

    # login
    tk.Label(frame_principal, text="Login de Acesso:", anchor="w").pack(fill=tk.X)
    campo_login = tk.Entry(frame_principal, width=40)
    campo_login.pack(pady=(0, 10), fill=tk.X)

    # senha
    tk.Label(frame_principal, text="Senha:", anchor="w").pack(fill=tk.X)
    campo_senha = tk.Entry(frame_principal, width=40, show="*")
    campo_senha.pack(pady=(0, 10), fill=tk.X)

    # tipo
    tk.Label(frame_principal, text="Tipo de Usuário:", anchor="w").pack(fill=tk.X)
    var_tipo = tk.StringVar(value="")

    frame_radio = tk.Frame(frame_principal)
    frame_radio.pack(pady=(0, 15), anchor='w')

    # opção1: sindico
    radio_sindico = ttk.Radiobutton(frame_radio, text="Síndico", variable=var_tipo, value="sindico")
    radio_sindico.pack(side=tk.LEFT, padx=5)

    # opção2: porteiro
    radio_porteiro = ttk.Radiobutton(frame_radio, text="Porteiro", variable=var_tipo, value="porteiro")
    radio_porteiro.pack(side=tk.LEFT, padx=5)

    def limpar_campos():
        campo_nome.delete(0, tkinter.END)
        campo_telefone.delete(0, tkinter.END)
        campo_login.delete(0, tkinter.END)
        campo_senha.delete(0, tkinter.END)
        var_tipo.set("")

    def cadastrar_administrador():
        nome = campo_nome.get()
        telefone = campo_telefone.get()
        login = campo_login.get()
        senha = campo_senha.get()
        tipo = var_tipo.get()

        if not nome:
            messagebox.showwarning("Campo Obrigatório", "O campo Nome Completo não pode estar vazio.", parent=janela)
            return
        if not telefone:
            messagebox.showwarning("Campo Obrigatório", "O campo Telefone não pode estar vazio.", parent=janela)
            return
        if not validar_telefone(telefone):
            messagebox.showwarning("Formato Inválido", "O campo Telefone deve ser no formato '(xx) xxxxx-xxxx'.", parent=janela)
            return
        if not login:
            messagebox.showwarning("Campo Obrigatório", "O campo Login não pode estar vazio.", parent=janela)
            return
        if not senha:
            messagebox.showwarning("Campo Obrigatório", "O campo Senha não pode estar vazio.", parent=janela)
            return
        if not validar_senha(senha):
            messagebox.showwarning("Formato Inválido", "O campo senha deve ter pelo menos 6 caracteres.", parent=janela)
            return
        if not tipo:
            messagebox.showwarning("Seleção Obrigatória", "Selecione o Tipo de Usuário (Síndico ou Porteiro).", parent=janela)
            return

        autenticador = Autenticacao()
        sucesso = autenticador.registrar_administrador_db(nome, telefone, login, senha, tipo)

        if sucesso:
            messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso!", parent=janela)
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar Administrador.", parent=janela)

    # Botão Cadastrar
    btn_cadastrar = tk.Button(frame_principal, command=cadastrar_administrador, text="Cadastrar Administrador", font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_cadastrar.pack()

    widgets = {
        "entry_nome": campo_nome,
        "entry_telefone": campo_telefone,
        "entry_login": campo_login,
        "entry_senha": campo_senha,
        "var_tipo": var_tipo,
        "radio_sindico": radio_sindico,
        "radio_porteiro": radio_porteiro,
        "btn_cadastrar": btn_cadastrar,
        "janela": janela
    }

    if not master:
        janela.mainloop()
    return widgets

def validar(telefone, senha):
    telefone

if __name__ == '__main__':
    criar_janela_cadastro_administrador()

