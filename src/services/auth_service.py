import hashlib
import secrets

from src.repositories.usuario_repository import UsuarioRepository


class AuthService:
    ITERATIONS = 600_000

    def __init__(self):
        self.usuario_repository = UsuarioRepository()

    @staticmethod
    def gerar_hash(senha):
        salt = secrets.token_bytes(16)

        hash_senha = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            AuthService.ITERATIONS,
        )

        return f"pbkdf2_sha256${AuthService.ITERATIONS}${salt.hex()}${hash_senha.hex()}"

    @staticmethod
    def verificar_senha(senha, senha_hash):
        try:
            algoritmo, iteracoes, salt_hex, hash_hex = senha_hash.split("$")

            if algoritmo != "pbkdf2_sha256":
                return False

            salt = bytes.fromhex(salt_hex)

            hash_calculado = hashlib.pbkdf2_hmac(
                "sha256",
                senha.encode("utf-8"),
                salt,
                int(iteracoes),
            )

            return secrets.compare_digest(
                hash_calculado.hex(),
                hash_hex,
            )

        except (ValueError, TypeError):
            return False

    def autenticar(self, login, senha):
        usuario = self.usuario_repository.buscar_por_login(login)

        if not usuario:
            return None

        if usuario["status"] != "Ativo":
            return None

        if not self.verificar_senha(senha, usuario["senha"]):
            return None

        return usuario
