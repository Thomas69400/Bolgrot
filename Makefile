SRC := src
UV := uv

all: run

install:
	$(UV) sync

run: install
	$(UV) run python -m $(SRC)