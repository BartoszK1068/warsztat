"""
db_init.py -  inicjalizacja bazy SQLite dla systemu zgłoszeń / warsztatu.

Tabele:
- utworzone_konta
- zgloszenia
- harmonogram
- zgloszenia_archiwum
"""

import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = "data/base.db"

def get_connection (db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Zwraca połączenie do bazy danych i włącza obsługę kluczy obcych.
    """
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_table_utworzone_konta(conn: sqlite3.Connection) -> None:
    """
    Tworzy tabelę kont użytkowników, jeśli nie istnieje.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS utworzone_konta (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        login        TEXT NOT NULL UNIQUE,
        haslo_hash   TEXT NOT NULL,
        uprawnienie  TEXT NOT NULL CHECK (uprawnienie IN ('admin', 'pracownik', 'klient'))
    );
    """
    conn.execute(sql)


def init_db(db_path: Optional[str] = None) -> None:
    """
    Główna funkcja inicjalizująca bazę:
    - tworzy plik bazy (jeśli nie istnieje),
    - tworzy wszystkie tabele (IF NOT EXISTS),
    - commit i zamknięcie połączenia.
    """
    path = db_path or DB_PATH
    # upewniamy się że katalog istnieje (jeśli ścieżka jest z podkatalogiem)
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection(path)
    try:
        create_table_utworzone_konta(conn)
        conn.commit()
    finally:
        conn.close()






if __name__ == "__main__":
    init_db()
    print(f"Baza zainicjalizowana: {DB_PATH}")
