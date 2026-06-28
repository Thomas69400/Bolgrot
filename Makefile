SRC := src
UV := uv

all: run

install:
	$(UV) sync

run: install
	$(UV) run python -m $(SRC)

lint:
	flake8 $(SRC)
	mypy $(SRC)

clean:
	find . -type d -name "__pycache__" | xargs rm -rf || true
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info