# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

def criar_janela_cadastro_administrador(master=None):

    if master:
        janela = tk.Toplevel(master)
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Administrador")
    janela.geometry("400x400") #

    # Frame principal
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # Título
    tk.Label(frame_principal, text="Cadastrar Novo Administrador", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # --- Campo Nome ---
    tk.Label(frame_principal, text="Nome Completo:", anchor="w").pack(fill=tk.X)
    entry_nome = tk.Entry(frame_principal, width=40)
    entry_nome.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Telefone ---
    tk.Label(frame_principal, text="Telefone:", anchor="w").pack(fill=tk.X)
    entry_telefone = tk.Entry(frame_principal, width=40)
    entry_telefone.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Login ---
    tk.Label(frame_principal, text="Login de Acesso:", anchor="w").pack(fill=tk.X)
    entry_login = tk.Entry(frame_principal, width=40)
    entry_login.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Senha ---
    tk.Label(frame_principal, text="Senha:", anchor="w").pack(fill=tk.X)
    entry_senha = tk.Entry(frame_principal, width=40, show="*")
    entry_senha.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Tipo (Usando Radiobuttons) ---
    tk.Label(frame_principal, text="Tipo de Usuário:", anchor="w").pack(fill=tk.X)
    var_tipo = tk.StringVar(value="") # Variável para armazenar a escolha

    frame_radio = tk.Frame(frame_principal)

    frame_radio.pack(pady=(0, 15), anchor='w')

    radio_sindico = ttk.Radiobutton(frame_radio, text="Síndico", variable=var_tipo, value="sindico")
    radio_sindico.pack(side=tk.LEFT, padx=5)

    radio_porteiro = ttk.Radiobutton(frame_radio, text="Porteiro", variable=var_tipo, value="porteiro")
    radio_porteiro.pack(side=tk.LEFT, padx=5)

    # Botão Cadastrar
    btn_cadastrar = tk.Button(frame_principal, text="Cadastrar Administrador",
                              # command= foi removido
                              font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_cadastrar.pack()


    widgets = {
        "entry_nome": entry_nome,
        "entry_telefone": entry_telefone,
        "entry_login": entry_login,
        "entry_senha": entry_senha,
        "var_tipo": var_tipo,
        "radio_sindico": radio_sindico,
        "radio_porteiro": radio_porteiro,
        "btn_cadastrar": btn_cadastrar,
        "janela": janela
    }

    if not master:
        janela.mainloop()

    return widgets

if __name__ == '__main__':

    criar_janela_cadastro_administrador()

