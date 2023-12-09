#!/usr/bin/env python

#==========================================================================================#
# >>>>> ПОДКЛЮЧЕНИЕ БИБЛИОТЕК И МОДУЛЕЙ <<<<< #
#==========================================================================================#

from datetime import datetime
from dublib.Methods import CheckPythonMinimalVersion
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

#==========================================================================================#
# >>>>> ЧТЕНИЕ НАСТРОЕК <<<<< #
#==========================================================================================#

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 11)

# Создаем основной объект класса Flask.
app = Flask(__name__)

# Задание настроек бд.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Food.db'

# Создание бд.
db = SQLAlchemy(app)

# Создание всех данных приложения.
with app.app_context():
     db.create_all()

#==========================================================================================#
# >>>>> СОЗДАНИЕ ПОЛЕЙ ТАБЛИЦЫ СТАТЕЙ <<<<< #
#==========================================================================================#   

# Создадим класс, на основе которого, будет создаваться поля таблицы.
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20), nullable=True)
    title = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    check = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text, nullable=True)
    create_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Получение данных объекта базы данных в виде строки.
    def __repr__(self):
        # Возвращаем класс Article в текстовом виде.
        return '<Article %r>' % self.id

#==========================================================================================#
# >>>>> ГЛАВНАЯ СТРАНИЦА САЙТА <<<<< #
#==========================================================================================#

# Обработка пути по ссылке.
@app.route('/')
# Функция отображения содержимого страницы при переходе по ссылке.
def mainpageview():
    # Возвращаем на страницу текст.
    return render_template("MainPage.html")

#==========================================================================================#
# >>>>> СТРАНИЦА СОЗДАТЕЛЯ САЙТА <<<<< #
#==========================================================================================#

# ↑.
@app.route('/About')
# ↑.
def about():
    # ↑.
    return render_template("About.html")

#==========================================================================================#
# >>>>> ДЕТАЛЬНЫЙ ПРОСМОТР БЛЮДА <<<<< #
#==========================================================================================#

# ↑.
@app.route('/WatchArticles/<int:id>')
# Функция для детального просмотра статьи по id.
def watch_detailarticles(id):
    # Сохраняем объект, в котором находится данные выбранной статьи.
    article = Article.query.get(id)
    # ↑ и передаем данные объекта.
    return render_template("WatchDetailarticles.html", article=article)

#==========================================================================================#
# >>>>> УДАЛЕНИЕ БЛЮДА <<<<< #
#==========================================================================================#

# ↑.
@app.route('/WatchArticles/<int:id>/delete')
# Функция для удаления статьи по id.
def delete_detailarticles(id):
    # Сохраняем  объект, который надо удалить.
    article = Article.query.get(id)
    # Попробуем удалить из бд.
    try:
        # Добавление объекта класса Article в сессию.
        db.session.delete(article)
        # Удаление статьи в базе данных.
        db.session.commit()
        # Перенаправление на страницу со всеми статьями.
        return redirect('/WatchArticles')
    # Исключение.
    except:
        # Возвращаем ошибку в виде текста на страницу.
        return "Не удалось удалить статью."
    # Возвращаем статьи на страницу, если удаление прошло успешно.
    return render_template("WatchArticles.html", article=article)

#==========================================================================================#
# >>>>> РЕДАКТИРОВАНИЕ БЛЮДА <<<<< #
#==========================================================================================#

# ↑, работа с методами GET, POST.
@app.route('/WatchArticles/<int:id>/edit', methods=['GET', 'POST'])
# Функция для редактирования статьи по id.
def post_update(id):
    # Если пришел запрос с методом POST.
    if request.method == 'POST':
        # Сохраняем объект, в котором находится данные выбранной статьи.
        article = Article.query.get(id)

        # Сохраняем в переменную значение из поля формы.
        article.tag = request.form['tag']
        article.title = request.form['title']
        article.value = request.form['value']
        article.comment = request.form['comment']
        article.check = request.form['check']
        
        # Сохраняем в переменную file файл из поля формы file.
        file = request.files['file']

        # Если название файла пустое или название файла соответствует полю выбранного объекта бд.
        if file.filename == '' or file.filename == article.image:
            # Вывод текста.
            print('None or similar')

        # Иначе:
        else:
            # Сохраняем в поле image объекта article название файла.
            article.image = file.filename

            # Сохраняем файл.
            file.save(f"static/UploadImages/{secure_filename(file.filename)}")

        # Попробуем изменить значение в бд.
        try:
            # Добавление объекта класса Article в сессию.
            db.session.add(article)

            # Изменение полей объекта в бд.
            db.session.commit()

            # Перенаправление на страницу со всеми статьями.
            return redirect('/WatchArticles')
        
        # Исключение.
        except:
            # Возвращаем ошибку в виде текста на страницу.
            return "Не удалось изменить статью."
        
        # Возвращаем статьи на страницу, если удаление прошло успешно.
        return render_template("WatchArticles.html", article=article)
    # Если не пришел POST-запрос.
    else:
        # Сохраняем объект, в котором находится данные выбранной статьи.
        article = Article.query.get(id)

        # Возвращаем страницу с данными выбранной статьи.
        return render_template("EditArticles.html", article=article)
    
#==========================================================================================#
# >>>>> СОЗДАНИЕ НОВОГО БЛЮДА <<<<< #
#==========================================================================================#
    
# ↑.
@app.route('/CreateArticles', methods=['GET', 'POST'])
# Функция для создания статей.
def create_articles():
    # Если пришел запрос с методом POST.
    if request.method == 'POST':
        # Сохраняем в переменную значение из поля формы.
        tag = request.form['tag']
        title = request.form['title']
        value = request.form['value']
        comment = request.form['comment']
        check = request.form['check']

        # Сохраняем в переменную file изображение из поля формы file.
        file = request.files['file']

        # Сохраняем изображение в папку с именем.
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
            return redirect('/WatchArticles')
        
        # Исключение.
        except:
            # Возвращаем ошибку: "Не удалось добавить статью".
            return "Не удалось добавить статью."
    # Если не пришел POST-запрос.
    else:
        # Возвращаем страницу с созданием статьи.
        return render_template("Index.html")

#==========================================================================================#
# >>>>> ПРОСМОТР ВСЕХ ДОБАВЛЕННЫХ БЛЮД <<<<< #
#==========================================================================================#

# ↑.
@app.route('/WatchArticles')
# Функция для вывода всех статей.
def watch_articles():
    # Создаем объект, в котором находится данные всех полей класса Article, сортированные от более поздних к ранним.
    articles = Article.query.order_by(Article.create_on.desc()).all()
    # Возвращаем страницу со всеми статьями на страницу.
    return render_template("WatchArticles.html", articles=articles)

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СКРИПТА <<<<< #
#==========================================================================================#

# Проверка правильности запуска проекта через файл с названием app.
if __name__ == '__main__':
    # Запуск приложения и отслеживание ошибок.
    app.run(debug=True)
