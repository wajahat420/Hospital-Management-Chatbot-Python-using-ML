def remove_stopwords(wrds):
	# print("wrds",wrds)
	stop_words = ["a","the","an","i","to","my","me","you","and",",","."]
	for i in stop_words:
		i = i.lower()
		if i in wrds:
			# print("i",i)
			wrds.remove(i)

	return wrds
