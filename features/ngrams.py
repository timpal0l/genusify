from sklearn.feature_extraction.text import CountVectorizer

text = "this is a foo bar sentences and i want to ngramize it"
vectorizer = CountVectorizer(ngram_range=(1, 6))
analyzer = vectorizer.build_analyzer()
print
analyzer(text)
