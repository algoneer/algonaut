SETTINGS := postgres
ALGONAUT_SETTINGS_D := settings:algonaut_tests/settings/$(SETTINGS)

all: format flake mypy test

lint: venv/bin/pylint
	venv/bin/pylint -E algonaut

flake: venv/bin/autoflake
	venv/bin/autoflake --remove-all-unused-imports -i algonaut/**/*.py
	venv/bin/autoflake --remove-unused-variables -i algonaut/**/*.py

venv/bin/autoflake:
	make requirements

venv/bin/pylint:
	make requirements

venv/bin/black:
	make requirements

venv/bin/mypy:
	make requirements

format: venv/bin/black
	venv/bin/black algonaut/
	venv/bin/black algonaut_tests/

mypy: venv/bin/mypy
	venv/bin/mypy algonaut/
	venv/bin/mypy algonaut_tests/

venv/bin/pur: venv
	venv/bin/pip install pur


update: venv pur
	venv/bin/pur -r requirements.txt
	venv/bin/pur -r requirements-test.txt

venv/bin/twine: venv
	venv/bin/pip install twine

release: twine
	venv/bin/python setup.py sdist
	venv/bin/twine upload dist/* -u ${TWINE_USER} -p ${TWINE_PASSWORD}

setup: requirements

teardown:
	rm -rf venv
	rm -rf docs/build/*

venv:
	virtualenv --python python3 venv

requirements: venv
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -r requirements-test.txt

test:
	ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) venv/bin/pytest $(testargs) algonaut_tests
	#ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(testargs) algonaut/plugins
