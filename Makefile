format:
	poetry run black src/tock_genai_core tests --line-length=120
	poetry run flake8 --ignore=E101,E111,E114,E115,E116,E117,E12,E13,E2,E3,E401,E5,E70,W1,W2,W3,W5 --per-file-ignores="__init__.py:F401" --max-line-length=120 src/tock_genai_core

