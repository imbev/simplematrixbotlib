.DEFAULT_GOAL = help
.PHONY: help prep build upload clean-windows clean-linux

help:
	@echo --HELP--
	@echo make help - display this message
	@echo make prep - run "poetry install"
#	@echo make test - run tests on the project
	@echo make build - run "poetry build"
	@echo make upload - run "poetry publish"
	@echo make clean-windows - clean project of unwanted files and dirs on windows
	@echo make clean-linux - clean project of unwanted files and dirs on linux

prep:
	@echo --PREP--
	poetry install

#test:
#	@echo --TEST--
#	python -m unittest discover -s tests

build:
	@echo --BUILD--
	poetry build

upload:
	@echo --UPLOAD--
	poetry publish

clean-windows:
	@echo --CLEAN-WINDOWS--
	if exist build rmdir /S /Q build
	if exist dist rmdir /S /Q dist
	if exist simplematrixbotlib.egg-info rmdir /S /Q simplematrixbotlib.egg-info
	if exist simplematrixbotlib\__pycache__ rmdir /S /Q simplematrixbotlib\__pycache__
	if exist "doc/_build" rmdir /S /Q "doc/_build"
	if exist tests\__pycache__ rmdir /S /Q tests\__pycache__

clean-linux:
	@echo --CLEAN-LINUX--
	rm -r -f build
	rm -r -f dist
	rm -r -f simplematrixbotlib.egg-info
	rm -r -f simplematrixbotlib/__pycache__
	rm -r -f doc/_build
	rm -r -f tests/__pycache__
