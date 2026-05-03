.PHONY: env shell install clean lock lint lintfix types tests quality

env:
	uv venv

install: # Install everything there is
	uv sync --all-extras --all-groups

clean: # Remove packages that are not specified in pyproject.toml
	make install

lint:
	uv run ruff check cipug tests

lintfix:
	uv run ruff check cipug tests --fix

types:
	uv run basedpyright cipug tests

test_mocked:
	uv run pytest tests/test_A_unit_tests tests/test_B_end2end_tests

test_real:
	uv run pytest tests/test_C_real_tests

tests: test_mocked test_real

quality:
	make lint
	make types
	make tests
