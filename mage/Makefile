.PHONY: build test run

run: build
	@docker run --rm --network=dungeonsnpipes_default roqueando/spells:stable $(module)

build:
	@docker build -t roqueando/spells:stable -f Dockerfile.spells .

test:
	python -m pytest
