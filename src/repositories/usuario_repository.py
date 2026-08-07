from src.config.database import get_connection


class UsuarioRepository:

    def criar_tabela(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                login TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                perfil TEXT NOT NULL DEFAULT 'Operador',
                status TEXT NOT NULL DEFAULT 'Ativo'
            )
        """)

        conn.commit()
        conn.close()

    def inserir(self, usuario):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios
            (nome, login, senha, perfil, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                usuario.nome,
                usuario.login,
                usuario.senha,
                usuario.perfil,
                usuario.status,
            ),
        )

        usuario_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return usuario_id

    def buscar_por_login(self, login):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, nome, login, senha, perfil, status
            FROM usuarios
            WHERE login = ?
            """,
            (login,),
        )

        usuario = cursor.fetchone()

        conn.close()

        return usuario

    def listar(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nome, login, senha, perfil, status
            FROM usuarios
            ORDER BY nome
        """)

        usuarios = cursor.fetchall()

        conn.close()

        return usuarios
