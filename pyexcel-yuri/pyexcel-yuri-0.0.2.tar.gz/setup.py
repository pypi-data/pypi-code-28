# Template by setupmobans
import os
import sys
import codecs
from shutil import rmtree
from setuptools import setup, find_packages, Command

NAME = 'pyexcel-yuri'
AUTHOR = 'Yuri'
VERSION = '0.0.2'
EMAIL = 'yuri@yuri-x.com'
LICENSE = 'New BSD'
DESCRIPTION = (
    'A wrapper library to read, manipulate and write data format'
)
URL = 'https://github.com/Yuri-x/pyexcel-yuri'
DOWNLOAD_URL = '%s/archive/0.0.2.tar.gz' % URL
FILES = ['README.rst', 'CHANGELOG.rst']
KEYWORDS = [
    'xlsx'
    'python'
]

CLASSIFIERS = [
    'Topic :: Office/Business',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: PyPy'
]

INSTALL_REQUIRES = [
    'openpyxl>=2.5.0',
    'pyexcel-io>=0.5.3',
    'Xlsxwriter',
    'pandas>=0.23.4'
]
SETUP_COMMANDS = {}


PACKAGES = find_packages(exclude=['ez_setup', 'examples', 'tests'])
EXTRAS_REQUIRE = {
}
# You do not need to read beyond this line
PUBLISH_COMMAND = '{0} setup.py sdist bdist_wheel upload -r pypi'.format(
    sys.executable)
UPLOAD_FAILED_MSG = (
    'Upload failed. please run "%s" yourself.' % PUBLISH_COMMAND)
HERE = os.path.abspath(os.path.dirname(__file__))


class PublishCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package on github and pypi'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print(s)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(HERE, 'dist'))
            rmtree(os.path.join(HERE, 'build'))
            rmtree(os.path.join(HERE, 'pyexcel_yuri.egg-info'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        run_status = True
        if run_status:
            if os.system(PUBLISH_COMMAND) != 0:
                self.status(UPLOAD_FAILED_MSG % PUBLISH_COMMAND)

        sys.exit()


SETUP_COMMANDS.update({
    'publish': PublishCommand
})


def read_files(*files):
    """Read files into setup"""
    text = ""
    for single_file in files:
        content = read(single_file)
        text = text + content + "\n"
    return text


def read(afile):
    """Read a file into setup"""
    with codecs.open(afile, 'r', 'utf-8') as opened_file:
        content = filter_out_test_code(opened_file)
        content = "".join(list(content))
        return content


def filter_out_test_code(file_handle):
    found_test_code = False
    for line in file_handle.readlines():
        if line.startswith('.. testcode:'):
            found_test_code = True
            continue
        if found_test_code is True:
            if line.startswith('  '):
                continue
            else:
                empty_line = line.strip()
                if len(empty_line) == 0:
                    continue
                else:
                    found_test_code = False
                    yield line
        else:
            for keyword in ['|version|', '|today|']:
                if keyword in line:
                    break
            else:
                yield line


if __name__ == '__main__':
    setup(
        name=NAME,
        author=AUTHOR,
        version=VERSION,
        author_email=EMAIL,
        description=DESCRIPTION,
        url=URL,
        download_url=DOWNLOAD_URL,
        long_description=read_files(*FILES),
        license=LICENSE,
        keywords=KEYWORDS,
        extras_require=EXTRAS_REQUIRE,
        tests_require=['nose'],
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        classifiers=CLASSIFIERS,
        cmdclass=SETUP_COMMANDS
    )
