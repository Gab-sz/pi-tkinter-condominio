
import tkinter as tk
from tkinter import ttk


def criar_janela_cadastro_visita(master=None):

    if master:
        janela = tk.Toplevel(master)
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Visita")
    janela.geometry("450x350")

    # Frame principal
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # Título
    tk.Label(frame_principal, text="Registrar Nova Visita", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # --- Campos do Visitante ---
    tk.Label(frame_principal, text="Nome do Visitante:", anchor="w").pack(fill=tk.X)
    entry_nome_visitante = tk.Entry(frame_principal, width=50)
    entry_nome_visitante.pack(pady=(0, 10), fill=tk.X)

    tk.Label(frame_principal, text="CPF do Visitante:", anchor="w").pack(fill=tk.X)
    entry_cpf_visitante = tk.Entry(frame_principal, width=50)
    entry_cpf_visitante.pack(pady=(0, 10), fill=tk.X)


    tk.Label(frame_principal, text="Morador Visitado:", anchor="w").pack(fill=tk.X)

    lista_moradores_exemplo = ["(Carregar moradores...)"]
    combo_morador = ttk.Combobox(frame_principal, values=lista_moradores_exemplo, state="readonly", width=48)
    combo_morador.pack(pady=(0, 15), fill=tk.X)
    combo_morador.set(lista_moradores_exemplo[0])


    btn_registrar = tk.Button(frame_principal, text="Registrar Visita",

                              font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_registrar.pack()


    widgets = {
        "entry_nome_visitante": entry_nome_visitante,
        "entry_cpf_visitante": entry_cpf_visitante,
        "combo_morador": combo_morador,
        "btn_registrar": btn_registrar,
        "janela": janela
    }

    if not master:
        janela.mainloop()

    return widgets


if __name__ == '__main__':

    criar_janela_cadastro_visita()

