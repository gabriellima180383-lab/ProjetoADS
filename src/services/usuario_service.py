from src.models.usuario import Usuario
from src.repositories.usuario_repository import UsuarioRepository
from src.services.auth_service import AuthService


class UsuarioService:

    def __init__(self):
        self.repository = UsuarioRepository()

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(self, usuario_id):
        return self.repository.buscar_por_id(usuario_id)

    def criar(self, nome, login, senha, perfil="Operador", status="Ativo"):
        nome = nome.strip()
        login = login.strip()

        if not nome:
            raise ValueError("O nome é obrigatório.")

        if not login:
            raise ValueError("O login é obrigatório.")

        if not senha:
            raise ValueError("A senha é obrigatória.")

        if self.repository.buscar_por_login(login):
            raise ValueError("Este login já está cadastrado.")

        senha_hash = AuthService.gerar_hash(senha)

        usuario = Usuario(
            nome=nome,
            login=login,
            senha=senha_hash,
            perfil=perfil,
            status=status,
        )

        return self.repository.inserir(usuario)

    def atualizar(
        self,
        usuario_id,
        nome,
        login,
        senha=None,
        perfil="Operador",
        status="Ativo",
    ):
        nome = nome.strip()
        login = login.strip()

        if not nome:
            raise ValueError("O nome é obrigatório.")

        if not login:
            raise ValueError("O login é obrigatório.")

        usuario_atual = self.repository.buscar_por_id(usuario_id)

        if not usuario_atual:
            raise ValueError("Usuário não encontrado.")

        usuario_login = self.repository.buscar_por_login(login)

        if usuario_login and usuario_login["id"] != usuario_id:
            raise ValueError("Este login já está sendo utilizado.")

        if senha:
            senha_hash = AuthService.gerar_hash(senha)
        else:
            senha_hash = usuario_atual["senha"]

        usuario = Usuario(
            nome=nome,
            login=login,
            senha=senha_hash,
            perfil=perfil,
            status=status,
        )

        return self.repository.atualizar(usuario_id, usuario)

    def excluir(self, usuario_id):
        usuario = self.repository.buscar_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if usuario["login"] == "admin":
            raise ValueError("O usuário administrador principal não pode ser excluído.")

        return self.repository.excluir(usuario_id)