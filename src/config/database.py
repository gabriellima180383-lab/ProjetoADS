import sqlite3

from src.config.settings import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def create_database():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ==================================================
        # USUÁRIOS
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                login TEXT NOT NULL,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Ativo',
                foto TEXT
            )
            """
        )

        # ==================================================
        # MIGRAÇÃO DA TABELA USUÁRIOS
        # ==================================================

        cursor.execute("PRAGMA table_info(usuarios)")

        colunas_usuarios = [coluna["name"] for coluna in cursor.fetchall()]

        if "foto" not in colunas_usuarios:
            cursor.execute(
                """
                ALTER TABLE usuarios
                ADD COLUMN foto TEXT
                """
            )

        # ==================================================
        # COLABORADORES
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS colaboradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                cargo TEXT NOT NULL,
                setor TEXT,
                status TEXT NOT NULL DEFAULT 'Ativo',
                foto TEXT
            )
            """
        )

        # ==================================================
        # MIGRAÇÃO DA TABELA COLABORADORES
        # ==================================================

        cursor.execute("PRAGMA table_info(colaboradores)")

        colunas_colaboradores = [coluna["name"] for coluna in cursor.fetchall()]

        if "foto" not in colunas_colaboradores:
            cursor.execute(
                """
                ALTER TABLE colaboradores
                ADD COLUMN foto TEXT
                """
            )

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":
    create_database()
