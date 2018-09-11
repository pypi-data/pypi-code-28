import unittest

from pcu_nlp.pcu_nlp import spacyPipeline
from pcu_nlp.pcu_nlp import tokenize
from pcu_nlp.pcu_nlp import extractAnnotations

class test_pcu_nlp(unittest.TestCase):

	def test_spacy(self):
		try:
			file = open("data/test.txt", "r") # read test file
		except IOError:
			print('cannot open')
		else:
			text = file.read() # content of the test file
			print(text)
			self.assertIn('Information extraction', text)
			doc = spacyPipeline("en", text) # spacy pipeline
			print("************ Tokens ************")
			tokens = tokenize(doc) # tokens of the text
			print(tokens)
			print("************ Annotations ************")
			annotations = extractAnnotations(doc) # annotations of the text
			print(annotations)
			self.assertNotEqual(tokens, []) # tokens not empty
			self.assertNotEqual(annotations, []) # annotations not empty
			file.close()

if __name__ == '__main__':
	unittest.main()