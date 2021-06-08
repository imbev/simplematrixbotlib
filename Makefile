.DEFAULT_GOAL = help
.PHONY: help prep build upload clean-windows clean-linux

help:
	@echo --HELP--
	@echo make help - display this message
	@echo make prep - install neccesary packages for development
	@echo make build - build wheel etc. for Pypi
	@echo make upload - upload dist to PyPi
	@echo make clean-windows - clean project of unwanted files and dirs on windows
	@echo make clean-linux - clean project of unwanted files and dirs on linux

prep:
	@echo --PREP--
	python -m pip install wheel twine

build:
	@echo --BUILD--
	python setup.py sdist bdist_wheel

upload:
	@echo --UPLOAD--
	twine upload dist/*

clean-windows:
	@echo --CLEAN-WINDOWS--
	if exist build rmdir /S /Q build
	if exist dist rmdir /S /Q dist
	if exist simplematrixbotlib.egg-info rmdir /S /Q simplematrixbotlib.egg-info
	if exist simplematrixbotlib\__pycache__ rmdir /S /Q simplematrixbotlib\__pycache__
	if exist "doc/_build" rmdir /S /Q "doc/_build"

clean-linux:
	@echo --CLEAN-LINUX--
	rm -r -f build
	rm -r -f dist
	rm -r -f simplematrixbotlib.egg-info
	rm -r -f simplematrixbotlib/__pycache__
	rm -r -f doc/_build
