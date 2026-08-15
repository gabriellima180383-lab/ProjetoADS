class Colaborador:
    def __init__(
        self,
        nome,
        matricula,
        cargo,
        setor="",
        status="Ativo",
        foto=None,
    ):
        self.nome = nome
        self.matricula = matricula
        self.cargo = cargo
        self.setor = setor
        self.status = status
        self.foto = foto

    def __str__(self):
        return f"{self.nome} - {self.matricula} - {self.cargo} - {self.status}"
