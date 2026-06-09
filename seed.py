from app import app
from models import db, Test

with app.app_context():

    if Test.query.count() == 0:

        db.session.add(
            Test(
                title="Математика",
                description="Базовый тест по математике"
            )
        )

        db.session.add(
            Test(
                title="Информатика",
                description="Основы программирования"
            )
        )

        db.session.commit()

        print("Тесты добавлены")

    else:
        print("Тесты уже существуют")