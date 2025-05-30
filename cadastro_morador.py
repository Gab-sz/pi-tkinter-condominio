import tkinter
import tkinter as tk
from autenticacao import Autenticacao

def criar_janela_cadastro_morador(master=None):
    if master:
        janela = tk.Toplevel(master)
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

    def limpar_campos():
        campo_nome.delete(0, tkinter.END)
        campo_telefone.delete(0, tkinter.END)
        campo_cpf.delete(0, tkinter.END)
        campo_bloco.delete(0, tkinter.END)
        campo_apartamento.delete(0, tkinter.END)

    def cadastrar_morador():
        nome = campo_nome.get()
        telefone = campo_telefone.get()
        cpf = campo_cpf.get()
        bloco = campo_bloco.get()
        apartamento = campo_apartamento.get()

        ## validar aqui

        autenticador = Autenticacao()
        sucesso = autenticador.registrar_morador(nome, telefone, cpf, bloco, apartamento)

        if sucesso:
            print("CADASTRO FEITO")
            limpar_campos()

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

if __name__ == '__main__':
    criar_janela_cadastro_morador()

