import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_init import get_connection


def login_user(login: str, password: str) -> str:
    """
    Weryfikuje użytkownika i hasło. Zwraca komunikat dla UI.
    """
    if not login or not password:
        return "Podaj login i hasło."

    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT haslo_hash FROM utworzone_konta WHERE login = ?",
            (login,),
        ).fetchone()

        if row is None:
            return "Nie znaleziono konta."
        if not check_password_hash(row[0], password):
            return "Błędne hasło."
        return "Zalogowano pomyślnie."
    finally:
        conn.close()


def register_user(login: str, password: str, uprawnienie: str = "klient") -> str:
    """
    Dodaje nowego użytkownika. Zwraca komunikat dla UI.
    """
    if not login or not password:
        return "Podaj login i hasło."
    if uprawnienie not in ("admin", "pracownik", "klient"):
        return "Nieprawidłowe uprawnienie."

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO utworzone_konta (login, haslo_hash, uprawnienie) VALUES (?, ?, ?)",
            (login, generate_password_hash(password), uprawnienie),
        )
        conn.commit()
        return "Konto utworzone. Możesz się zalogować."
    except sqlite3.IntegrityError:
        return "Taki login już istnieje."
    finally:
        conn.close()