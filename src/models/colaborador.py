class Colaborador:
    def __init__(self, nome, matricula, cargo, setor="", status="Ativo"):

        self.nome = nome
        self.matricula = matricula
        self.cargo = cargo
        self.setor = setor
        self.status = status

    def __str__(self):

        return f"{self.nome} - {self.cargo} - {self.status}"
