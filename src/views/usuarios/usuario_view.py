from tkinter import ttk

import customtkinter as ctk

from src.services.usuario_service import UsuarioService


class UsuarioView:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario
        self.service = UsuarioService()
        self.usuario_selecionado = None

        self.window = ctk.CTkToplevel(master)

        self.window.title("GL Secure Manager - Usuários")
        self.window.geometry("1100x700")
        self.window.minsize(900, 600)

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.fechar,
        )

        self.criar_interface()

    def criar_interface(self):

        # ==========================
        # TÍTULO
        # ==========================

        self.titulo = ctk.CTkLabel(
            self.window,
            text="Gestão de Usuários",
            font=("Arial", 28, "bold"),
        )

        self.titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 10),
        )

        # ==========================
        # USUÁRIO LOGADO
        # ==========================

        self.usuario_logado = ctk.CTkLabel(
            self.window,
            text=(
                f"Usuário logado: "
                f"{self.usuario['nome']} | "
                f"Perfil: "
                f"{self.usuario['perfil']}"
            ),
            font=("Arial", 14),
        )

        self.usuario_logado.pack(
            anchor="w",
            padx=30,
            pady=(0, 20),
        )

        # ==========================
        # BOTÕES DE AÇÃO
        # ==========================

        self.frame_acoes = ctk.CTkFrame(
            self.window,
            fg_color="transparent",
        )

        self.frame_acoes.pack(
            fill="x",
            padx=30,
            pady=(0, 10),
        )

        self.botao_novo = ctk.CTkButton(
            self.frame_acoes,
            text="Novo Usuário",
            width=150,
            command=self.novo_usuario,
        )

        self.botao_novo.pack(
            side="left",
        )

        self.botao_editar = ctk.CTkButton(
            self.frame_acoes,
            text="Editar Usuário",
            width=150,
            command=self.editar_usuario,
        )

        self.botao_editar.pack(
            side="left",
            padx=10,
        )

        self.botao_excluir = ctk.CTkButton(
            self.frame_acoes,
            text="Excluir Usuário",
            width=150,
            command=self.excluir_usuario,
        )

        self.botao_excluir.pack(
            side="left",
        )

        # ==========================
        # TABELA
        # ==========================

        self.tabela = ttk.Treeview(
            self.window,
            columns=(
                "id",
                "nome",
                "login",
                "perfil",
                "status",
            ),
            show="headings",
        )

        self.tabela.heading(
            "id",
            text="ID",
        )

        self.tabela.heading(
            "nome",
            text="Nome",
        )

        self.tabela.heading(
            "login",
            text="Login",
        )

        self.tabela.heading(
            "perfil",
            text="Perfil",
        )

        self.tabela.heading(
            "status",
            text="Status",
        )

        self.tabela.column(
            "id",
            width=60,
            anchor="center",
        )

        self.tabela.column(
            "nome",
            width=300,
        )

        self.tabela.column(
            "login",
            width=180,
        )

        self.tabela.column(
            "perfil",
            width=180,
        )

        self.tabela.column(
            "status",
            width=120,
            anchor="center",
        )

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10,
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar_usuario,
        )

        self.carregar_usuarios()

    def carregar_usuarios(self):

        usuarios = self.service.listar()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for usuario in usuarios:
            self.tabela.insert(
                "",
                "end",
                values=(
                    usuario["id"],
                    usuario["nome"],
                    usuario["login"],
                    usuario["perfil"],
                    usuario["status"],
                ),
            )

    def selecionar_usuario(self, event=None):

        selecao = self.tabela.selection()

        if not selecao:
            self.usuario_selecionado = None
            return

        item = selecao[0]

        valores = self.tabela.item(
            item,
            "values",
        )

        self.usuario_selecionado = int(valores[0])

        print(f"Usuário selecionado: ID {self.usuario_selecionado}")

    # ==================================================
    # NOVO USUÁRIO
    # ==================================================

    def novo_usuario(self):

        self.janela_novo = ctk.CTkToplevel(
            self.window,
        )

        self.janela_novo.title(
            "Novo Usuário",
        )

        self.janela_novo.geometry(
            "500x550",
        )

        self.janela_novo.resizable(
            False,
            False,
        )

        self.janela_novo.transient(
            self.window,
        )

        self.janela_novo.grab_set()

        titulo = ctk.CTkLabel(
            self.janela_novo,
            text="Novo Usuário",
            font=("Arial", 24, "bold"),
        )

        titulo.pack(
            pady=(30, 25),
        )

        self.nome_entry = ctk.CTkEntry(
            self.janela_novo,
            width=350,
            height=40,
            placeholder_text="Nome completo",
        )

        self.nome_entry.pack(
            pady=10,
        )

        self.login_entry = ctk.CTkEntry(
            self.janela_novo,
            width=350,
            height=40,
            placeholder_text="Login",
        )

        self.login_entry.pack(
            pady=10,
        )

        self.senha_entry = ctk.CTkEntry(
            self.janela_novo,
            width=350,
            height=40,
            placeholder_text="Senha",
            show="*",
        )

        self.senha_entry.pack(
            pady=10,
        )

        self.perfil_combo = ctk.CTkComboBox(
            self.janela_novo,
            width=350,
            height=40,
            values=[
                "Administrador",
                "Supervisor",
                "Operador",
            ],
        )

        self.perfil_combo.pack(
            pady=10,
        )

        self.perfil_combo.set(
            "Operador",
        )

        self.status_combo = ctk.CTkComboBox(
            self.janela_novo,
            width=350,
            height=40,
            values=[
                "Ativo",
                "Inativo",
            ],
        )

        self.status_combo.pack(
            pady=10,
        )

        self.status_combo.set(
            "Ativo",
        )

        self.mensagem_novo = ctk.CTkLabel(
            self.janela_novo,
            text="",
            font=("Arial", 13),
        )

        self.mensagem_novo.pack(
            pady=(10, 5),
        )

        self.botao_salvar = ctk.CTkButton(
            self.janela_novo,
            width=350,
            height=40,
            text="SALVAR",
            command=self.salvar_novo_usuario,
        )

        self.botao_salvar.pack(
            pady=10,
        )

        self.nome_entry.focus()

    def salvar_novo_usuario(self):

        nome = self.nome_entry.get()
        login = self.login_entry.get()
        senha = self.senha_entry.get()
        perfil = self.perfil_combo.get()
        status = self.status_combo.get()

        try:
            usuario_id = self.service.criar(
                nome=nome,
                login=login,
                senha=senha,
                perfil=perfil,
                status=status,
            )

            print(f"Usuário criado com sucesso. ID: {usuario_id}")

            self.janela_novo.destroy()

            self.carregar_usuarios()

        except ValueError as erro:
            self.mensagem_novo.configure(
                text=str(erro),
            )

    # ==================================================
    # EDITAR USUÁRIO
    # ==================================================

    def editar_usuario(self):

        if not self.usuario_selecionado:
            print("Nenhum usuário selecionado.")
            return

        usuario = self.service.buscar_por_id(
            self.usuario_selecionado,
        )

        if not usuario:
            print("Usuário não encontrado.")
            return

        self.janela_editar = ctk.CTkToplevel(
            self.window,
        )

        self.janela_editar.title(
            "Editar Usuário",
        )

        self.janela_editar.geometry(
            "500x550",
        )

        self.janela_editar.resizable(
            False,
            False,
        )

        self.janela_editar.transient(
            self.window,
        )

        self.janela_editar.grab_set()

        titulo = ctk.CTkLabel(
            self.janela_editar,
            text="Editar Usuário",
            font=("Arial", 24, "bold"),
        )

        titulo.pack(
            pady=(30, 25),
        )

        self.nome_editar_entry = ctk.CTkEntry(
            self.janela_editar,
            width=350,
            height=40,
        )

        self.nome_editar_entry.pack(
            pady=10,
        )

        self.nome_editar_entry.insert(
            0,
            usuario["nome"],
        )

        self.login_editar_entry = ctk.CTkEntry(
            self.janela_editar,
            width=350,
            height=40,
        )

        self.login_editar_entry.pack(
            pady=10,
        )

        self.login_editar_entry.insert(
            0,
            usuario["login"],
        )

        self.senha_editar_entry = ctk.CTkEntry(
            self.janela_editar,
            width=350,
            height=40,
            placeholder_text=("Nova senha (deixe vazio para manter)"),
            show="*",
        )

        self.senha_editar_entry.pack(
            pady=10,
        )

        self.perfil_editar_combo = ctk.CTkComboBox(
            self.janela_editar,
            width=350,
            height=40,
            values=[
                "Administrador",
                "Supervisor",
                "Operador",
            ],
        )

        self.perfil_editar_combo.pack(
            pady=10,
        )

        self.perfil_editar_combo.set(
            usuario["perfil"],
        )

        self.status_editar_combo = ctk.CTkComboBox(
            self.janela_editar,
            width=350,
            height=40,
            values=[
                "Ativo",
                "Inativo",
            ],
        )

        self.status_editar_combo.pack(
            pady=10,
        )

        self.status_editar_combo.set(
            usuario["status"],
        )

        self.mensagem_editar = ctk.CTkLabel(
            self.janela_editar,
            text="",
            font=("Arial", 13),
        )

        self.mensagem_editar.pack(
            pady=(10, 5),
        )

        self.botao_salvar_edicao = ctk.CTkButton(
            self.janela_editar,
            width=350,
            height=40,
            text="SALVAR ALTERAÇÕES",
            command=self.salvar_edicao_usuario,
        )

        self.botao_salvar_edicao.pack(
            pady=10,
        )

        self.nome_editar_entry.focus()

    def salvar_edicao_usuario(self):

        nome = self.nome_editar_entry.get()
        login = self.login_editar_entry.get()
        senha = self.senha_editar_entry.get()
        perfil = self.perfil_editar_combo.get()
        status = self.status_editar_combo.get()

        try:
            self.service.atualizar(
                usuario_id=self.usuario_selecionado,
                nome=nome,
                login=login,
                senha=senha,
                perfil=perfil,
                status=status,
            )

            print(f"Usuário ID {self.usuario_selecionado} atualizado com sucesso.")

            self.janela_editar.destroy()

            self.carregar_usuarios()

            self.usuario_selecionado = None

        except ValueError as erro:
            self.mensagem_editar.configure(
                text=str(erro),
            )

    # ==================================================
    # EXCLUIR USUÁRIO
    # ==================================================

    def excluir_usuario(self):

        if not self.usuario_selecionado:
            print("Nenhum usuário selecionado.")
            return

        usuario = self.service.buscar_por_id(
            self.usuario_selecionado,
        )

        if not usuario:
            print("Usuário não encontrado.")
            return

        self.janela_autorizacao = ctk.CTkToplevel(
            self.window,
        )

        self.janela_autorizacao.title(
            "Autorizar exclusão",
        )

        self.janela_autorizacao.geometry(
            "500x350",
        )

        self.janela_autorizacao.resizable(
            False,
            False,
        )

        self.janela_autorizacao.transient(
            self.window,
        )

        self.janela_autorizacao.grab_set()

        titulo = ctk.CTkLabel(
            self.janela_autorizacao,
            text="Autorizar Exclusão",
            font=("Arial", 24, "bold"),
        )

        titulo.pack(
            pady=(30, 20),
        )

        informacao = ctk.CTkLabel(
            self.janela_autorizacao,
            text=(
                "Usuário selecionado:\n"
                f"{usuario['nome']}\n\n"
                "Esta operação não poderá "
                "ser desfeita."
            ),
            font=("Arial", 14),
            justify="center",
        )

        informacao.pack(
            pady=(0, 20),
        )

        self.senha_autorizacao_entry = ctk.CTkEntry(
            self.janela_autorizacao,
            width=350,
            height=40,
            placeholder_text=("Digite sua senha para autorizar"),
            show="*",
        )

        self.senha_autorizacao_entry.pack(
            pady=10,
        )

        self.mensagem_autorizacao = ctk.CTkLabel(
            self.janela_autorizacao,
            text="",
            font=("Arial", 13),
        )

        self.mensagem_autorizacao.pack(
            pady=5,
        )

        frame_botoes = ctk.CTkFrame(
            self.janela_autorizacao,
            fg_color="transparent",
        )

        frame_botoes.pack(
            pady=15,
        )

        botao_cancelar = ctk.CTkButton(
            frame_botoes,
            text="CANCELAR",
            width=150,
            command=self.janela_autorizacao.destroy,
        )

        botao_cancelar.pack(
            side="left",
            padx=5,
        )

        botao_confirmar = ctk.CTkButton(
            frame_botoes,
            text="CONFIRMAR",
            width=150,
            command=self.confirmar_exclusao,
        )

        botao_confirmar.pack(
            side="left",
            padx=5,
        )

        self.senha_autorizacao_entry.focus()

    def confirmar_exclusao(self):

        senha = self.senha_autorizacao_entry.get()

        if not senha:
            self.mensagem_autorizacao.configure(
                text="Digite sua senha.",
            )
            return

        try:
            self.service.excluir(
                usuario_id=self.usuario_selecionado,
                login_autorizador=self.usuario["login"],
                senha_autorizacao=senha,
            )

            print(f"Usuário ID {self.usuario_selecionado} excluído com sucesso.")

            self.usuario_selecionado = None

            self.janela_autorizacao.destroy()

            self.carregar_usuarios()

        except ValueError as erro:
            self.mensagem_autorizacao.configure(
                text=str(erro),
            )

    # ==================================================
    # FECHAR
    # ==================================================

    def fechar(self):

        self.window.destroy()

        if self.master.winfo_exists():
            self.master.deiconify()
            self.master.focus_force()
