# Algonaut Worker

The responsibilities of the worker are:

* Receiving tasks from a backend, e.g. AMQP
* Executing the tasks
* Possibly returning the results of the tasks (not really required)
* Scheduling regularly running tasks

## Desirable Properties

* Tasks should be able to pick up changes in the Python code without a restart
  of the entire service.


## Implementation

* A runner 