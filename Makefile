UV = uv

.PHONY: install run debug clean lint lint-strict

install:
	$(UV) sync

run:
	$(UV) run python fly_in.py

debug:
	$(UV) run python -m pdb fly_in.py

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
	rm -rf .mypy_cache .pytest_cache

lint:
	$(UV) run flake8 --exclude=.venv .
	$(UV) run mypy . --exclude-gitignore --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV) run flake8 --exclude=.venv .
	$(UV) run mypy . --strict --exclude-gitignore