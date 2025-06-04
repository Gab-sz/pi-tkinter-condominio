import tkinter as tk
from tkinter import ttk, messagebox, Label
from banco_de_dados import Banco_de_dados

class InterfaceListagens:
    def __init__(self, root, admin_info):
        """
        Inicia a janela de menu.
        :param root: Janela que sera mostrada.
        :param admin_info: Usuario logado no sistema.
        """
        self.root = root
        self.admin_info = admin_info
        self.root.title("Sistema Condomínio - Listagens")
        self.root.geometry("500x250")

        self.db = Banco_de_dados()

        tk.Label(root, text=f"Bem vindo(a) {self.admin_info.get('nome')}! ({self.admin_info.get('tipo').capitalize()})", font=("Arial",14)).pack(pady=10)

        btn_moradores = tk.Button(root, text="Lista de Moradores", command=self.abrir_janela_moradores)
        btn_moradores.pack(pady=10)

        btn_visitas = tk.Button(root, text="Lista de Visitas", command=self.abrir_janela_visitas)
        btn_visitas.pack(pady=10)

        btn_ocorrencias = tk.Button(root, text="Lista de Ocorrências", command=self.abrir_janela_ocorrencias)
        btn_ocorrencias.pack(pady=10)

    #============ TELA DE MORADORES ==============

    def abrir_janela_moradores(self):
        """
        Cria uma janela com a listagem de moradores registrados no banco de dados.
        """
        janela = tk.Toplevel(self.root)
        janela.title("Moradores Cadastrados")
        janela.geometry("750x400")

        tree_frame = tk.Frame(janela)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        # DEFINIÇÃO DAS COLUNAS
        colunas = ("ID", "Nome", "Bloco", "Apartamento", "Status")
        tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")

        # CABEÇALHOS
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Bloco", text="Bloco")
        tree.heading("Apartamento", text="Apto")
        tree.heading("Status", text="Status")

        # LARGURA
        tree.column("ID", width=40, anchor='center', stretch=tk.NO)
        tree.column("Nome", width=300)
        tree.column("Bloco", width=60, anchor='center')
        tree.column("Apartamento", width=60, anchor='center')
        tree.column("Status", width=80, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # LOCAL ONDE FICA OS BOTOES
        area_botoes = tk.Frame(janela)
        area_botoes.pack(fill="x", padx=10, pady=10)

        btn_detalhes = tk.Button(area_botoes, text="Ver Detalhes", width=15,
                                 command=lambda: self.mostrar_detalhes_morador(tree))
        btn_detalhes.pack(side="left", padx=5)

        btn_ativar = tk.Button(area_botoes, text="Ativar/Desativar", width=15,
                               command=lambda: self.alterar_status_morador_selecionado(tree))
        btn_ativar.pack(side="left", padx=5)

        self.popular_tabela_moradores(tree)

    def popular_tabela_moradores(self, tree):
        """
        Função para preencher a tabela com os moradores registrados (ativados e desativados).
        :param tree: tabela que será feita a visualização dos dados.
        """
        for i in tree.get_children():
            tree.delete(i)

        # Lista de moradores
        moradores = self.db.listar_todos_moradores()

        # Caso a lista nao possua moradores
        if not moradores:
            tree.insert("", "end", values=("", "Nenhum morador cadastrado", "", "", ""))
            return

        for morador in moradores:
            morador_id, nome, bloco, apto, ativo_status = morador
            status_texto = "Ativo" if ativo_status == 1 else "Inativo"
            tree.insert("", "end", values=(morador_id, nome, bloco, apto, status_texto), iid=morador_id)

    def alterar_status_morador_selecionado(self, tree):
        """
        Modifica o status do morador (entre 0 e 1 (ativado e desativado)).
        :param tree: treeview que exibirá os moradores.
        """
        selection = tree.selection()

        if not selection:
            messagebox.showwarning("Seleção", "Selecione um morador da lista.", parent=tree.winfo_toplevel())
            return

        if len(selection) > 1:
            messagebox.showwarning("Seleção", "Selecione apenas um morador.", parent=tree.winfo_toplevel())
            return

        morador_id = int(selection[0])

        valores_linha = tree.item(selection[0], 'values')
        nome_morador = valores_linha[1]
        status_atual = valores_linha[4]
        mudar_status = "Desativar" if status_atual == "Ativo" else "Ativar"

        confirmar = messagebox.askyesno("Confirmar Ação", f"Deseja {mudar_status.lower()} o morador '{nome_morador}' (ID: {morador_id})?", parent=tree.winfo_toplevel())

        if confirmar:
            sucesso = self.db.modificar_status_morador(morador_id)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Status do morador '{nome_morador}' alterado com sucesso!", parent=tree.winfo_toplevel())
                self.popular_tabela_moradores(tree)
            else:
                messagebox.showerror("Erro", f"Falha ao alterar o status do morador '{nome_morador}'.", parent=tree.winfo_toplevel())

    def mostrar_detalhes_morador(self, tree):
        """
        Abre uma janela para mostrar os detalhes (ocorrencias e visitas) do morador selecionado na treeview
        :param tree: Tabela onde será mostrado os moradores.
        """
        selection = tree.selection()

        if not selection:
            messagebox.showwarning("Seleção", "Selecione um morador para ver os detalhes.", parent=tree.winfo_toplevel())
            return
        if len(selection) > 1:
            messagebox.showwarning("Seleção", "Selecione apenas um morador.", parent=tree.winfo_toplevel())
            return

        morador_data = tree.item(selection[0], 'values')

        try:
            morador_id_texto, nome, bloco, apartamento, status_texto = morador_data
            morador_id = int(morador_id_texto)
        except ValueError:
            messagebox.showerror("Erro", "Não foi possível obter os dados do morador selecionado.", parent=tree.winfo_toplevel())
            return

        janela_detalhes = tk.Toplevel(self.root)
        janela_detalhes.title(f"Detalhes do Morador: {nome}")
        janela_detalhes.geometry("600x400")

        main_frame = tk.Frame(janela_detalhes)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        info_frame = tk.LabelFrame(main_frame, text="Informações do Morador")
        info_frame.pack(fill="x", pady=5)

        tk.Label(info_frame, text=f"ID: {morador_id}").pack(anchor="w")
        tk.Label(info_frame, text=f"Nome: {nome}").pack(anchor="w")
        tk.Label(info_frame, text=f"Bloco: {bloco}").pack(anchor="w")
        tk.Label(info_frame, text=f"Apartamento: {apartamento}").pack(anchor="w")
        tk.Label(info_frame, text=f"Status: {status_texto}").pack(anchor="w")

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True, pady=5)

        ocorrencias_frame = ttk.Frame(notebook)
        notebook.add(ocorrencias_frame, text="Ocorrências")
        tree_ocorrencias = ttk.Treeview(ocorrencias_frame, columns=("Motivo", "Status"), show="headings")
        tree_ocorrencias.heading("Motivo", text="Motivo")
        tree_ocorrencias.heading("Status", text="Status")
        tree_ocorrencias.pack(fill="both", expand=True)

        visitantes_frame = ttk.Frame(notebook)
        notebook.add(visitantes_frame, text="Visitantes")
        tree_visitantes = ttk.Treeview(visitantes_frame, columns=("Visitante", "CPF"), show="headings")
        tree_visitantes.heading("Visitante", text="Visitante")
        tree_visitantes.heading("CPF", text="CPF")
        tree_visitantes.pack(fill="both", expand=True)

        self.carregar_ocorrencias_morador(morador_id, tree_ocorrencias)
        self.carregar_visitantes_morador(morador_id, tree_visitantes)

    def carregar_ocorrencias_morador(self, morador_id, tree):
        """
        Busca as ocorrencias do morador selecionado na treeview.
        :param morador_id: ID do morador seleciado.
        :param tree: Tabela que mostra os moradores.
        """
        for i in tree.get_children():
            tree.delete(i)

        ocorrencias = self.db.listar_ocorrencias_por_morador(morador_id)

        if ocorrencias:
            for oc in ocorrencias:
                tree.insert("", "end", values=oc)
        else:
            tree.insert("", "end", values=("Nenhuma ocorrência", ""))

    def carregar_visitantes_morador(self, morador_id, tree):
        """
        Busca as visitas do morador selecionado na treeview.
        :param morador_id: ID do morador selecionado na treeview.
        :param tree: Janela que mostra os moradores.
        """
        for i in tree.get_children():
            tree.delete(i)

        visitantes = self.db.listar_visitantes_por_morador(morador_id)

        if visitantes:
            for v in visitantes: tree.insert("", "end", values=v)
        else:
            tree.insert("", "end", values=("Nenhum visitante", ""))

    #============ TELA DE VISITANTES ==============

    def abrir_janela_visitas(self):
        """
        Cria uma janela para mostrar todos as visitas feitas.
        """
        janela = tk.Toplevel(self.root)
        janela.title("Visitas Registradas")
        janela.geometry("800x400")

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tree = ttk.Treeview(frame, columns=("ID", "Visitante", "CPF", "Morador", "Data/Hora"), show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Visitante", text="Visitante")
        tree.heading("CPF", text="CPF")
        tree.heading("Morador", text="Morador")
        tree.heading("Data/Hora", text="Data/Hora")

        tree.column("ID", width=40, anchor='center', stretch=tk.NO)
        tree.column("Visitante", width=150)
        tree.column("CPF", width=200)
        tree.column("Morador", width=150)
        tree.column("Data/Hora", width=80, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        visitas = self.db.listar_visitas()
        for visita in visitas:
            tree.insert("", "end", values=(visita[0], visita[1], visita[2], visita[3], visita[4]))

    # ============ TELA DE OCORRENCIAS ==============

    def abrir_janela_ocorrencias(self):
        """
        Cria uma janela de ocorrencias para mostrar todas as registradas no banco de dados.
        """
        janela = tk.Toplevel(self.root)
        janela.title("Ocorrências Registradas")
        janela.geometry("800x400")

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Motivo", "Descrição", "Morador", "Data/Hora", "Status"), show="headings")

        tree.heading("ID", text="ID")
        tree.heading("Motivo", text="Motivo")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Morador", text="Morador")
        tree.heading("Data/Hora", text="Data/Hora")
        tree.heading("Status", text="Status")

        tree.column("ID", width=40, anchor='center', stretch=tk.NO)
        tree.column("Motivo", width=100)
        tree.column("Descrição", width=200)
        tree.column("Morador", width=150)
        tree.column("Data/Hora", width=100)
        tree.column("Status", width=80, anchor='center')

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        area_botoes = tk.Frame(janela)
        area_botoes.pack(fill="x", padx=10, pady=10)

        tk.Label(area_botoes, text="Modificar para:", anchor="w").pack(fill=tk.X)

        btn_aberto = tk.Button(area_botoes, text="Aberto", width=15,
                                 command=lambda: self.alterar_status_ocorrencia_selecionada(tree, novo_status='aberto'))
        btn_aberto.pack(side="left", padx=5)

        btn_andamento = tk.Button(area_botoes, text="Em andamento", width=15,
                                 command=lambda: self.alterar_status_ocorrencia_selecionada(tree, novo_status='em andamento'))
        btn_andamento.pack(side="left", padx=5)

        btn_fechado = tk.Button(area_botoes, text="Fechado", width=15,
                               command=lambda: self.alterar_status_ocorrencia_selecionada(tree, novo_status='fechado'))
        btn_fechado.pack(side="left", padx=5)

        self.popular_tabela_ocorrencias(tree)

    def popular_tabela_ocorrencias(self, tree):
        for i in tree.get_children():
            tree.delete(i)

        # Lista de ocorrencias
        ocorrencias = self.db.listar_ocorrencias()

        # Caso a lista nao possua moradores
        if not ocorrencias:
            tree.insert("", "end", values=("", "Nenhuma ocorrencia cadastrada", "", "", ""))
            return

        for oc in ocorrencias:
            tree.insert("", "end", values=(oc[0], oc[1], oc[2], oc[3], oc[4], oc[5].capitalize()), iid=oc[0])

    def alterar_status_ocorrencia_selecionada(self, tree, novo_status):
        selection = tree.selection()

        if not selection:
            messagebox.showwarning("Seleção", "Selecione uma ocorrencia.", parent=tree.winfo_toplevel())
            return

        if len(selection) > 1:
            messagebox.showwarning("Seleção", "Selecione apenas uma ocorrenciar.", parent=tree.winfo_toplevel())
            return

        ocorrencia_id = int(selection[0])

        valores = tree.item(selection[0], 'values')
        motivo = valores[1]
        status_atual = valores[5]

        if status_atual == novo_status:
            print("STATUS É O MESMO")
            return

        confirmar = messagebox.askyesno("Confirmar Ação", f"Deseja modificar o status da ocorrencia '{motivo}' para: {novo_status.capitalize()}.", parent=tree.winfo_toplevel())

        if confirmar:
            sucesso = self.db.modificar_status_ocorrencia(novo_status=novo_status, ocorrencia_id=ocorrencia_id)

            if sucesso:
                messagebox.showinfo("Sucesso", f"Status da ocorrencia modificada para: {novo_status}.", parent=tree.winfo_toplevel())
                self.popular_tabela_ocorrencias(tree)
            else:
                messagebox.showerror("Erro", "Falha ao alterar o status da ocorrencia.", parent=tree.winfo_toplevel())


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceListagens(root)
    root.mainloop()




