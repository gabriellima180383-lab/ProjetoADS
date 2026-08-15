import customtkinter as ctk

from src.views.colaboradores.colaborador_view import ColaboradorView
from src.views.usuarios.usuario_view import UsuarioView


class DashboardView:
    def __init__(self, master, usuario):
        self.master = master
        self.usuario = usuario

        self.usuario_view = None
        self.colaborador_view = None

        self.window = ctk.CTkToplevel(master)

        self.window.title("GL Secure Manager")

        self.window.geometry("1100x700")

        self.window.minsize(
            900,
            600,
        )

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.fechar,
        )

        self.criar_interface()

    def criar_interface(self):

        # ==========================
        # CABEÇALHO
        # ==========================

        self.header = ctk.CTkFrame(
            self.window,
            height=70,
            corner_radius=0,
        )

        self.header.pack(
            side="top",
            fill="x",
        )

        self.titulo = ctk.CTkLabel(
            self.header,
            text="GL Secure Manager",
            font=("Arial", 24, "bold"),
        )

        self.titulo.pack(
            side="left",
            padx=25,
            pady=15,
        )

        self.usuario_label = ctk.CTkLabel(
            self.header,
            text=(f"{self.usuario['nome']}  |  {self.usuario['perfil']}"),
            font=("Arial", 14),
        )

        self.usuario_label.pack(
            side="right",
            padx=25,
        )

        # ==========================
        # MENU LATERAL
        # ==========================

        self.menu = ctk.CTkFrame(
            self.window,
            width=220,
            corner_radius=0,
        )

        self.menu.pack(
            side="left",
            fill="y",
        )

        self.menu.pack_propagate(False)

        self.menu_titulo = ctk.CTkLabel(
            self.menu,
            text="MENU",
            font=("Arial", 16, "bold"),
        )

        self.menu_titulo.pack(
            pady=(30, 20),
        )

        self.criar_botao_menu(
            "Início",
            self.abrir_inicio,
        )

        self.criar_botao_menu(
            "Usuários",
            self.abrir_usuarios,
        )

        self.criar_botao_menu(
            "Colaboradores",
            self.abrir_colaboradores,
        )

        self.criar_botao_menu(
            "Crachás",
        )

        self.criar_botao_menu(
            "Visitantes",
        )

        self.criar_botao_menu(
            "Auditorias",
        )

        self.criar_botao_menu(
            "Patrimônio",
        )

        # ==========================
        # BOTÃO SAIR
        # ==========================

        self.botao_sair = ctk.CTkButton(
            self.menu,
            text="Sair",
            command=self.sair,
        )

        self.botao_sair.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=20,
        )

        # ==========================
        # ÁREA PRINCIPAL
        # ==========================

        self.conteudo = ctk.CTkFrame(
            self.window,
            corner_radius=0,
        )

        self.conteudo.pack(
            side="right",
            fill="both",
            expand=True,
            padx=15,
            pady=15,
        )

        self.titulo_conteudo = ctk.CTkLabel(
            self.conteudo,
            text="Painel de Controle",
            font=("Arial", 28, "bold"),
        )

        self.titulo_conteudo.pack(
            anchor="w",
            padx=30,
            pady=(30, 10),
        )

        self.boas_vindas = ctk.CTkLabel(
            self.conteudo,
            text=(
                f"Bem-vindo, {self.usuario['nome']}!\nPerfil: {self.usuario['perfil']}"
            ),
            font=("Arial", 17),
            justify="left",
        )

        self.boas_vindas.pack(
            anchor="w",
            padx=30,
            pady=10,
        )

    # ==================================================
    # BOTÃO DO MENU
    # ==================================================

    def criar_botao_menu(
        self,
        texto,
        comando=None,
    ):
        botao = ctk.CTkButton(
            self.menu,
            text=texto,
            anchor="w",
            command=comando,
        )

        botao.pack(
            fill="x",
            padx=20,
            pady=5,
        )

    # ==================================================
    # INÍCIO
    # ==================================================

    def abrir_inicio(self):
        print("Painel inicial selecionado.")

    # ==================================================
    # USUÁRIOS
    # ==================================================

    def abrir_usuarios(self):

        if self.usuario_view is not None and self.usuario_view.window.winfo_exists():
            self.usuario_view.window.lift()
            self.usuario_view.window.focus_force()
            return

        self.window.withdraw()

        self.usuario_view = UsuarioView(
            master=self.window,
            usuario=self.usuario,
        )

    # ==================================================
    # COLABORADORES
    # ==================================================

    def abrir_colaboradores(self):

        if (
            self.colaborador_view is not None
            and self.colaborador_view.window.winfo_exists()
        ):
            self.colaborador_view.window.lift()
            self.colaborador_view.window.focus_force()
            return

        self.window.withdraw()

        self.colaborador_view = ColaboradorView(
            master=self.window,
            usuario=self.usuario,
        )

    # ==================================================
    # SAIR
    # ==================================================

    def sair(self):
        self.fechar()

    # ==================================================
    # FECHAR DASHBOARD
    # ==================================================

    def fechar(self):

        if self.usuario_view is not None and self.usuario_view.window.winfo_exists():
            self.usuario_view.fechar()

        if (
            self.colaborador_view is not None
            and self.colaborador_view.window.winfo_exists()
        ):
            self.colaborador_view.fechar()

        self.window.destroy()

        if self.master.winfo_exists():
            self.master.destroy()

    # ==================================================
    # EXECUÇÃO
    # ==================================================

    def run(self):
        self.window.deiconify()


if __name__ == "__main__":
    print("Execute o sistema pelo LoginView.")
