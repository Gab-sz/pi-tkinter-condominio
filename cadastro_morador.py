import tkinter as tk
from tkinter import messagebox
import re

from autenticacao import Autenticacao

def criar_janela_cadastro_morador(master=None):
    if master:
        janela = tk.Toplevel(master)
        janela.transient(master)
        janela.grab_set()
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Morador")
    janela.geometry("400x400")

    # Janela
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # Título
    tk.Label(frame_principal, text="Cadastrar Novo Morador", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # Nome
    tk.Label(frame_principal, text="Nome Completo:", anchor="w").pack(fill=tk.X)
    campo_nome = tk.Entry(frame_principal, width=40)
    campo_nome.pack(pady=(0, 10), fill=tk.X)
    campo_nome.focus()

    # Telefone
    tk.Label(frame_principal, text="Telefone:", anchor="w").pack(fill=tk.X)
    campo_telefone = tk.Entry(frame_principal, width=40)
    campo_telefone.pack(pady=(0, 10), fill=tk.X)

    # Cpf
    tk.Label(frame_principal, text="CPF:", anchor="w").pack(fill=tk.X)
    campo_cpf = tk.Entry(frame_principal, width=40)
    campo_cpf.pack(pady=(0, 10), fill=tk.X)

    # Bloco
    tk.Label(frame_principal, text="Bloco:", anchor="w").pack(fill=tk.X)
    campo_bloco = tk.Entry(frame_principal, width=40)
    campo_bloco.pack(pady=(0, 10), fill=tk.X)

    # Apartamento
    tk.Label(frame_principal, text="Apartamento:", anchor="w").pack(fill=tk.X)
    campo_apartamento = tk.Entry(frame_principal, width=40)
    campo_apartamento.pack(pady=(0, 15), fill=tk.X)

    def cadastrar_morador():
        nome = campo_nome.get()
        telefone = campo_telefone.get()
        cpf = campo_cpf.get()
        bloco = campo_bloco.get()
        apartamento = campo_apartamento.get()

        if not nome:
            messagebox.showwarning("Campo Obrigatório", "Campo Nome não pode estar vazio.", parent=janela)
            return
        if not telefone:
            messagebox.showwarning("Campo Obrigatório", "Campo Telefone não pode estar vazio.", parent=janela)
            return
        if not validar_telefone(telefone):
            messagebox.showwarning("Formato Inválido", "O Telefone deve estar no formato '(xx) xxxxx-xxxx'", parent=janela)
            return
        if not cpf:
            messagebox.showwarning("Campo Obrigatório", "Campo CPF não pode estar vazio.", parent=janela)
            return
        if not validar_cpf(cpf):
            messagebox.showwarning("Formato Inválido", "O CPF deve deve estar no formato 'xxx.xxx.xxx-xx'", parent=janela)
            return
        if not bloco:
            messagebox.showwarning("Campo Obrigatório", "Campo Bloco não pode estar vazio.", parent=janela)
            return
        if not apartamento:
            messagebox.showwarning("Campo Obrigatório", "Campo Apartamento não pode estar vazio.", parent=janela)
            return

        autenticador = Autenticacao()
        sucesso = autenticador.registrar_morador_db(nome, telefone, cpf, bloco, apartamento)

        if sucesso:
            messagebox.showinfo("Sucesso", "Morador cadastrado com sucesso!", parent=janela)
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar morador.", parent=janela)

    btn_cadastrar = tk.Button(frame_principal, text="Cadastrar Morador", command=cadastrar_morador, font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_cadastrar.pack()

    widgets = {
        "entry_nome": campo_nome,
        "entry_telefone": campo_telefone,
        "entry_cpf": campo_cpf,
        "entry_bloco": campo_bloco,
        "entry_apartamento": campo_apartamento,
        "btn_cadastrar": btn_cadastrar,
        "janela": janela
    }

    if not master:
        janela.mainloop()

    return widgets

def validar_cpf(cpf):
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    if re.match(padrao, cpf):
        return True
    return False

def validar_telefone(telefone):
    padrao = r"^\(\d{2}\) \d{4,5}-\d{4}$"
    if re.match(padrao, telefone):
        return True
    return False

if __name__ == '__main__':
    criar_janela_cadastro_morador()

