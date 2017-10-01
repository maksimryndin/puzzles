.PHONY: all, rundev, shell, test

all:
	pip install -r requirements.txt
	make test
	make rundev

rundev:
	python run.py --debug=True

doc:
	./docs/run.sh

test:
	python -m tornado.test.runtests tests.test_puzzles