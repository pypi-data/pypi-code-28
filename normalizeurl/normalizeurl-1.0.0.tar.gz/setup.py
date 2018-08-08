import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "normalizeurl",
    packages = ["normalizeurl"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    version = "1.0.0",
    description = "Normalize a URL",
    author = "Yoginth",
    author_email = "yoginth@zoho.com",
    url = "https://yoginth.gitlab.io",
    classifiers=(
        "Programming Language :: Python",
        "Natural Language :: English",
        "Environment :: Plugins",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ),
    project_urls={
        'Patreon': 'https://www.patreon.com/yoginth',
        'Source': 'https://gitlab.com/yoginth/normalizeurl',
    },
    install_requires=[
        'future',
    ],
)
