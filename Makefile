SETTINGS := postgres
ALGONAUT_SETTINGS_D := settings:algonaut_tests/settings/$(SETTINGS)

all: format flake mypy test

lint:
	pylint -E algonaut

flake:
	autoflake --remove-all-unused-imports -i algonaut/**/*.py
	autoflake --remove-unused-variables -i algonaut/**/*.py

format:
	black algonaut/
	black algonaut_tests/

mypy:
	mypy algonaut/

update:
	pip3 install pur
	pur -r requirements.txt
	pur -r requirements-test.txt

release:
	python3 setup.py sdist
	twine upload dist/* -u ${TWINE_USER} -p ${TWINE_PASSWORD}

test:
	ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(testargs) algonaut_tests
	#ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(testargs) algonaut/plugins
