from setuptools import setup, find_packages
import os

VERSION = '2.1.0'
DESCRIPTION = 'An easy to use bot library for the Matrix ecosystem written in Python.'
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'README.md'),
          encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    # the name must match the folder name 'verysimplemodule'
    name="simplematrixbotlib",
    version=VERSION,
    author="krazykirby99999",
    author_email="krazykirby99999@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "matrix-nio == 0.18.6", "python-cryptography-fernet-wrapper == 1.0.4",
        "pillow == 8.2.0", "markdown == 3.3.4"
    ],
    keywords=[
        'python', 'matrix', 'bot', 'simple', 'library',
        'simplepythonbotlibrary', 'simplepythonbotlib',
        'simple-python-bot-library', 'simple-python-bot-lib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat", "Topic :: Internet"
    ])
