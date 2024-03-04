# prov-tools
A very simple first attempt of using FastAPI. The concept and some of the code is copied from a functional application 
which uses Flask OpenAPI3.  

The initial example exposes an endpoint that receives a netbox webhook event then
just prints the event content. The code doesn't perform any other processing than that.

The plan is to continue adding functionality such as example DynamodDB, ORM, SQS/SNS, etc. 
solutions.  The main idea is to use this repo to explore all things AWS and to revisit
code/solutions previous developed in Flask but lever FastAPI as the framework.

## file layout
* app - main application folder
  * `main.py` - contains the bootstrap for either running the app from a command line or as a wsgi
  * `.env` - contains the app inventory environment
  * `event_test_client.py` - a test client 
  * test - unit/py test (no tests so far)
    * mock_data - folder containing mock data
      * [README.md](./tests/mock_data/README.md)
  * models - contains pydantic models
    * `__init__.py` - contains common models
    * `netbox.py` - netbox event models *(currently contains device and IP Address models)*
  * static - meant for any static files such as images, CSS, etc. but could contain Javascript
  * routers - endpoint routes are defined here
    * `webhook.py` - exposes a netbox webhook event receiver
    * `devices.py` - exposes a REST wrapper around nornir/napalm supported functions *(Note only limited functions are exposed at this time)*
  * provisioning - contains provisioning related modules *(in the future we'd refactor to maintain such logic in a package/repo)*
    * `dns.py` - a very simple/example stub that might be used for future DNS provisioning
    

## run app
The following examples assume a python virtual environment is available in `.venv`

### run from python
```shell
.venv/bin/python -m app.main

```

### run as uvicorn
```shell
.venv/bin/uvicorn app.main:app
```