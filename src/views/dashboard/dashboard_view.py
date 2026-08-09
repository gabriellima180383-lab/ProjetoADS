import customtkinter as ctk


class DashboardView:

    def __init__(self, usuario):
        self.usuario = usuario

        self.window = ctk.CTk()

        self.window.title("GL Secure Manager")
        self.window.geometry("1100x700")
        self.window.minsize(900, 600)

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
            text=f"{self.usuario['nome']}  |  {self.usuario['perfil']}",
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

        self.criar_botao_menu("Início")
        self.criar_botao_menu("Usuários")
        self.criar_botao_menu("Colaboradores")
        self.criar_botao_menu("Crachás")
        self.criar_botao_menu("Visitantes")
        self.criar_botao_menu("Auditorias")
        self.criar_botao_menu("Patrimônio")

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
                f"Bem-vindo, {self.usuario['nome']}!\n"
                f"Perfil: {self.usuario['perfil']}"
            ),
            font=("Arial", 17),
            justify="left",
        )
        self.boas_vindas.pack(
            anchor="w",
            padx=30,
            pady=10,
        )

    def criar_botao_menu(self, texto):
        botao = ctk.CTkButton(
            self.menu,
            text=texto,
            anchor="w",
        )
        botao.pack(
            fill="x",
            padx=20,
            pady=5,
        )

    def sair(self):
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    usuario_teste = {
        "nome": "Administrador do Sistema",
        "perfil": "Administrador",
        "status": "Ativo",
    }

    app = DashboardView(usuario_teste)
    app.run()