from src.models.usuario import Usuario
from src.repositories.usuario_repository import UsuarioRepository

print("=" * 55)
print("          TESTE CRUD - USUARIOS")
print("=" * 55)


repo = UsuarioRepository()

repo.criar_tabela()


# ==========================================================
# CREATE
# ==========================================================

print("\n[CREATE] Cadastrando usuário de teste...")

usuario = Usuario(
    "Usuário Teste",
    "teste_crud",
    "1234",
    "Operador"
)

try:
    usuario_id = repo.inserir(usuario)

    print("OK - Usuário cadastrado!")
    print(f"ID criado: {usuario_id}")

except Exception as erro:
    print(f"ERRO: {erro}")
    raise


# ==========================================================
# READ - BUSCAR POR ID
# ==========================================================

print("\n[READ] Buscando usuário pelo ID...")

usuario_encontrado = repo.buscar_por_id(usuario_id)

if usuario_encontrado:
    print(
        f"Encontrado: {usuario_encontrado['nome']} "
        f"- {usuario_encontrado['login']}"
    )
else:
    print("ERRO - Usuário não encontrado!")


# ==========================================================
# READ - BUSCAR POR LOGIN
# ==========================================================

print("\n[READ] Buscando usuário pelo login...")

usuario_login = repo.buscar_por_login("teste_crud")

if usuario_login:
    print(
        f"Encontrado: {usuario_login['nome']} "
        f"- {usuario_login['login']}"
    )
else:
    print("ERRO - Usuário não encontrado!")


# ==========================================================
# READ - LISTAR
# ==========================================================

print("\n[READ] Listando usuários...")

usuarios = repo.listar()

for usuario_item in usuarios:
    print(
        f"ID: {usuario_item['id']} | "
        f"Nome: {usuario_item['nome']} | "
        f"Login: {usuario_item['login']} | "
        f"Perfil: {usuario_item['perfil']} | "
        f"Status: {usuario_item['status']}"
    )


# ==========================================================
# UPDATE
# ==========================================================

print("\n[UPDATE] Atualizando usuário de teste...")

usuario_atualizado = Usuario(
    "Usuário Teste Atualizado",
    "teste_crud",
    "5678",
    "Administrador"
)

usuario_atualizado.status = "Inativo"

repo.atualizar(usuario_id, usuario_atualizado)

print("OK - Usuário atualizado!")


# ==========================================================
# READ - CONFERIR UPDATE
# ==========================================================

print("\n[READ] Conferindo atualização...")

usuario_atualizado_db = repo.buscar_por_id(usuario_id)

print(f"Nome:    {usuario_atualizado_db['nome']}")
print(f"Login:   {usuario_atualizado_db['login']}")
print(f"Perfil:  {usuario_atualizado_db['perfil']}")
print(f"Status:  {usuario_atualizado_db['status']}")


# ==========================================================
# DELETE
# ==========================================================

print("\n[DELETE] Excluindo usuário de teste...")

repo.excluir(usuario_id)

print("OK - Usuário excluído!")


# ==========================================================
# READ - VERIFICAÇÃO FINAL
# ==========================================================

print("\n[READ] Verificação final...")

usuario_excluido = repo.buscar_por_id(usuario_id)

if usuario_excluido is None:
    print("OK - Registro removido com sucesso!")
else:
    print("ERRO - Registro ainda existe!")


print("\n" + "=" * 55)
print("             TESTE FINALIZADO")
print("=" * 55)