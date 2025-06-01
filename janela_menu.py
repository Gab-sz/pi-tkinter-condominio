import tkinter as tk
from tkinter import ttk
from banco_de_dados import Banco_de_dados


class InterfaceListagens:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Condomínio - Listagens")
        self.root.geometry("500x300")

        self.db = Banco_de_dados()

        # Botões principais
        btn_moradores = tk.Button(root, text="Listar Moradores", command=self.abrir_janela_moradores)
        btn_moradores.pack(pady=10)

        btn_visitantes = tk.Button(root, text="Listar Visitantes", command=self.abrir_janela_visitantes)
        btn_visitantes.pack(pady=10)

        btn_ocorrencias = tk.Button(root, text="Listar Ocorrências", command=self.abrir_janela_ocorrencias)
        btn_ocorrencias.pack(pady=10)

    def abrir_janela_moradores(self):
        janela = tk.Toplevel(self.root)
        janela.title("Moradores Cadastrados")

        tree = ttk.Treeview(janela, columns=("ID", "Nome", "Bloco", "Apartamento"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Bloco", text="Bloco")
        tree.heading("Apartamento", text="Apartamento")
        tree.column("ID", width=50, anchor='center')
        tree.pack(fill="both", expand=True)

        btn_detalhes = tk.Button(janela, text="Ver Detalhes",
                                 command=lambda: self.mostrar_detalhes_morador(tree.item(tree.selection())['values']))
        btn_detalhes.pack()

        moradores = self.db.listar_moradores_ativos()
        for morador in moradores:
            tree.insert("", "end", values=morador)

    def abrir_janela_visitantes(self):
        janela = tk.Toplevel(self.root)
        janela.title("Histórico de Visitas")
        janela.geometry("800x400")

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=("Visita"), show="headings")
        tree.heading("Visita", text="Registro de Visitas")
        tree.column("Visita", width=750)
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        visitas = self.db.listar_visitas_com_detalhes()
        for visita in visitas:
            visitante_nome, visitante_cpf, morador_nome, data_visita = visita
            data_formatada = data_visita.split()[0]
            registro = f"{visitante_nome} (CPF: {visitante_cpf}) visitou {morador_nome} em {data_formatada}"
            tree.insert("", "end", values=(registro,))

    def abrir_janela_ocorrencias(self):
        janela = tk.Toplevel(self.root)
        janela.title("Ocorrências Registradas")
        janela.geometry("800x400")

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=("Motivo", "Descrição", "Morador", "Status"), show="headings")
        tree.heading("Motivo", text="Motivo")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Morador", text="Morador")
        tree.heading("Status", text="Status")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        ocorrencias = self.db.listar_ocorrencias()
        for oc in ocorrencias:
            tree.insert("", "end", values=(oc[1], oc[2], oc[3], oc[4]))

    def mostrar_detalhes_morador(self, morador_data):
        if not morador_data:
            return

        morador_id, nome, bloco, apartamento = morador_data
        janela = tk.Toplevel(self.root)
        janela.title(f"Detalhes do Morador: {nome}")
        janela.geometry("600x400")

        # Frame principal
        main_frame = tk.Frame(janela)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Informações básicas
        info_frame = tk.LabelFrame(main_frame, text="Informações do Morador")
        info_frame.pack(fill="x", pady=5)

        tk.Label(info_frame, text=f"Nome: {nome}").pack(anchor="w")
        tk.Label(info_frame, text=f"Bloco: {bloco}").pack(anchor="w")
        tk.Label(info_frame, text=f"Apartamento: {apartamento}").pack(anchor="w")

        # Abas para ocorrências e visitantes
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        # Aba de Ocorrências
        ocorrencias_frame = ttk.Frame(notebook)
        notebook.add(ocorrencias_frame, text="Ocorrências")

        tree_ocorrencias = ttk.Treeview(ocorrencias_frame, columns=("Motivo", "Status"), show="headings")
        tree_ocorrencias.heading("Motivo", text="Motivo")
        tree_ocorrencias.heading("Status", text="Status")
        tree_ocorrencias.pack(fill="both", expand=True)

        # Aba de Visitantes
        visitantes_frame = ttk.Frame(notebook)
        notebook.add(visitantes_frame, text="Visitantes")

        tree_visitantes = ttk.Treeview(visitantes_frame, columns=("Visitante", "CPF"), show="headings")
        tree_visitantes.heading("Visitante", text="Visitante")
        tree_visitantes.heading("CPF", text="CPF")
        tree_visitantes.pack(fill="both", expand=True)

        # Preencher os dados
        self.carregar_ocorrencias_morador(morador_id, tree_ocorrencias)
        self.carregar_visitantes_morador(morador_id, tree_visitantes)

    def carregar_ocorrencias_morador(self, morador_id, tree):
        # Implemente esta função para carregar as ocorrências do morador
        pass

    def carregar_visitantes_morador(self, morador_id, tree):
        # Implemente esta função para carregar os visitantes do morador
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceListagens(root)
    root.mainloop()