from setuptools import setup


setup(
    name="chariot",
    version="0.4.1",
    description="Deliver the read-to-train data to your NLP model.",
    keywords=["machine learning", "nlp", "natural language processing"],
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    license="Apache License 2.0",
    packages=[
        "chariot",
        "chariot.resource",
        "chariot.transformer",
        "chariot.transformer.formatter",
        "chariot.transformer.text",
        "chariot.transformer.token",
        "chariot.transformer.tokenizer"
        ],
    url="https://github.com/chakki-works/chariot",
    install_requires=[
        "numpy>=1.14.4",
        "scipy>=1.1.0",
        "scikit-learn>=0.19.1",
        "spacy>=2.0.11",
        "pandas>=0.23.1",
        "chazutsu>=0.8.1",
        "chakin>=0.0.6",
        "tqdm>=4.23.4"
    ],
)
