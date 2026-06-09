from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Регистрация успешна")

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        print("EMAIL:", email)
        print("USER:", user)

        if user:
            print("HASH:", user.password)
            print("CHECK:", check_password_hash(
                user.password,
                password
            ))

        user = User.query.filter_by(email=email).first()

        print("EMAIL:", email)
        print("USER FOUND:", user)

        if user:
            print("PASSWORD CHECK:", check_password_hash(user.password, password))

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        print("LOGIN FAILED")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for("home")
    )

from models import Test, Result

@app.route("/tests")
@login_required
def tests():

    tests = Test.query.all()

    return render_template(
        "tests.html",
        tests=tests
    )


@app.route("/take_test/<int:test_id>", methods=["GET", "POST"])
@login_required
def take_test(test_id):

    test = Test.query.get_or_404(test_id)

    questions = {
        1: [
            "Что выводит print(type([]))?",
            "Какая структура данных изменяемая?",
            "Для чего используется def?",
            "Что делает цикл for?",
            "Что такое list?",
            "Что возвращает input()?",
            "Для чего нужен try/except?",
            "Как получить длину списка?",
            "Что такое dict?",
            "Что такое модуль?"
        ],
        2: [
            "Для чего нужен тег <head>?",
            "Как создать ссылку?",
            "Как вставить изображение?",
            "Для чего нужен <div>?",
            "Что такое HTML?",
            "Как создать форму?",
            "Для чего нужен <input>?",
            "Что делает тег <table>?",
            "Что такое атрибут class?",
            "Что такое CSS?"
        ],
        3: [
            "Что делает SELECT?",
            "Для чего нужен WHERE?",
            "Что такое PRIMARY KEY?",
            "Что делает INSERT?",
            "Что делает UPDATE?",
            "Что делает DELETE?",
            "Для чего нужен JOIN?",
            "Что такое база данных?",
            "Что делает ORDER BY?",
            "Что такое SQL?"
        ]
    }

    if request.method == "POST":

        score = 0

        for i in range(10):
            answer = request.form.get(f"q{i}")

            if answer:
                score += 10

        result = Result(
            user_id=current_user.id,
            score=score
        )

        db.session.add(result)
        db.session.commit()

        return redirect(url_for("results"))

    return render_template(
        "take_test.html",
        test=test,
        questions=questions.get(test_id, [])
    )


@app.route("/results")
@login_required
def results():

    results = Result.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "results.html",
        results=results
    )

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        if Test.query.count() == 0:

            db.session.add(
                Test(
                    title="Математика",
                    description="Базовые математические вопросы"
                )
            )

            db.session.add(
                Test(
                    title="Информатика",
                    description="Основы программирования"
                )
            )

            db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)