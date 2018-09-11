from setuptools import setup
import os
import codecs
import re


install_requires = ['aiohttp>=3.0.1']
extras_require = {
    'aioredis': ['aioredis>=1.0.0'],
}

def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return open(fpath(fname),encoding='utf-8').read()


def desc():
    info = read('README.rst')
    try:
        return info + '\n\n' + read('doc/changelog.rst')
    except IOError:
        return info


file_text = read(fpath('mw_aiohttp_session/__init__.py'))


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval


setup(name='mw-aiohttp-session',
      version=grep('__version__'),
      description=("only for maxwin aiohttp session"),

      long_description=desc(),
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: AsyncIO',
      ],
      author=grep('__author__'),
      author_email=grep('__email__'),
      url='https://github.com/candyABC/mw-aiohttp-session',
      license='Apache 2',
      packages=['mw_aiohttp_session'],
      python_requires=">=3.5",
      install_requires=install_requires,
      include_package_data=True,
      extras_require=extras_require)