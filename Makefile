SETTINGS := postgres
ALGONAUT_SETTINGS_D := settings:tests/settings/$(SETTINGS)

all: format mypy test

format:
	black algonaut/

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
	ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(testargs) tests
	#ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(testargs) algonaut/plugins
