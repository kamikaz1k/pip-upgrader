.PHONY: install

install:  # install package with test dependencies
	pip install -e .[test]

tests: # Run unit tests
	py.test
