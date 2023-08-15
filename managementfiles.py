import os
def management(article, articles):
	count = 0
	for el in articles:	
		if article.image in el.image:
			count +=1
			print(count)
	if count < 2:
		print(count)
		os.remove((f"static//uploadimages//{article.image}"))
		
    
    

