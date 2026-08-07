from src.models.colaborador import Colaborador
from src.repositories.colaborador_repository import ColaboradorRepository


print("=" * 50)
print("       TESTE CRUD - COLABORADORES")
print("=" * 50)


repo = ColaboradorRepository()

repo.criar_tabela()


# ==================================================
# CREATE
# ==================================================

print("\n[CREATE] Cadastrando colaborador de teste...")

colaborador = Colaborador(
    "Colaborador Teste",
    "999",
    "Vigilante",
    "Segurança Patrimonial"
)

try:
    colaborador_id = repo.inserir(colaborador)

    print("OK - Colaborador cadastrado!")
    print(f"ID criado: {colaborador_id}")

except Exception as erro:
    print(f"ERRO: {erro}")
    raise


# ==================================================
# READ
# ==================================================

print("\n[READ] Listando colaboradores...")

colaboradores = repo.listar()

for item in colaboradores:
    print(
        f"ID: {item['id']} | "
        f"Nome: {item['nome']} | "
        f"Matrícula: {item['matricula']} | "
        f"Cargo: {item['cargo']} | "
        f"Setor: {item['setor']} | "
        f"Status: {item['status']}"
    )


# ==================================================
# BUSCAR
# ==================================================

print("\n[READ] Buscando colaborador criado...")

registro = repo.buscar_por_id(colaborador_id)

if registro:
    print(
        f"Encontrado: {registro['nome']} - "
        f"{registro['cargo']}"
    )
else:
    print("ERRO - Colaborador não encontrado.")


# ==================================================
# UPDATE
# ==================================================

print("\n[UPDATE] Atualizando colaborador de teste...")

colaborador_atualizado = Colaborador(
    "Colaborador Teste Atualizado",
    "999",
    "Supervisor de Segurança",
    "Segurança Patrimonial",
    "Ativo"
)

linhas = repo.atualizar(
    colaborador_id,
    colaborador_atualizado
)

if linhas:
    print("OK - Colaborador atualizado!")
else:
    print("ERRO - Nenhum registro foi atualizado.")


# ==================================================
# READ APÓS UPDATE
# ==================================================

print("\n[READ] Conferindo atualização...")

registro = repo.buscar_por_id(colaborador_id)

if registro:
    print(f"Nome:    {registro['nome']}")
    print(f"Cargo:   {registro['cargo']}")
    print(f"Setor:   {registro['setor']}")
    print(f"Status:  {registro['status']}")


# ==================================================
# DELETE
# ==================================================

print("\n[DELETE] Excluindo colaborador de teste...")

linhas = repo.excluir(colaborador_id)

if linhas:
    print("OK - Colaborador excluído!")
else:
    print("ERRO - Nenhum registro foi excluído.")


# ==================================================
# VERIFICAÇÃO FINAL
# ==================================================

print("\n[READ] Verificação final...")

registro = repo.buscar_por_id(colaborador_id)

if registro is None:
    print("OK - Registro removido com sucesso!")
else:
    print("ERRO - Registro ainda existe.")


print("\n" + "=" * 50)
print("           TESTE CRUD FINALIZADO")
print("=" * 50)