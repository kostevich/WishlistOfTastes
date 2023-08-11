# Импортируем класс Flask из модуля flask.
from flask import Flask
# Импортируем модуль render_template для работы шаблонов.
from flask import render_template
# Импортируем модуль request получения запросов.
from flask import request
# Испортируем
from werkzeug.utils import secure_filename
# Импортируем модуль SQLAlchemy для работы с базой данных.
from flask_sqlalchemy import SQLAlchemy
# Импортируем модуль redirect для перенаправления на другую страницу.
from flask import redirect
# Импортируем модуль datetime для работы с полем дата базы данных.
from datetime import datetime

# Создаем основной объект app класса Flask.
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
# Создание бд.
db = SQLAlchemy(app)


# Создадим класс, на основе которого, будет создаваться таблица.
class Article(db.Model):
    # Добавим поле id, уникальное.
    id = db.Column(db.Integer, primary_key=True)
    # Добавим поле tag, не может быть пустым.
    tag = db.Column(db.String(20), nullable=True)
    # Добавим поле название, не может быть пустым.
    title = db.Column(db.String(50), nullable=False)
    # Добавим поле оценки, не может быть пустым.
    value = db.Column(db.String(200), nullable=True)
    # Добавим поле комментарий к оценке, не может быть пустым.
    comment = db.Column(db.Text, nullable=True)

    check = db.Column(db.Text, nullable=False)

    image = db.Column(db.Text, nullable=True)
    # Добавим поле время создания, значение по умолчанию время сейчас.
    create_on = db.Column(db.DateTime, default=datetime.utcnow)
    # Добавим поле время изменения, значение по умолчанию время сейчас, и оно обновляется при обновлении информации в базе данных.
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Получение данных объекта базы данных в виде строки.
    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    # Возвращаем на страницу текст.
    return render_template("mainpage.html")

@app.route('/about')
def about():
    # Возвращаем на страницу текст.
    return render_template("about.html")


@app.route('/create_articles', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Сохраняем в переменную text значение из поля формы text.
        tag = request.form['tag']
        # Сохраняем в переменную title значение из поля формы title.
        title = request.form['title']
        # Сохраняем в переменную intro значение из поля формы intro.
        value = request.form['value']
        # Сохраняем в переменную text значение из поля формы text.
        comment = request.form['comment']
        check = request.form['check']
        file = request.files['file']

        file.save(f"static/uploadimages/{secure_filename(file.filename)}")
        # Сохраняем объект класса Article с данными из переменных, записанных в нужные поля.
        article = Article(title=title, tag=tag, value=value, comment=comment, image=file.filename, check=check)
        # Попробуем добавить значения в базу данных.
        try:
            # Добавление объекта класса Article в сессию.
            db.session.add(article)
            # Сохранение в базе данных.
            db.session.commit()
            # Возвращение на страницу со всеми статьями.
            return redirect('/watch_articles')
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
    print(articles)
    # Возвращаем статьи на страницу.
    return render_template("watch_articles.html", articles=articles)


with app.app_context():
    db.create_all()
    # Проверка правильности запуска проекта через файл с названием app.
if __name__ == '__main__':
    # Запуск приложения и отслеживание ошибок.
    app.run(debug=True)
