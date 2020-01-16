

def remove_stopwords(wrds):
	# print("wrds",wrds)
	stop_words = ["a","the","an","i","to","my","me","am","are","you","you","and",",",".","please","on","it","up","at","by","or","n't","'s","in","for","had","is"]
	for i in stop_words:
		i = i.lower()
		if i in wrds:
			# print("i",i)
			wrds.remove(i)

	return wrds




