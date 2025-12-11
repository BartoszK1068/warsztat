from flask import Flask, render_template, request, session, redirect, url_for
from data import db_ops
from data.db_init import init_db
import emailing

app = Flask(__name__, template_folder="pages", static_folder="pages")
app.secret_key = "change-me"  # replace for production

# Ensure DB schema exists
init_db()


@app.context_processor
def inject_user_role():
    user = session.get("user")
    role = db_ops.get_user_role(user) if user else None
    return {"current_user": user, "current_role": role}


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    user = session.get("user")

    if request.method == "POST":
        login_value = (request.form.get("login") or "").strip()
        password = request.form.get("password") or ""
        message = db_ops.login_user(login_value, password)
        if message == "Zalogowano pomyślnie.":
            session["user"] = login_value
            user = login_value
    elif user:
        message = f"Jesteś zalogowany jako {user}."

    return render_template("login.html", message=message)


@app.route("/register", methods=["POST"])
def register():
    login_value = (request.form.get("login") or "").strip()
    password = request.form.get("password") or ""
    message = db_ops.register_user(login_value, password)
    return render_template("login.html", message=message)


@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return render_template("login.html", message="Wylogowano.")


@app.route("/zgloszenia", methods=["GET", "POST"])
def zgloszenia():
    user = session.get("user")
    message = None
    if request.method == "POST":
        imie = (request.form.get("imie") or "").strip()
        nazwisko = (request.form.get("nazwisko") or "").strip()
        tel = (request.form.get("tel") or "").strip()
        termin = request.form.get("termin") or ""
        opis = (request.form.get("w_jakiej_sprawie") or "").strip()

        if not user:
            message = "Zaloguj się, aby złożyć zgłoszenie."
        else:
            message = db_ops.add_zgloszenie(
                imie=imie,
                nazwisko=nazwisko,
                tel=tel,
                termin=termin,
                w_jakiej_sprawie=opis,
                login=user,
            )
            if message == "Zgłoszenie przyjęte.":
                try:
                    emailing.send_zgloszenie(
                        imie=imie,
                        nazwisko=nazwisko,
                        tel=tel,
                        termin=termin,
                        opis=opis,
                        login=user,
                    )
                except Exception as e:
                    message = f"{message} (Błąd wysyłki e-mail: {e})"

    return render_template("zgloszenia.html", user=user, message=message)


def render_admin(message: str | None):
    zgloszenia = db_ops.list_zgloszenia()
    zgloszenia_arch = db_ops.list_zgloszenia_archiwum()
    return render_template(
        "admin_zgloszenia.html",
        message=message,
        zgloszenia=zgloszenia,
        zgloszenia_arch=zgloszenia_arch,
    )


@app.route("/admin/zgloszenia")
def admin_zgloszenia():
    user = session.get("user")
    role = db_ops.get_user_role(user) if user else None
    flash_msg = session.pop("admin_msg", None)
    if not user or role != "admin":
        return render_admin("Brak uprawnień (wymagany admin).")
    return render_admin(flash_msg)


@app.route("/admin/zgloszenia/usun", methods=["POST"])
def admin_usun_zgloszenie():
    user = session.get("user")
    role = db_ops.get_user_role(user) if user else None
    if not user or role != "admin":
        return render_admin("Brak uprawnień (wymagany admin).")

    zgloszenie_id = request.form.get("zgloszenie_id")
    try:
        zgloszenie_id_int = int(zgloszenie_id)
    except (TypeError, ValueError):
        msg = "Niepoprawne ID zgłoszenia."
    else:
        msg = db_ops.delete_zgloszenie(zgloszenie_id_int)

    session["admin_msg"] = msg
    return redirect(url_for("admin_zgloszenia"))


@app.route("/admin/zgloszenia/usun_archiwum", methods=["POST"])
def admin_usun_zgloszenie_archiwum():
    user = session.get("user")
    role = db_ops.get_user_role(user) if user else None
    if not user or role != "admin":
        return render_admin("Brak uprawnień (wymagany admin).")

    zgloszenie_id = request.form.get("zgloszenie_id")
    try:
        zgloszenie_id_int = int(zgloszenie_id)
    except (TypeError, ValueError):
        msg = "Niepoprawne ID zgłoszenia."
    else:
        msg = db_ops.delete_zgloszenie_archiwum(zgloszenie_id_int)

    session["admin_msg"] = msg
    return redirect(url_for("admin_zgloszenia"))


@app.route("/admin/zgloszenia/archiwum", methods=["POST"])
def admin_archiwizuj_zgloszenie():
    user = session.get("user")
    role = db_ops.get_user_role(user) if user else None
    if not user or role != "admin":
        return render_admin("Brak uprawnień (wymagany admin).")

    zgloszenie_id = request.form.get("zgloszenie_id")
    try:
        zgloszenie_id_int = int(zgloszenie_id)
    except (TypeError, ValueError):
        msg = "Niepoprawne ID zgłoszenia."
    else:
        msg = db_ops.archive_zgloszenie(zgloszenie_id_int)

    session["admin_msg"] = msg
    return redirect(url_for("admin_zgloszenia"))


if __name__ == "__main__":
    app.run(debug=True)
