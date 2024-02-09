.PHONY: test mypy pytest black

all: lint mypy test refurb

install:
	pip install -r dev-requirements.txt

lint: ruff black isort

ruff:
	ruff cal9000 test

black:
	black cal9000 test -l 79 --check --diff --color

isort:
	isort . --diff --check

mypy:
	mypy -p cal9000
	mypy -p test

test:
	pytest

refurb:
	refurb cal9000 test

clean:
	rm -rf .mypy_cache .ruff_cache .pytest_cache
