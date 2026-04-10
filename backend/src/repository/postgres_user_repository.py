from typing import Optional
from src.domain.interfaces import UserRepository
from src.db.connection import get_connection, release_connection


class PostgresUserRepository(UserRepository):
    """
    Implementación real de UserRepository con psycopg3.
    Las filas llegan como dicts gracias a dict_row en connection.py.
    """

    def get_by_username(self, username: str) -> Optional[dict]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, hashed_password FROM users WHERE username = %s",
                    (username,)
                )
                row = cur.fetchone()
                return dict(row) if row else None
        finally:
            release_connection(conn)

    def save(self, user_id: str, user_data: dict) -> dict:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (id, username, hashed_password)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) DO NOTHING
                    """,
                    (user_data["id"], user_data["username"], user_data["hashed_password"])
                )
                conn.commit()
            return user_data
        except Exception:
            conn.rollback()
            raise
        finally:
            release_connection(conn)
