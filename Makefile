SETTINGS := postgres
ALGONAUT_SETTINGS_D := settings:tests/settings/$(SETTINGS)

test:
	ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(args) tests
	ALGONAUT_SETTINGS_D=$(ALGONAUT_SETTINGS_D) pytest $(args) algonaut/plugins
