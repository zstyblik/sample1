# sample1

sample1 is a vagrant box provisioned by ansible with:

* HAproxy acting as load-balancer
* web application written in Django(Python) running in Docker container to
  store/list events in DB
* PostgreSQL running in Docker container

Despite there are two instances of web application, PostgreSQL is obviously
SPOF in this example.

## Dependencies

* ansible=2.1.0-2
* vagrant=2.0.1

## How-to run/setup

```
# Install ansible dependencies
ansible-galaxy install -p provisioning/roles/ -r requirements.yml
# Start and provision vagrant environment
vagrant up
```

## Web application

Once vagrant environment is up, web application should be reachable at
`http://localhost:8080`.

## URIs

Followin URIs are available:

* `/events`
 * `GET` to list events in DB
 * `POST` to push event into DB
* `/event/<id>/` to show one particular event stored in DB

## Structure of Event

Event is expected to be in JSON format with the following mandatory attributes:

* `timestamp` - seconds since 1970-01-01 00:00:00 UTC aka Unix timestamp
* `message` - text

## How-to test

```
# In order to push some event run the following command
curl -XPOST -H 'Content-Type: application/json' http://localhost:8080/events \
    -d '{"timestamp": 1515948504, "message": "Printer is on fire"}'
# To list events stored in DB
curl http://localhost:8080/events
# And to get the detail of particular event
curl http://localhost:8080/event/1/
```

## Extra notes

PostgreSQL configuration is being fetched from ENV variables. Therefore, sadly
these variables must be set in order to use `manage.py`.

* `POSTGRES_HOST`
* `POSTGRES_DB`
* `POSTGRES_USER`
* `POSTGRES_PASS`

# References

* https://github.com/geerlingguy/ansible-vagrant-examples
