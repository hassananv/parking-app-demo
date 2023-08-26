# Running with Docker Compose

The following instructions provide details on how to deploy the project using Docker Compose.  This method of deployment is intended for local development and demonstration purposes.  It is **NOT** intended to support production level deployments where security, availability, resilience, and data integrity are important.

All application services are exposed to the host so they may be easily accessed individually for development and testing purposes.

## Benefits

The benefits to using this approach are;
* Ease of getting the project up and running on your local system.
* Builds the images using the source code from your local working copy.  This allows you to test your changes without having to commit code in a branch.
* Fewer moving parts for developers to have to content with when developing locally; when compared with the OpenShift approach.

## Prerequisites

* Docker and Docker Compose
  * Install and configure Docker and Docker Compose on your system.  The recommended approach is to use either [Homebrew](https://brew.sh/) (MAC) or [Chocolatey](https://chocolatey.org/) (Windows) to install Docker (which includes Docker Compose).
  * You may also refer to the docker documentation for [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installation instructions.
* The S2I CLI
  * Download and install the S2I CLI tool; [source-to-image](https://github.com/openshift/source-to-image)
  * Make sure it is available on your `PATH`.  The `manage` script will look for the `s2i` executable on your `PATH`.  If it is not found you will get a message asking you to download and set it on your `PATH`.
* If you are working on Windows, use Git Bash (or equivalent shell) to run the scripts.
* Ensure to have internet connection without VPN.
* Fork and clone a local working copy of the project source code.
* Open a command/shell window to the project's `./docker` folder.

## Management Script

The `manage` script (located in the docker folder) wraps the Docker and S2I process in easy to use commands.

To get full usage information on the script run:
```
./manage -h
```
  
## Building the Images

The first thing you'll need to do is build the Docker images.  Since this requires a combination of Docker and S2I builds the process has been scripted inside `manage`.  _The `docker-compose.yml` file does not perform any of the builds._

To build the images run:
```
./manage build
```

## Starting the Project

To start the project run:
```
./manage start
```

This will start the project interactively; with all of the logs being written to the command line.  Press `Ctrl-C` to shut down the services from the same shell window.

If you want to change the database keys; start the project by running:

```
./manage start POSTGRESQL_DATABASE=your_db_name POSTGRESQL_USER=your_db_user POSTGRESQL_PASSWORD=your_db_password
```


## Stopping the Project

To stop the project run:
```
./manage stop
```

This will shut down and clean up all of the containers in the project.  This is a non-destructive process.  The containers are not deleted so they will be reused the next time you run start.

Since the services are started interactively, you will have to issue this command from another shell window.  This command can also be run after shutting down the services using the `Ctrl-C` method to clean up any services that may not have shutdown correctly.

## Using the Application

* The main UI is exposed at; http://localhost:8081/
* The API is exposed at; http://localhost:8080/docs#/
* The database is exposed at; localhost:5432
