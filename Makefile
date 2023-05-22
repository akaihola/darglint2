MOCK_VERSION ?= v1.5
.PHONY: docs
docs:
	MOCK_VERSION=$(MOCK_VERSION) poetry run sphinx-build -a -v docs/source docs/build

.PHONY: docs-polyversion
docs-polyversion:
	poetry run sphinx_polyversion -a -v docs/source docs/build --poetry-groups docs

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: test
test:
	poetry run tox

.PHONY: clean
clean:
	rm -R -f docs/build
