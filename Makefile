.PHONY: test mypy pytest black

all: lint mypy test

install:
	pip install -r dev-requirements.txt

lint: black isort

black:
	black cal9000 test -l 79 --check --diff --color

isort:
	isort . --diff --check

mypy:
	mypy -p cal9000
	mypy -p test

test:
	pytest --cov=cal9000
