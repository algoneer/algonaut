# Algonaut - The Algoneer API

Algonaut is an API service that exposes the functionality of
the Algoneer algorithm toolkit. The following sections explain how you can
set up Algonaut locally.

## Installing

You can install Algonaut using pip:

    pip install .

When developing Algonaut, you can install the package in development mode,
which will not copy files but instead link them to your virtual environment
so that you can edit them and see changes immediately:

    pip install -e .

If you want to run tests, please also install test dependencies:

    pip install -r requirements-test.txt --no-index --find-links wheels

## Defining settings

Algonaut loads settings from the directory specified in the `ALGONAUT_SETTINGS_D`
environment variable. You can specify multiple directories separated by
a `:` character as well.

For development, you can point the variable to the `settings` directory in
the Algonaut repository:

    export ALGONAUT_SETTINGS_D=settings

Alternatively you can source the `.dev-setup` file into your environment:

    source .dev-setup

This will set all required environment variables.

## Migrations

Algonaut runs on Postgres (but can support SQLite too). The database schema is
managed using SQL migration files. To run the migrations simply execute

    algonaut db migrate

To add a new migration, create a pair of files in the `migrations` directory
and define your SQL commands for migrating up and down. Take a look at the
existing files to get a feeling for the format.

## Running Algonaut

To run Algonaut:

    algonaut api run

To run the background worker (only required if you use RabbitMQ):

    algonaut worker run

# Developer Information

The following sections are only relevant if you want to actively develop Algonaut.

## Upgrading packages

You can use the fabulous `pur` tool to upgrade packages in the requirements files:

    # will update normal requirements
    pur -v -r requirements.txt
    # will update test requirements
    pur -v -r requirements-test.txt

## Building Wheels

We install all packages from local wheels if possible (for security reasons), to
generate these wheels simply use the following commands:

    pip wheel --wheel-dir wheels -r requirements.txt
    pip wheel --wheel-dir wheels -r requirements-test.txt

## Making a New Release

To release a new version of Algonaut, follow these steps:

* Make sure all tests pass for the new release.
* Update `setup.py` with the new version number. We follow the
  [semantic versioning](https://semver.org/) standard for our version
  numbers.
* Add a changelog entry in the `README.md`.
* Commit the updated `setup.py` and `README.md` files to the repository.
* Create a new tag with the version number (which is required for CI integration):

      git tag -a v0.1.4 -m "v0.1.4"
* Push the tag to the main repository together with the commit

      git push origin master --tags
* Gitlab/Travis will pick up the version tag and make the release for us.
* Alternatively, you can create the distribution packages using `setup.py`:

      python setup.py sdist bdist_wheel
* You can also manually publish the packages to PyPi via Twine
  (not recommended):
  
      twine upload dist/*
