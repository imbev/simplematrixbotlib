from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A simple matrix bot library.'
LONG_DESCRIPTION = 'An easy to use bot library for the Matrix ecosystem written in Python.'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="simplematrixbotlib", 
        version=VERSION,
        author="krazykirby99999",
        author_email="krazykirby99999@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            matrix-nio
        ],
        keywords=['python', 'matrix','bot'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Topic :: Communications :: Chat",
            "Topic :: Internet"
        ]
)