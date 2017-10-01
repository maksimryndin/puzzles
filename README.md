Puzzles Service
===============

Uses Elasticsearch as a storage for CRUD-actions with puzzles.
On app start loads initial data if these data are not present in the storage.

Based on Tornado Web Server because of its [good performance](http://klen.github.io/py-frameworks-bench/#remote) 
for proxying other services.

### EXTERNAL DEPENDENCIES
* Docker
* Docker compose
* Make (optional, for development only)

### TESTS
* $ make test

### RUN
* $ docker volume create --name=esdata
* $ docker-compose up
* $ make rundev

### DOCUMENTATION
* $ make doc

### TODO
* add analyzers for partial search
* add pagination
* add tests for search
* add partial fields validation for put
* add inter-service authentication
