import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'easy_utils',
    version = '0.0.2',
    author = 'Dane Morgan',
    author_email = 'danemorgan91@gmail.com',
    description = 'Easy to use utilities, like logging, downloading, uploading, and file checking',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/deadlift1226/easy_utils.git',
    install_requires = [
        'colorama'
        ],
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

