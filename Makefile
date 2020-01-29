PYTHON = python
PYTEST = $(PYTHON) -m pytest

test:
	$(PYTEST) ./src/tests
