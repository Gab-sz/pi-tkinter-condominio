
import tkinter as tk
from tkinter import ttk


def criar_janela_cadastro_ocorrencia(master=None):

    if master:
        janela = tk.Toplevel(master)
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Ocorrência")
    janela.geometry("450x450")


    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)


    tk.Label(frame_principal, text="Registrar Nova Ocorrência", font=("Arial", 16, "bold")).pack(pady=(0, 15))


    tk.Label(frame_principal, text="Motivo:", anchor="w").pack(fill=tk.X)
    entry_motivo = tk.Entry(frame_principal, width=50)
    entry_motivo.pack(pady=(0, 10), fill=tk.X)


    tk.Label(frame_principal, text="Descrição Detalhada:", anchor="w").pack(fill=tk.X)
    text_descricao = tk.Text(frame_principal, height=8, width=50)
    text_descricao.pack(pady=(0, 10), fill=tk.BOTH, expand=True)


    tk.Label(frame_principal, text="Morador Relacionado:", anchor="w").pack(fill=tk.X)

    opcoes_moradores = ["(Carregar moradores...)"]
    combo_morador = ttk.Combobox(frame_principal, values=opcoes_moradores, state="readonly")
    combo_morador.pack(pady=(0, 10), fill=tk.X)
    combo_morador.set(opcoes_moradores[0])


    tk.Label(frame_principal, text="Status Inicial:", anchor="w").pack(fill=tk.X)
    opcoes_status = ["aberto", "fechado"]
    combo_status = ttk.Combobox(frame_principal, values=opcoes_status, state="readonly")
    combo_status.pack(pady=(0, 15), fill=tk.X)
    combo_status.set("aberto")

    btn_registrar = tk.Button(frame_principal, text="Registrar Ocorrência",

                              font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_registrar.pack()

    widgets = {
        "entry_motivo": entry_motivo,
        "text_descricao": text_descricao,
        "combo_morador": combo_morador,
        "combo_status": combo_status,
        "btn_registrar": btn_registrar,
        "janela": janela
    }


    if not master:
        janela.mainloop()

    return widgets


if __name__ == '__main__':

    criar_janela_cadastro_ocorrencia()

