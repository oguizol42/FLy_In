UV          = uv
PYTHON      = $(UV) run python
MAIN        = fly_in.py

MYPY_FLAGS  = --warn-return-any \
              --warn-unused-ignores \
              --ignore-missing-imports \
              --disallow-untyped-defs \
              --check-untyped-defs
LINT_EXCLUDE = .venv

.PHONY: install run debug clean lint lint-strict

install:
	$(UV) sync

run:
	$(PYTHON) $(MAIN)

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -not -path "./$(LINT_EXCLUDE)/*" \
		-prune -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) \
		-not -path "./$(LINT_EXCLUDE)/*" -delete
	rm -rf .mypy_cache .pytest_cache

lint:
	$(UV) run flake8 . --exclude=$(LINT_EXCLUDE)
	$(UV) run mypy . --exclude $(LINT_EXCLUDE) $(MYPY_FLAGS)

lint-strict:
	$(UV) run flake8 . --exclude=$(LINT_EXCLUDE)
	$(UV) run mypy . --exclude $(LINT_EXCLUDE) --strict
