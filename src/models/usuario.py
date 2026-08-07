class Usuario:

    def __init__(
        self,
        nome,
        login,
        senha,
        perfil="Administrador",
        status="Ativo"
    ):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.perfil = perfil
        self.status = status

    def autenticar(self):
        return True

    def __str__(self):
        return f"{self.nome} - {self.login} - {self.perfil} - {self.status}"