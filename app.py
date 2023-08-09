# Импортируем класс Flask из модуля flask.
from flask import Flask
# Импортируем модуль render_template для работы шаблонов.
from flask import render_template
# Импортируем модуль request получения запросов.
from flask import request

from werkzeug.utils import secure_filename
# Импортируем модуль SQLAlchemy для работы с базой данных.
from flask_sqlalchemy import SQLAlchemy
# Импортируем модуль redirect для перенаправления на другую страницу.
from flask import redirect

# Создаем основной объект app класса Flask.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
# Создание бд.
db = SQLAlchemy(app)


# Создадим класс, на основе которого, будет создаваться таблица.
class Article(db.Model):
    # Добавим поле id, уникальное.
    id = db.Column(db.Integer, primary_key=True)
    # Добавим поле image, не может быть пустым.
    image = db.Column(db.Text, nullable=False)

    # Получение данных объекта базы данных в виде строки.
    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    # Возвращаем на страницу текст.
    return render_template("index.html")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        file = request.files['file']

        file.save(f"static/uploadimages/{secure_filename(file.filename)}")
        # Сохраняем объект класса Article с данными из переменных, записанных в нужные поля.
        article = Article(image=file.filename)
        print(article)
        # Попробуем добавить значения в базу данных.
        try:
            # Добавление объекта класса Article в сессию.
            db.session.add(article)
            # Сохранение в базе данных.
            db.session.commit()
            # Возвращение на страницу со всеми статьями.
            return render_template("watch_articles.html")
        # Исключение.
        except:
            # Возвращаем ошибку: "Не удалось добавить статью".
            return "Не удалось добавить статью."
    else:
        return render_template("index.html")


# Декоратор, который регистрирует URL-адрес.
@app.route('/watch_articles')
# Функция для вывода всех статей.
def watch_articles():
    # Создаем объект, в котором находится данные всех полей класса Article.
    articles = Article.query.order_by(Article.create_on.desc()).all()
    # Возвращаем статьи на страницу.
    return render_template("watch_articles.html", articles=articles)


with app.app_context():
    db.create_all()
    # Проверка правильности запуска проекта через файл с названием app.
if __name__ == '__main__':
    # Запуск приложения и отслеживание ошибок.
    app.run(debug=True)
