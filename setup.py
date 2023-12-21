from setuptools import setup, find_packages
import pyper

with open("README.md", "r") as fin:
    long_description = fin.read()

setup(
    name="pyper",
    version=pyper.__version__,
    author="christian.tillich.walker@gmail.com",
    author_email="christian.tillich.walker@gmail.com",
    description="A tool for managing data preprocessing workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/christiantillich/pyper/tree/main/",
    packages=["pyper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas>=1.1.1"
    ],
    python_requires=">=3.6",
)