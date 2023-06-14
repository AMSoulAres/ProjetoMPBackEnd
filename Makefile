all:
	python -m uvicorn app.src.main:app --reload

test:
	pytest -vv --cov

pylint:
	pylint ./app