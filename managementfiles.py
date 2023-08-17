# Импортируем os для работы с файлами.
import os

# Функция для удаления изображений, принимающая в качестве аргументов поля статьи, которую удаляют(article) и поля всех статей(articles).
def delete_files(article, articles):
	# Создаем переменную количество изображений.
	count = 0
	# Итерируем поля всех статей.
	for articleview in articles:
		# Если картинка, статьи которую удаляют такая же как и картинка в бд.	
		if article.image in articleview.image:
			# То добавляют к количеству 1.
			count +=1
	# Если количество меньше 2.
	if count < 2:
		# Удаляем изображение.
		os.remove((f"static//uploadimages//{article.image}"))
		

# Функция для работы с картинками, принимающая в качестве аргументов поля статьи, которая была заполнена в форме ранее(articleold) и поля всех статей(articles).
def updating_files(articles, articleold):
	# Создаем переменную количество изображений равнозначных articleold.
	countold = 0
	# Итерируем поля всех статей.
	for articleview in articles:
		# Если картинка, статьи которой были заданы в форме ранее такая же как и картинка в бд.
		if articleold in articleview.image:
			# То добавляют к количеству 1.
			countold +=1
	# Если количество меньше 1.
	if countold < 1:
		# Удаляем изображение.
		os.remove((f"static//uploadimages//{articleold}"))