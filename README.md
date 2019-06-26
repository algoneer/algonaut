# Algonaut - The Algoneer API

Algonaut is an API service that exposes the functionality of
the Algoneer algorithm toolkit.

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

To run the background worker:

    algonaut worker run

You can set up a local RabbitMQ broker by using the
`algonaut worker initialize-rabbitmq` command.

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
