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
        {
            "question": "Найдите значение выражения: 2² + 3²",
            "options": ["10", "12", "13", "15"],
            "correct": "13"
        },
        {
            "question": "Решите уравнение: x + 7 = 15",
            "options": ["6", "7", "8", "9"],
            "correct": "8"
        },
        {
            "question": "Чему равен корень из 144?",
            "options": ["10", "11", "12", "13"],
            "correct": "12"
        },
        {
            "question": "Сколько процентов составляет 50 от 200?",
            "options": ["20%", "25%", "30%", "40%"],
            "correct": "25%"
        },
        {
            "question": "Найдите площадь прямоугольника со сторонами 5 и 8.",
            "options": ["13", "26", "40", "80"],
            "correct": "40"
        },
        {
            "question": "Чему равен синус 30°?",
            "options": ["0", "0.5", "1", "2"],
            "correct": "0.5"
        },
        {
            "question": "Решите: 3x = 21",
            "options": ["5", "6", "7", "8"],
            "correct": "7"
        },
        {
            "question": "Найдите среднее арифметическое чисел 4, 6 и 8.",
            "options": ["5", "6", "7", "8"],
            "correct": "6"
        },
        {
            "question": "Чему равен cos(0°)?",
            "options": ["0", "0.5", "1", "-1"],
            "correct": "1"
        },
        {
            "question": "Сколько будет 15 × 6?",
            "options": ["75", "80", "90", "95"],
            "correct": "90"
        }
    ],

    2: [
        {
            "question": "Как вывести текст на экран в Python?",
            "options": ["echo()", "print()", "show()", "output()"],
            "correct": "print()"
        },
        {
            "question": "Как называется переменная в Python?",
            "options": ["name = 'Tom'", "var Tom", "string Tom", "Tom := name"],
            "correct": "name = 'Tom'"
        },
        {
            "question": "Как получить ввод пользователя?",
            "options": ["scan()", "input()", "read()", "enter()"],
            "correct": "input()"
        },
        {
            "question": "Какой тип данных хранит текст?",
            "options": ["int", "bool", "str", "list"],
            "correct": "str"
        },
        {
            "question": "Какой тип данных хранит целые числа?",
            "options": ["str", "int", "float", "list"],
            "correct": "int"
        },
        {
            "question": "Как создать список?",
            "options": ["{}", "()", "[]", "<>"],
            "correct": "[]"
        },
        {
            "question": "Какой цикл используется для перебора элементов?",
            "options": ["while", "for", "repeat", "loop"],
            "correct": "for"
        },
        {
            "question": "Как обозначается комментарий?",
            "options": ["//", "#", "/*", "--"],
            "correct": "#"
        },
        {
            "question": "Что вернёт len([1,2,3])?",
            "options": ["2", "3", "4", "Ошибка"],
            "correct": "3"
        },
        {
            "question": "Для чего используется if?",
            "options": [
                "Для импорта",
                "Для условия",
                "Для списка",
                "Для функции"
            ],
            "correct": "Для условия"
        }
    ]
}

    if request.method == "POST":

        score = 0

        current_questions = questions.get(test_id, [])

        for i, q in enumerate(current_questions):

            answer = request.form.get(f"q{i}")
            print("QUESTION", i)
            print("USER ANSWER =", answer)
            print("CORRECT =", q["correct"])

            if answer == q["correct"]:
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
@app.route("/test/python", methods=["GET", "POST"])
@login_required
def python_test():

    questions = [
        {
            "question": "Как вывести текст в Python?",
            "options": ["print()", "echo()", "show()", "write()"],
            "correct": "print()"
        },
        {
            "question": "Какой тип данных хранит текст?",
            "options": ["int", "str", "bool", "list"],
            "correct": "str"
        },
        {
            "question": "Как создать список?",
            "options": ["{}", "[]", "()", "<>"],
            "correct": "[]"
        }
    ]

    if request.method == "POST":

        score = 0

        for i, q in enumerate(questions):

            answer = request.form.get(f"q{i}")

            if answer == q["correct"]:
                score += 100 // len(questions)

        result = Result(
            user_id=current_user.id,
            score=score
        )

        db.session.add(result)
        db.session.commit()

        return redirect(url_for("results"))

    return render_template(
        "subject_test.html",
        title="Тест по Python",
        questions=questions
    )

@app.route("/test/html", methods=["GET", "POST"])
@login_required
def html_test():

    questions = [
        {
            "question": "Какой тег создаёт ссылку?",
            "options": ["<a>", "<link>", "<href>", "<url>"],
            "correct": "<a>"
        },
        {
            "question": "Как вставить изображение?",
            "options": ["<img>", "<image>", "<pic>", "<src>"],
            "correct": "<img>"
        }
    ]

    if request.method == "POST":

        score = 0

        for i, q in enumerate(questions):
            answer = request.form.get(f"q{i}")

            if answer == q["correct"]:
                score += 100 // len(questions)

        result = Result(
            user_id=current_user.id,
            score=score
        )

        db.session.add(result)
        db.session.commit()

        return redirect(url_for("results"))

    return render_template(
        "subject_test.html",
        title="Тест по HTML & CSS",
        questions=questions
    )
@app.route("/test/sql", methods=["GET", "POST"])
@login_required
def sql_test():

    questions = [
        {
            "question": "Что делает SELECT?",
            "options": [
                "Удаляет данные",
                "Выбирает данные",
                "Изменяет данные",
                "Создаёт таблицу"
            ],
            "correct": "Выбирает данные"
        },
        {
            "question": "Для чего нужен WHERE?",
            "options": [
                "Фильтрация",
                "Сортировка",
                "Удаление",
                "Создание"
            ],
            "correct": "Фильтрация"
        }
    ]

    if request.method == "POST":

        score = 0

        for i, q in enumerate(questions):
            answer = request.form.get(f"q{i}")

            if answer == q["correct"]:
                score += 100 // len(questions)

        result = Result(
            user_id=current_user.id,
            score=score
        )

        db.session.add(result)
        db.session.commit()

        return redirect(url_for("results"))

    return render_template(
        "subject_test.html",
        title="Тест по SQL",
        questions=questions
    )
if __name__ == "__main__":
    app.run(debug=True)