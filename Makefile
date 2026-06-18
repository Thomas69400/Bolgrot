SRC := src
UV := uv

install:
	$(UV) sync

run: install
	$(UV) run python -m $(SRC)