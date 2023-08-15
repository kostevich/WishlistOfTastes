import os
def delete_files(article, articles):
	count = 0
	for articleview in articles:	
		if article.image in articleview.image:
			count +=1
	if count < 2:
		os.remove((f"static//uploadimages//{article.image}"))
		

def updating_files(article, articles, articleold):
	countold = 0
	for articleview in articles:
		if articleold in articleview.image:
			countold +=1
	if countold < 1:
		os.remove((f"static//uploadimages//{articleold}"))