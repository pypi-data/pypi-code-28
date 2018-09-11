import spacy
from spacy import displacy

"""
Copyright (C) 2018 Stella Zevio
stella.zevio@lipn.univ-paris13.fr
This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class Token: 
	def __init__(self, token_text, token_lemma, token_pos, token_tag, token_dep, token_shape, token_is_alpha, token_is_stop):
		self.token_text= token_text # text
		self.token_lemma= token_lemma # lemma
		self.token_pos= token_pos # pos
		self.token_tag= token_tag # tag
		self.token_dep= token_dep # dep
		self.token_shape= token_shape # shape
		self.token_is_alpha= token_is_alpha # is alpha ?
		self.token_is_stop= token_is_stop # is stop ?    
	def __repr__(self): # representation of a keyphrase
		return repr((self.token_text, self.token_lemma, self.token_pos, self.token_tag, self.token_dep, self.token_shape, self.token_is_alpha, self.token_is_stop))


def explain(category) :
	"""Explain a syntactic category.
	Parameter :
	category -- a syntactic category 
	Return :
	explanation -- explanation of the syntactic category
	"""
	print(spacy.explain(category))

def renderEntities(doc):
	"""Render entities in the document.
	Parameter :
	doc -- Spacy document
	Return :
	html -- document rendering (entities style)
	"""
	html = displacy.serve(doc, style='ent') # server enablement
	return html

def renderParseTree(doc):
	"""Render document's associated syntactic dependencies tree.
	Parameter :
	doc -- Spacy document 
	Return :
	html -- document rendering (parse tree style)
	"""
	html = displacy.serve(doc, style='dep') # server enablement
	return html

def getSentiment(doc):
	"""Get document global sentiment.
	Parameter :
	doc -- Spacy document
	Return :
	sentiment -- document global sentiment 
	"""
	return doc.sentiment

def getEntities(doc):
	"""Get entities of a document.
	Parameter :
	doc -- Spacy document 
	Return :
	ents -- entities
	"""
	ents = list(doc.ents)
	return ents

def getNounPhrases(doc):
	"""Get noun phrases of a document.
	Parameter :
	doc -- Spacy document 
	Return :
	chunks -- noun phrases 
	"""
	chunks = list(doc.noun_chunks) # noun phrases
	return chunks

def getSimilarity(doc1,doc2):
	"""Get similarity between two Spacy documents.
	Parameters :
	doc1 -- a Spacy document
	doc2 -- another Spacy document
	Return :
	similarity -- similarity between the documents 
	"""
	return doc1.similarity(doc2)

def extractAnnotations(doc):
	"""Get Spacy annotations.
	Parameter :
	doc -- a Spacy document
	Return :
	annotations -- syntactic annotations 
	"""
	annotations = getEntities(doc) + getNounPhrases(doc) # get document entities and noun phrases
	for annotation in annotations:
		annotation.merge()
	return annotations

def tokenize(doc):
	"""Tokenization of the document
	Parameter :
	doc -- a Spacy document 
	"""
	tokens_obj = []
	for token in doc:
		print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
		tokens_obj.append(Token(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop))
	return tokens_obj    

def loadPipeline(language):
	"""Load Spacy pipeline.
	Parameter :
	language -- main language used within the text on which Spacy pipeline will be applied
	Return :
	nlp -- Spacy pipeline 
	"""
	nlp = spacy.load(language)
	return nlp

def spacyPipeline(language, text):	
	"""Apply spacy pipeline to a text, according to a language. 
	Parameter :
	language -- main language used in the text
	text -- text on which spacy pipeline will be applied 
	Return :
	annotations -- Spacy annotations of the text 
	"""
	nlp = loadPipeline(language) # load pipeline
	doc = nlp(text) # apply pipeline on the text and get the Spacy document
	return doc

if __name__ == '__main__':
	main()