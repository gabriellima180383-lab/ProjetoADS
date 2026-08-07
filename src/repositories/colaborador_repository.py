from src.config.database import get_connection


class ColaboradorRepository:

    def criar_tabela(self):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS colaboradores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    matricula TEXT NOT NULL UNIQUE,
                    cargo TEXT NOT NULL,
                    setor TEXT,
                    status TEXT DEFAULT 'Ativo'
                )
            """)

            conn.commit()

        finally:
            conn.close()

    def inserir(self, colaborador):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO colaboradores
                (nome, matricula, cargo, setor, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                colaborador.nome,
                colaborador.matricula,
                colaborador.cargo,
                colaborador.setor,
                colaborador.status
            ))

            conn.commit()

            return cursor.lastrowid

        finally:
            conn.close()

    def listar(self):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nome, matricula, cargo, setor, status
                FROM colaboradores
                ORDER BY nome
            """)

            return cursor.fetchall()

        finally:
            conn.close()

    def buscar_por_id(self, colaborador_id):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nome, matricula, cargo, setor, status
                FROM colaboradores
                WHERE id = ?
            """, (colaborador_id,))

            return cursor.fetchone()

        finally:
            conn.close()

    def atualizar(self, colaborador_id, colaborador):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE colaboradores
                SET nome = ?,
                    matricula = ?,
                    cargo = ?,
                    setor = ?,
                    status = ?
                WHERE id = ?
            """, (
                colaborador.nome,
                colaborador.matricula,
                colaborador.cargo,
                colaborador.setor,
                colaborador.status,
                colaborador_id
            ))

            conn.commit()

            return cursor.rowcount

        finally:
            conn.close()

    def excluir(self, colaborador_id):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM colaboradores
                WHERE id = ?
            """, (colaborador_id,))

            conn.commit()

            return cursor.rowcount

        finally:
            conn.close()