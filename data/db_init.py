"""
db_init.py - inicjalizacja bazy SQLite dla systemu zgłoszeń / warsztatu.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from werkzeug.security import generate_password_hash

DB_PATH = "data/base.db"


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Zwraca połączenie do bazy danych i włącza obsługę kluczy obcych.
    """
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_table_utworzone_konta(conn: sqlite3.Connection) -> None:
    """
    Tworzy tabelę kont użytkowników, jeżeli nie istnieje.
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


def create_table_zgloszenia(conn: sqlite3.Connection) -> None:
    """
    Tworzy tabelę bieżących zgłoszeń, jeżeli nie istnieje.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS zgloszenia (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        data_godzina     TEXT NOT NULL DEFAULT (datetime('now')),
        imie             TEXT NOT NULL,
        nazwisko         TEXT NOT NULL,
        login            TEXT,
        tel              TEXT NOT NULL,
        termin           TEXT NOT NULL,
        w_jakiej_sprawie TEXT NOT NULL,
        FOREIGN KEY (login) REFERENCES utworzone_konta(login)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    );
    """
    conn.execute(sql)


def create_table_zgloszenia_archiwum(conn: sqlite3.Connection) -> None:
    """
    Tworzy tabelę archiwum zgłoszeń, jeżeli nie istnieje.
    """
    sql = """
    CREATE TABLE IF NOT EXISTS zgloszenia_archiwum (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        data_godzina     TEXT NOT NULL,
        imie             TEXT NOT NULL,
        nazwisko         TEXT NOT NULL,
        login            TEXT,
        tel              TEXT NOT NULL,
        termin           TEXT NOT NULL,
        w_jakiej_sprawie TEXT NOT NULL,
        archived_at      TEXT NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (login) REFERENCES utworzone_konta(login)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    );
    """
    conn.execute(sql)


def ensure_admin_account(conn: sqlite3.Connection) -> None:
    """
    Tworzy konto admin:admin, jeżeli jeszcze nie istnieje.
    """
    conn.execute(
        """
        INSERT OR IGNORE INTO utworzone_konta (login, haslo_hash, uprawnienie)
        VALUES ('admin', ?, 'admin');
        """,
        (generate_password_hash("admin"),),
    )


def init_db(db_path: Optional[str] = None) -> None:
    """
    Tworzy plik bazy (jeżeli nie istnieje), tabele i domyślne konto admina.
    """
    path = db_path or DB_PATH
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection(path)
    try:
        create_table_utworzone_konta(conn)
        create_table_zgloszenia(conn)
        create_table_zgloszenia_archiwum(conn)
        ensure_admin_account(conn)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Baza zainicjalizowana: {DB_PATH}")
