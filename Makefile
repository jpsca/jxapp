.PHONY: install
install:
	uv sync

.PHONY: run
run:
	uv run flask --app app run --port 6000 --debug
