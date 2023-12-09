# WishlistOfTastes
**WishlistOfTastes** – учебный проект на [Flask](https://github.com/pallets/flask?ysclid=lpxvt6k9hy682670415), представляющий собой индивидуальный список новых блюд, которые хочется попробовать. Список можно дополнять, удалять, оценивать, добавлять изображения, комментарии. Есть и другие возможности.

# Порядок установки и использования
1. Загрузить репозиторий. Распаковать.
2. Установить [Python](https://www.python.org/downloads/) версии не старше 3.11. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [dublib](https://github.com/DUB1401/dublib), [flask](https://github.com/pallets/flask?ysclid=lpxvt6k9hy682670415), [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/latest/).
```
pip install flask
pip install flask-sqlalchemy
pip install git+https://github.com/DUB1401/dublib
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r requirements.txt
```
4. В среде исполнения запустить файл _app.py_ командой:
```
 flask run
```
5. Перейти по ссылке (пример: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)).

# Отслеживание в базе данных.

Откройте файл Food.db в программе для открытия баз данных (пример: [SQLiteStudio](https://sqlitestudio.pl/)).

# Пример работы

**Главная страница:**

![image](https://github.com/kostevich/WishlistOfTastes/assets/109979502/7a6d3f85-83a1-425b-a469-db12c0a76e3b)

![image](https://github.com/kostevich/WishlistOfTastes/assets/109979502/dc5dbc60-4b91-45d8-aecb-caddfef1e790)

**Возможный вид ваших списков на сайте:**

![image](https://github.com/kostevich/WishlistOfTastes/assets/109979502/89d53106-dc88-4b40-8c84-b52207729cce)

**Детальный просмотр пункта списка:**

![image](https://github.com/kostevich/WishlistOfTastes/assets/109979502/4133dec0-e5df-4c2f-8b46-4e605484af1d)

**Форма добавления нового блюда:**

![image](https://github.com/kostevich/WishlistOfTastes/assets/109979502/f559db62-8552-4fc4-b5bb-dd1fb7dfe8e7)

**О создателе:**

![image](https://github.com/kostevich/WishlistOfTastes/assets/109979502/ed28f638-8cf6-4f37-980c-2de221390c27)

_Copyright © Kostevich Irina. 2023._
