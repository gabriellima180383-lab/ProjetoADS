from src.config.database import get_connection


class UsuarioRepository:
    def criar_tabela(self):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    login TEXT NOT NULL,
                    senha TEXT NOT NULL,
                    perfil TEXT NOT NULL DEFAULT 'Operador',
                    status TEXT NOT NULL DEFAULT 'Ativo'
                )
            """)

            conn.commit()

        finally:
            conn.close()

    def inserir(self, usuario):
        conn = get_connection()

        try:
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

            conn.commit()

            return cursor.lastrowid

        finally:
            conn.close()

    def buscar_por_id(self, usuario_id):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, nome, login, senha, perfil, status
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            )

            usuario = cursor.fetchone()

            if usuario:
                return dict(usuario)

            return None

        finally:
            conn.close()

    def buscar_por_login(self, login):
        conn = get_connection()

        try:
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

            if usuario:
                return dict(usuario)

            return None

        finally:
            conn.close()

    def listar(self):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nome, login, senha, perfil, status
                FROM usuarios
                ORDER BY nome
            """)

            usuarios = cursor.fetchall()

            return [dict(usuario) for usuario in usuarios]

        finally:
            conn.close()

    def atualizar(self, usuario_id, usuario):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE usuarios
                SET nome = ?,
                    login = ?,
                    senha = ?,
                    perfil = ?,
                    status = ?
                WHERE id = ?
                """,
                (
                    usuario.nome,
                    usuario.login,
                    usuario.senha,
                    usuario.perfil,
                    usuario.status,
                    usuario_id,
                ),
            )

            conn.commit()

            return cursor.rowcount

        finally:
            conn.close()

    def excluir(self, usuario_id):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            )

            conn.commit()

            return cursor.rowcount

        finally:
            conn.close()
