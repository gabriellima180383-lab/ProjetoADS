class Usuario:
    def __init__(self, nome, login, senha, perfil="Administrador"):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.perfil = perfil

    def autenticar(self):
        return True

    def __str__(self):
        return f"{self.nome} - {self.login} - {self.perfil}"