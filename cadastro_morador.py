
import tkinter as tk


def criar_janela_cadastro_morador(master=None):

    if master:
        janela = tk.Toplevel(master)
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Morador")
    janela.geometry("400x400")

    # Frame principal
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # Título
    tk.Label(frame_principal, text="Cadastrar Novo Morador", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # --- Campo Nome ---
    tk.Label(frame_principal, text="Nome Completo:", anchor="w").pack(fill=tk.X)
    entry_nome = tk.Entry(frame_principal, width=40)
    entry_nome.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Telefone ---
    tk.Label(frame_principal, text="Telefone:", anchor="w").pack(fill=tk.X)
    entry_telefone = tk.Entry(frame_principal, width=40)
    entry_telefone.pack(pady=(0, 10), fill=tk.X)

    # --- Campo CPF ---
    tk.Label(frame_principal, text="CPF:", anchor="w").pack(fill=tk.X)
    entry_cpf = tk.Entry(frame_principal, width=40)
    entry_cpf.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Bloco ---
    tk.Label(frame_principal, text="Bloco:", anchor="w").pack(fill=tk.X)
    entry_bloco = tk.Entry(frame_principal, width=40)
    entry_bloco.pack(pady=(0, 10), fill=tk.X)

    # --- Campo Apartamento ---
    tk.Label(frame_principal, text="Apartamento:", anchor="w").pack(fill=tk.X)
    entry_apartamento = tk.Entry(frame_principal, width=40)
    entry_apartamento.pack(pady=(0, 15), fill=tk.X)


    btn_cadastrar = tk.Button(frame_principal, text="Cadastrar Morador",

                              font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_cadastrar.pack()


    widgets = {
        "entry_nome": entry_nome,
        "entry_telefone": entry_telefone,
        "entry_cpf": entry_cpf,
        "entry_bloco": entry_bloco,
        "entry_apartamento": entry_apartamento,
        "btn_cadastrar": btn_cadastrar,
        "janela": janela
    }

    if not master:
        janela.mainloop()

    return widgets


if __name__ == '__main__':

    criar_janela_cadastro_morador()

