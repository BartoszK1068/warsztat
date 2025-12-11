"""
Operacje bazodanowe dla warsztatu.
"""

import sqlite3
from typing import Optional, List, Dict
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


def add_zgloszenie(
    imie: str,
    nazwisko: str,
    tel: str,
    termin: str,
    w_jakiej_sprawie: str,
    login: Optional[str] = None,) -> str:
    """
    Dodaje zgłoszenie do tabeli zgloszenia. Zwraca komunikat.
    """
    if not all([imie, nazwisko, tel, termin, w_jakiej_sprawie]):
        return "Uzupełnij wszystkie pola."

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO zgloszenia (imie, nazwisko, login, tel, termin, w_jakiej_sprawie)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (imie, nazwisko, login, tel, termin, w_jakiej_sprawie),
        )
        conn.commit()
        return "Zgłoszenie przyjęte."
    except Exception as e:
        return f"Błąd przy zapisie zgłoszenia: {e}"
    finally:
        conn.close()


def get_user_role(login: str) -> Optional[str]:
    """
    Zwraca rolę użytkownika lub None.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT uprawnienie FROM utworzone_konta WHERE login = ?",
            (login,),
        ).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def list_zgloszenia() -> List[Dict[str, str]]:
    """
    Zwraca listę zgłoszeń jako listę słowników.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, data_godzina, imie, nazwisko, login, tel, termin, w_jakiej_sprawie
            FROM zgloszenia
            ORDER BY datetime(data_godzina) DESC;
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def list_zgloszenia_archiwum() -> List[Dict[str, str]]:
    """
    Zwraca listę zgłoszeń w archiwum.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT id, data_godzina, imie, nazwisko, login, tel, termin, w_jakiej_sprawie, archived_at
            FROM zgloszenia_archiwum
            ORDER BY datetime(archived_at) DESC;
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def delete_zgloszenie(zgloszenie_id: int) -> str:
    """
    Usuwa zgłoszenie po id.
    """
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM zgloszenia WHERE id = ?",
            (zgloszenie_id,),
        )
        conn.commit()
        if cur.rowcount == 0:
            return "Zgłoszenie nie istnieje."
        return "Zgłoszenie usunięte."
    except Exception as e:
        return f"Błąd przy usuwaniu: {e}"
    finally:
        conn.close()


def delete_zgloszenie_archiwum(zgloszenie_id: int) -> str:
    """
    Usuwa zgłoszenie z archiwum po id.
    """
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM zgloszenia_archiwum WHERE id = ?",
            (zgloszenie_id,),
        )
        conn.commit()
        if cur.rowcount == 0:
            return "Zgłoszenie w archiwum nie istnieje."
        return "Zgłoszenie usunięte z archiwum."
    except Exception as e:
        return f"Błąd przy usuwaniu z archiwum: {e}"
    finally:
        conn.close()

def archive_zgloszenie(zgloszenie_id: int) -> str:
    """
    Przenosi zgłoszenie do archiwum.
    """
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT * FROM zgloszenia WHERE id = ?",
            (zgloszenie_id,),
        ).fetchone()
        if not row:
            return "Zgłoszenie nie istnieje."

        conn.execute(
            """
            INSERT INTO zgloszenia_archiwum (data_godzina, imie, nazwisko, login, tel, termin, w_jakiej_sprawie)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["data_godzina"],
                row["imie"],
                row["nazwisko"],
                row["login"],
                row["tel"],
                row["termin"],
                row["w_jakiej_sprawie"],
            ),
        )
        conn.execute("DELETE FROM zgloszenia WHERE id = ?", (zgloszenie_id,))
        conn.commit()
        return "Przeniesiono do archiwum."
    except Exception as e:
        return f"Błąd przy archiwizacji: {e}"
    finally:
        conn.close()


def delete_zgloszenie(zgloszenie_id: int) -> str:
    """
    Usuwa zgłoszenie po id.
    """
    conn = get_connection()
    try:
        cur = conn.execute(
            "DELETE FROM zgloszenia WHERE id = ?",
            (zgloszenie_id,),
        )
        conn.commit()
        if cur.rowcount == 0:
            return "Zgłoszenie nie istnieje."
        return "Zgłoszenie usunięte."
    except Exception as e:
        return f"Błąd przy usuwaniu: {e}"
    finally:
        conn.close()
