import customtkinter as ctk

from src.services.auth_service import AuthService


class LoginView:
    def __init__(self):
        self.window = ctk.CTk()

        self.window.title("GL Secure Manager")
        self.window.geometry("500x350")
        self.window.resizable(False, False)

        self.auth_service = AuthService()

        self.criar_interface()

    def criar_interface(self):
        self.titulo = ctk.CTkLabel(
            self.window,
            text="GL Secure Manager",
            font=("Arial", 26, "bold"),
        )
        self.titulo.pack(pady=(40, 30))

        self.login_entry = ctk.CTkEntry(
            self.window,
            width=300,
            height=40,
            placeholder_text="Login",
        )
        self.login_entry.pack(pady=10)

        self.senha_entry = ctk.CTkEntry(
            self.window,
            width=300,
            height=40,
            placeholder_text="Senha",
            show="*",
        )
        self.senha_entry.pack(pady=10)

        self.mensagem = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 14),
        )
        self.mensagem.pack(pady=(10, 5))

        self.botao_entrar = ctk.CTkButton(
            self.window,
            width=300,
            height=40,
            text="ENTRAR",
            command=self.autenticar,
        )
        self.botao_entrar.pack(pady=10)

        self.senha_entry.bind("<Return>", lambda event: self.autenticar())

        self.login_entry.focus()

    def autenticar(self):
        login = self.login_entry.get().strip()
        senha = self.senha_entry.get()

        if not login or not senha:
            self.mensagem.configure(text="Informe o login e a senha.")
            return

        usuario = self.auth_service.autenticar(login, senha)

        if usuario:
            self.mensagem.configure(text=f"Bem-vindo, {usuario['nome']}!")

            print("LOGIN REALIZADO COM SUCESSO")
            print(f"Usuário: {usuario['nome']}")
            print(f"Perfil: {usuario['perfil']}")

        else:
            self.mensagem.configure(text="Login ou senha inválidos.")

            self.senha_entry.delete(0, "end")
            self.senha_entry.focus()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = LoginView()
    app.run()
