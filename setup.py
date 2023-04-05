import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


setup(
    name="nutrinews",
    version="0.1.0",
    url="https://github.com/devbisme/nutrinews",
    license="MIT",
    author="Dave Vandenbout",
    author_email="devb@xess.com",
    description="Make news more nutritious by removing bias.",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=["bs4", "pyperclip", "openai", "requests"],
    entry_points={
        "console_scripts": [
            "nutrinews=nutrinews.nutrinews:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
