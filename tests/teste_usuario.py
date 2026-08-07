from src.models.usuario import Usuario
from src.repositories.usuario_repository import UsuarioRepository


print("=" * 50)
print("TESTE - USUARIOS")
print("=" * 50)

repo = UsuarioRepository()

repo.criar_tabela()


print("\n[CREATE] Cadastrando usuário...")

usuario = Usuario(
    "Administrador do Sistema",
    "admin",
    "1234",
    "Administrador"
)

try:
    usuario_id = repo.inserir(usuario)

    print("OK - Usuário cadastrado!")
    print(f"ID criado: {usuario_id}")

except Exception as erro:
    print(f"ERRO: {erro}")


print("\n[READ] Buscando usuário pelo login...")

usuario_encontrado = repo.buscar_por_login("admin")

if usuario_encontrado:
    print("OK - Usuário encontrado!")
    print(f"ID:      {usuario_encontrado['id']}")
    print(f"Nome:    {usuario_encontrado['nome']}")
    print(f"Login:   {usuario_encontrado['login']}")
    print(f"Perfil:  {usuario_encontrado['perfil']}")
    print(f"Status:  {usuario_encontrado['status']}")
else:
    print("ERRO - Usuário não encontrado!")


print("\n[READ] Listando usuários...")

usuarios = repo.listar()

for usuario in usuarios:
    print(
        f"ID: {usuario['id']} | "
        f"Nome: {usuario['nome']} | "
        f"Login: {usuario['login']} | "
        f"Perfil: {usuario['perfil']} | "
        f"Status: {usuario['status']}"
    )


print("\n" + "=" * 50)
print("TESTE FINALIZADO")
print("=" * 50)