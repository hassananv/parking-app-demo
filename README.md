# Parking Reservation Application

## Structure

## Dev environment
Currently it requires: npm 8.1.0, Node 16.13.0, Python 3.8/3.9/3.10. Running on Docker is recommended.

### Client Application (web)
A Vue client application.

#### Important commands for the web folder:
`npm install` # Build web packages  

`./run_web_local.sh` # Serve web under hot reloading 

#### The main UI is exposed at:
http://localhost:8081/


###	REST API (api)
A FastAPI based REST API which provides the heavy lifting. The API includes a Swagger interface containing API documentation and UI that allows you to interact with the various APIs manually:
http://localhost:8080/docs#/

#### Prerequisites

* Python Virtual Environment
  * Setup a [virtual environment](https://docs.python.org/3/tutorial/venv.html)

#### Important commands for the api folder:
`pip install -r requirements.txt` # Install required python packages

`./run_api_local.sh` # Run the API

###	Database (db)
A PostgreSQL database for storage.
Use the Environment Variable keys in the api/core/config.py file to setup the database and corresponding user.
The database is exposed at; localhost:5433


#### Prerequisites

* PostgreSQL running on localhost:5433
* Created db and user using keys in the api/core/config.py file.

## Running on Docker
The project can also be run locally using Docker and Docker Compose.  Refer to [Running with Docker Compose](./docker/README.md) for instructions.

## License
Code released under the [Apache License, Version 2.0](./LICENSE).
