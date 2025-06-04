import tkinter as tk
from tkinter import ttk, messagebox
from banco_de_dados import Banco_de_dados

# Dados para testar
usuario_teste = {
    'id': 1,
    'nome': 'Administrador teste',
    'tipo': 'sindico'
}

def criar_janela_cadastro_ocorrencia(master=None, usuario_logado=None):
    """
    Cria a janela de registro de ocorrencia, com as funções de popular o combobox e de registrar juntos.
    :param master: janela "pai"
    :param usuario_logado: Usuario que entrou no sistema. Recebe esses dados da janela anterior.
    """
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

    janela.title("Cadastro de Ocorrência")
    janela.geometry("450x450")

    # Janela
    frame_principal = tk.Frame(janela, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    # Titulo
    tk.Label(frame_principal, text="Registrar Nova Ocorrência", font=("Arial", 16, "bold")).pack(pady=(0, 15))

    # Motivo
    tk.Label(frame_principal, text="Motivo:", anchor="w").pack(fill=tk.X)
    campo_motivo = tk.Entry(frame_principal, width=50)
    campo_motivo.pack(pady=(0, 10), fill=tk.X)
    campo_motivo.focus()

    # Descrição
    tk.Label(frame_principal, text="Descrição Detalhada:", anchor="w").pack(fill=tk.X)
    campo_descricao = tk.Text(frame_principal, height=8, width=50)
    campo_descricao.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

    #Morador
    tk.Label(frame_principal, text="Morador Solicitante:", anchor="w").pack(fill=tk.X)
    combo_morador = ttk.Combobox(frame_principal, state="readonly")
    combo_morador.pack(pady=(0, 10), fill=tk.X)

    # Lista dos moradores
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

    def cadastrar_ocorrencia():
        """
        Cadastra uma ocorrencia para ser salva no banco de dados.
        """
        # Puxando as informações dos campos
        motivo = campo_motivo.get().strip()
        descricao = campo_descricao.get("1.0", tk.END).strip()
        morador_selecionado = combo_morador.get()
        morador_id = moradores.get(morador_selecionado)
        admin_id = usuario_logado['id']

        if morador_id is None:
            messagebox.showwarning("Nenhum morador selecionado")

        ##validação AQUIII

        # Conecta no banco e salva
        db = Banco_de_dados()
        sucesso = db.registrar_ocorrencia_db(motivo, descricao, morador_id, admin_id)

        if sucesso:
            messagebox.showinfo("Sucesso", "Cadastro de ocorrencia efetuado.", parent=janela)
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao registrar ocorrencia.", parent=janela)

    # Botao
    btn_registrar = tk.Button(frame_principal, command=cadastrar_ocorrencia, text="Registrar Ocorrência",
                              font=("Arial", 12), bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
    btn_registrar.pack()

    popular_moradores()
    widgets = {
        "campo_motivo": campo_motivo,
        "campo_descricao": campo_descricao,
        "combo_morador": combo_morador,
        "btn_registrar": btn_registrar,
        "janela": janela,
        "usuario_logado": usuario_logado,
        "moradores": moradores
    }

    if not master:
        janela.mainloop()

    return widgets

if __name__ == '__main__':
    criar_janela_cadastro_ocorrencia()

