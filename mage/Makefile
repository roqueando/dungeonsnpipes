.PHONY: build test

build:
	@docker build -t roqueando/spells:stable -f Dockerfile.spells .

test:
	python -m pytest
