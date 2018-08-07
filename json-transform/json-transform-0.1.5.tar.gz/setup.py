import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="json-transform",
    version="0.1.5",
    author="Peter Morawski",
    author_email="contact@peter-morawski.de",
    description="Allows to serialize python classes into JSON objects and deserialize JSON objects into python classes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/Peter-Morawski/json_transform",
    install_requires=["decorator", "python-dateutil"],
    py_modules=["jsontransform"],
    license="MIT License",
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Communications",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ),
)
