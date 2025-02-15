**Preprocessing ideas:
	
	- Tokenize
	- Conversion to lower-case	
	- Remove stop words (the, with, to, for, a, we, etc.). We need to write a list.
	- Remove punctuation
	- Remove tokens with less than 2 characters
	- Stemming (ex: forest, forests, forestation, forested ===> forest)
	//- Filter out Angus' error :P; i.e. the "Category" category. Can be done manually, only 3 entries.
	- Do we want to handle formulae? Count amount of formulae?
	
	1. make all words lower case
	2. remove punctuation
	
	3. remove tokens with less than two chars
	4. remove stop words
	5. stemming
	
	6. for group 1 and 2, build dictionaries
	
**Feature extraction:

	- Word presence/absence, bag of words or n-grams?
	- Need some kind of word occurrence threshold
	
**Classifiers:
	1) Basic: Naive Bayes
	2) Standard: To be covered in class (SVM?)
	3) Advanced: I suggest random forests	
		
	
**Sources of info:
	https://de.dariah.eu/tatom/preprocessing.html
	
**Papers:
Keyword: text categorization

General: http://nmis.isti.cnr.it/sebastiani/Publications/TM05.pdf
N-gram: http://odur.let.rug.nl/vannoord/TextCat/textcat.pdf
Bigrams: http://www.cs.ucsb.edu/~yfwang/papers/igm.pdf --> Might be interesting to try that! Pretty straigthforward.
SVM: http://www.cs.cornell.edu/people/tj/publications/joachims_98a.pdf
Regression: http://www.stat.columbia.edu/~madigan/PAPERS/techno.pdf
Classifier comparison: http://www.inf.ufes.br/~claudine/courses/ct08/artigos/yang_sigir99.pdf
Preprocessing: http://www.di.uevora.pt/~pq/papers/enia-goncalves-quaresma.pdf
