.PHONY: install
install:
	uv sync

.PHONY: tw
tw:
	uv run tailwindcss -i src/app.tw.css -o static/tailwind.css --watch

.PHONY: tw-build
tw-build:
	uv run tailwindcss -i src/app.tw.css -o static/tailwind.css --minify

.PHONY: run
run:
	make tw &
	uv run flask --app app run --port 5001 --debug
