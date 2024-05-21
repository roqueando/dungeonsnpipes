.PHONY: build test run

run: build
	@docker run --rm --network=dungeonsnpipes_default roqueando/spells:stable $(module)

build:
	@docker build -t roqueando/spells:stable -f Dockerfile.spells .

test-spec:
	python -m pytest -s -v -k $(spec)

test:
	python -m pytest -s -v 
