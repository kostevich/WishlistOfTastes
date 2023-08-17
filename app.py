# Импортируем класс Flask из модуля flask.
from flask import Flask
# Импортируем модуль render_template для работы шаблонов.
from flask import render_template
# Импортируем модуль request получения запросов.
from flask import request
# Импортируем secure_filename для работы с надежной версией файла.
from werkzeug.utils import secure_filename
# Импортируем модуль SQLAlchemy для работы с базой данных.
from flask_sqlalchemy import SQLAlchemy
# Импортируем модуль redirect для перенаправления на другую страницу.
from flask import redirect
# Импортируем модуль datetime для работы с полем дата базы данных.
from datetime import datetime

# Создаем основной объект app класса Flask.
app = Flask(__name__)
# Задание настроек бд.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
# Создание бд.
db = SQLAlchemy(app)


# Создадим класс, на основе которого, будет создаваться бд.
class Article(db.Model):
    # Добавим поле id, уникальное.
    id = db.Column(db.Integer, primary_key=True)
    # Добавим поле tag, может быть пустым.
    tag = db.Column(db.String(20), nullable=True)
    # Добавим поле название, не может быть пустым.
    title = db.Column(db.String(50), nullable=False)
    # Добавим поле оценки, не может быть пустым.
    value = db.Column(db.String(200), nullable=True)
    # Добавим поле комментарий к оценке, не может быть пустым.
    comment = db.Column(db.Text, nullable=True)
    # Добавим поле пробы, не может быть пустым.
    check = db.Column(db.Text, nullable=False)
    # Добавим поле картинки, может быть пустым.
    image = db.Column(db.Text, nullable=True)
    # Добавим поле время создания, значение по умолчанию время сейчас.
    create_on = db.Column(db.DateTime, default=datetime.utcnow)
    # Добавим поле время изменения, значение по умолчанию время сейчас, и оно обновляется при обновлении информации в базе данных.
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Получение данных объекта базы данных в виде строки.
    def __repr__(self):
        # Возвращаем класс Article в текстовом виде.
        return '<Article %r>' % self.id

# Обработка пути по ссылке.
@app.route('/')
# Функция отображения содержимого страницы при переходе по ссылке.
def mainpageview():
    # Возвращаем на страницу текст.
    return render_template("mainpage.html")

# ↑.
@app.route('/about')
# ↑.
def about():
    # ↑.
    return render_template("about.html")

# ↑.
@app.route('/watch_articles/<int:id>')
# Функция для детального просмотра статьи по id.
def watch_detailarticles(id):
    # Сохраняем объект, в котором находится данные выбранной статьи.
    article = Article.query.get(id)
    # ↑ и передаем данные объекта.
    return render_template("watch_detailarticles.html", article=article)

# ↑.
@app.route('/watch_articles/<int:id>/delete')
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
        return redirect('/watch_articles')
    # Исключение.
    except:
        # Возвращаем ошибку в виде текста на страницу.
        return "Не удалось удалить статью."
    # Возвращаем статьи на страницу, если удаление прошло успешно.
    return render_template("watch_articles.html", article=article)

# ↑, работа с методами GET, POST.
@app.route('/watch_articles/<int:id>/edit', methods=['GET', 'POST'])
# Функция для редактирования статьи по id.
def post_update(id):
    # Если пришел запрос с методом POST.
    if request.method == 'POST':
        # Сохраняем объект, в котором находится данные выбранной статьи.
        article = Article.query.get(id)
        # Сохраняем в поле tag объекта article значение из поля формы tag.
        article.tag = request.form['tag']
        # Сохраняем в поле title объекта article значение из поля формы title.
        article.title = request.form['title']
        # Сохраняем в поле value объекта article значение из поля формы value.
        article.value = request.form['value']
        # Сохраняем в поле comment объекта article значение из поля формы comment.
        article.comment = request.form['comment']
        # Сохраняем в поле check объекта article значение из поля формы check.
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
            file.save(f"static/uploadimages/{secure_filename(file.filename)}")
        # Попробуем изменить значение в бд.
        try:
            # Добавление объекта класса Article в сессию.
            db.session.add(article)
            # Изменение полей объекта в бд.
            db.session.commit()
            # Перенаправление на страницу со всеми статьями.
            return redirect('/watch_articles')
        # Исключение.
        except:
            # Возвращаем ошибку в виде текста на страницу.
            return "Не удалось изменить статью."
        # Возвращаем статьи на страницу, если удаление прошло успешно.
        return render_template("watch_articles.html", article=article)
    # Если не пришел POST-запрос.
    else:
        # Сохраняем объект, в котором находится данные выбранной статьи.
        article = Article.query.get(id)
         # Возвращаем страницу с данными выбранной статьи.
        return render_template("edit_articles.html", article=article)
    
# ↑.
@app.route('/create_articles', methods=['GET', 'POST'])
# Функция для создания статей.
def create_articles():
    # Если пришел запрос с методом POST.
    if request.method == 'POST':
        # Сохраняем в переменную tag значение из поля формы tag.
        tag = request.form['tag']
        # Сохраняем в переменную title значение из поля формы title.
        title = request.form['title']
        # Сохраняем в переменную value значение из поля формы value.
        value = request.form['value']
        # Сохраняем в переменную comment значение из поля формы comment.
        comment = request.form['comment']
        # Сохраняем в переменную check значение из поля формы check.
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
            return redirect('/watch_articles')
        # Исключение.
        except:
            # Возвращаем ошибку: "Не удалось добавить статью".
            return "Не удалось добавить статью."
    # Если не пришел POST-запрос.
    else:
        # Возвращаем страницу с созданием статьи.
        return render_template("index.html")

# ↑.
@app.route('/watch_articles')
# Функция для вывода всех статей.
def watch_articles():
    # Создаем объект, в котором находится данные всех полей класса Article, сортированные от более поздних к ранним.
    articles = Article.query.order_by(Article.create_on.desc()).all()
    # Возвращаем страницу со всеми статьями на страницу.
    return render_template("watch_articles.html", articles=articles)

# Создание контекста приложения.
with app.app_context():
    # Создание бд.
    db.create_all()
    # Проверка правильности запуска проекта через файл с названием app.
if __name__ == '__main__':
    # Запуск приложения и отслеживание ошибок.
    app.run(debug=True)
