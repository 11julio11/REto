from typing import List, Optional
from domain.interfaces import ItemRepository
from domain.schemas import ItemResponse
from db.connection import get_connection, release_connection


class PostgresItemRepository(ItemRepository):
    """
    Implementación real de ItemRepository con psycopg3.
    Usa dict_row (configurado en connection.py) — las filas son dicts.
    """

    def get_all(self) -> List[ItemResponse]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, description, price, created_at FROM items ORDER BY created_at DESC"
                )
                rows = cur.fetchall()
                return [
                    ItemResponse(
                        id=row["id"],
                        name=row["name"],
                        description=row["description"],
                        price=float(row["price"]),
                        created_at=str(row["created_at"])
                    )
                    for row in rows
                ]
        finally:
            release_connection(conn)

    def get_by_id(self, item_id: str) -> Optional[ItemResponse]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, description, price, created_at FROM items WHERE id = %s",
                    (item_id,)
                )
                row = cur.fetchone()
                if row:
                    return ItemResponse(
                        id=row["id"],
                        name=row["name"],
                        description=row["description"],
                        price=float(row["price"]),
                        created_at=str(row["created_at"])
                    )
                return None
        finally:
            release_connection(conn)

    def save(self, item_id: str, item_data: dict) -> ItemResponse:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO items (id, name, description, price, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        description = EXCLUDED.description,
                        price = EXCLUDED.price
                    """,
                    (
                        item_data["id"],
                        item_data["name"],
                        item_data.get("description"),
                        item_data["price"],
                        item_data["created_at"],
                    )
                )
                conn.commit()
            return ItemResponse(**item_data)
        except Exception:
            conn.rollback()
            raise
        finally:
            release_connection(conn)

    def delete(self, item_id: str) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            release_connection(conn)
