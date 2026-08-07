from src.models.colaborador import Colaborador
from src.repositories.colaborador_repository import ColaboradorRepository

repo = ColaboradorRepository()

repo.criar_tabela()


colaborador = Colaborador("Maria Souza", "002", "Vigilante", "Segurança")

repo.inserir(colaborador)

print("Colaborador cadastrado com sucesso!")
