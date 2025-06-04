import tkinter as tk
<<<<<<< HEAD
=======
from tkinter import ttk
>>>>>>> d6d471f59afc4bcc6995ec0c78e48c526a2feae4
from tkinter import ttk, messagebox
from banco_de_dados import Banco_de_dados

# Dados para testar
usuario_teste = {
    'id': 5,
    'nome': 'Administrador teste',
    'tipo': 'sindico'
}

def criar_janela_cadastro_visita(master=None, usuario_logado=None):
    if usuario_logado is None:
        messagebox.showwarning("DADOS DO ADM NAO FORNECIDOS")
        usuario_logado = usuario_teste
        messagebox.showwarning("Usando usuario teste")

    if master:
        janela = tk.Toplevel(master)
        janela.transient(master)
        janela.grab_set()
    else:
        janela = tk.Tk()

    janela.title("Cadastro de Visita")
    janela.geometry("450x350")

    # Janela
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # Título
    tk.Label(frame_principal, text="Registrar Nova Visita", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # Nome visitante
    tk.Label(frame_principal, text="Nome do Visitante:", anchor="w").pack(fill=tk.X)
    campo_nome_visita = tk.Entry(frame_principal, width=50)
    campo_nome_visita.pack(pady=(0, 10), fill=tk.X)
    campo_nome_visita.focus()

    # cpf visitante
    tk.Label(frame_principal, text="CPF do Visitante:", anchor="w").pack(fill=tk.X)
    campo_cpf_visita = tk.Entry(frame_principal, width=50)
    campo_cpf_visita.pack(pady=(0, 10), fill=tk.X)

    # Morador que recebe a visita
    tk.Label(frame_principal, text="Morador Visitado:", anchor="w").pack(fill=tk.X)
    combo_morador = ttk.Combobox(frame_principal, state="readonly", width=48)
    combo_morador.pack(pady=(0, 15), fill=tk.X)

    #Lista de moradores
    moradores = {}

    def popular_moradores():
        """
        Função para puxar os moradores do banco de dados e inseri-los no combobox.
        A função cria um texto formatado para colocar no combobox com <nome> <bloco> <apartamento>
        """
        db = Banco_de_dados()
        moradores_ativos = db.listar_moradores_ativos()
        moradores.clear()
        formato = []

        if moradores_ativos:
            for morador_id, nome, bloco, apt, ativo in moradores_ativos:
                texto = f"{nome} - Bloco {bloco} Apto {apt}"
                formato.append(texto)
                moradores[texto] = morador_id
            combo_morador['values'] = formato
            if formato:
                combo_morador.set(formato[0])
                combo_morador['state'] = 'readonly'
            else:
                combo_morador['values'] = formato
                combo_morador.set(formato[0])
                combo_morador['state'] = 'disabled'
        else:
            formato = ["Nenhum morador ativo encontrado"]
            combo_morador['values'] = formato
            combo_morador.set(formato[0])
            combo_morador['state'] = 'disabled'

    def cadastrar_visita():
        nome_visita = campo_nome_visita.get().strip()
        cpf_visita = campo_cpf_visita.get().strip()
        morador_selecionado = combo_morador.get()
        morador_id = moradores.get(morador_selecionado)
        admin_id = usuario_logado['id']

        if morador_id is None:
            messagebox.showwarning("Nenhum morador selecionado")

        ##Validação aqui

        db = Banco_de_dados()
        sucesso = db.registrar_visita_db(nome_visita, cpf_visita, morador_id, admin_id)

        if sucesso:
<<<<<<< HEAD
            messagebox.showinfo("Sucesso", "Cadastro de visita efetuado.", parent=janela)
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao registrar a visita.", parent=janela)
=======
            messagebox.showwarning("VISITA REGISTRADA")
            ##DESTRUIR A JANELA
>>>>>>> d6d471f59afc4bcc6995ec0c78e48c526a2feae4

    # Botao para registrar
    btn_registrar = tk.Button(frame_principal, text="Registrar Visita", command=cadastrar_visita,
                              font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_registrar.pack()

    janela.bind('<Return>', lambda event=None: btn_registrar.invoke())

    popular_moradores()
    widgets = {
        "campo_nome_visita": campo_nome_visita,
        "campo_cpf_visita": campo_cpf_visita,
        "combo_morador": combo_morador,
        "btn_registrar": btn_registrar,
        "janela": janela
    }

    if not master:
        janela.mainloop()

    return widgets

if __name__ == '__main__':
    criar_janela_cadastro_visita()

