from src.models.colaborador import Colaborador
from src.repositories.colaborador_repository import ColaboradorRepository
from src.services.auth_service import AuthService


class ColaboradorService:
    def __init__(self):
        self.repository = ColaboradorRepository()
        self.auth_service = AuthService()

        self.repository.criar_tabela()

    def criar(
        self,
        nome,
        matricula,
        cargo,
        setor="",
        status="Ativo",
        foto=None,
    ):
        nome = nome.strip()
        matricula = matricula.strip()
        cargo = cargo.strip()
        setor = setor.strip()

        if not nome:
            raise ValueError("Informe o nome do colaborador.")

        if not matricula:
            raise ValueError("Informe a matrícula.")

        if not cargo:
            raise ValueError("Informe o cargo.")

        colaborador = Colaborador(
            nome=nome,
            matricula=matricula,
            cargo=cargo,
            setor=setor,
            status=status,
            foto=foto,
        )

        try:
            return self.repository.inserir(
                colaborador,
            )

        except Exception as erro:
            mensagem = str(erro)

            if "UNIQUE constraint failed" in mensagem:
                raise ValueError("A matrícula informada já está cadastrada.") from erro

            raise

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(self, colaborador_id):
        return self.repository.buscar_por_id(
            colaborador_id,
        )

    def atualizar(
        self,
        colaborador_id,
        nome,
        matricula,
        cargo,
        setor="",
        status="Ativo",
        foto=None,
    ):
        nome = nome.strip()
        matricula = matricula.strip()
        cargo = cargo.strip()
        setor = setor.strip()

        if not nome:
            raise ValueError("Informe o nome do colaborador.")

        if not matricula:
            raise ValueError("Informe a matrícula.")

        if not cargo:
            raise ValueError("Informe o cargo.")

        # ==================================================
        # MANTER FOTO EXISTENTE
        # ==================================================

        if foto is None:
            colaborador_atual = self.repository.buscar_por_id(
                colaborador_id,
            )

            if colaborador_atual:
                foto = colaborador_atual["foto"]

        colaborador = Colaborador(
            nome=nome,
            matricula=matricula,
            cargo=cargo,
            setor=setor,
            status=status,
            foto=foto,
        )

        try:
            resultado = self.repository.atualizar(
                colaborador_id,
                colaborador,
            )

            if resultado == 0:
                raise ValueError("Colaborador não encontrado.")

            return resultado

        except Exception as erro:
            mensagem = str(erro)

            if "UNIQUE constraint failed" in mensagem:
                raise ValueError(
                    "A matrícula informada já está cadastrada para outro colaborador."
                ) from erro

            raise

    def excluir(
        self,
        colaborador_id,
        login_autorizador,
        senha_autorizacao,
    ):
        if not login_autorizador:
            raise ValueError("Usuário autorizador não informado.")

        if not senha_autorizacao:
            raise ValueError("Digite sua senha para autorizar.")

        usuario = self.auth_service.autenticar(
            login_autorizador,
            senha_autorizacao,
        )

        if not usuario:
            raise ValueError("Senha de autorização inválida.")

        resultado = self.repository.excluir(
            colaborador_id,
        )

        if resultado == 0:
            raise ValueError("Colaborador não encontrado.")

        return resultado
