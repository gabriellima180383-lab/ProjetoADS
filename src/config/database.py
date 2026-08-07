import sqlite3

from src.config.settings import DATABASE_PATH


def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def create_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS colaboradores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        matricula TEXT NOT NULL UNIQUE,
        cargo TEXT NOT NULL,
        setor TEXT,
        status TEXT NOT NULL
    )
    """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
