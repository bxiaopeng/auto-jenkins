.PHONY: test clean

init:
	pip install pipenv --upgrade
	pipenv install --skip-lock

install: test
	python setup.py install

upload: test
	python setup.py sdist upload -r local

test:
	pytest tests

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

flake8:
	pipenv run flake8 --ignore=E501,F401,E128,E402,E731,F821 auto-jenkins

ci:
	pipenv run py.test -n 8 --boxed --junitxml=report.xml

coverage:
	pipenv run py.test --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=auto-jenkins tests