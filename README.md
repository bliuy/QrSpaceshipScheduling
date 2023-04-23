# Introduction
This project is created as an example to solve the Spaceship optimization problem.

A webserver is created with 2 endpoints:

* /testing (GET): Used to test if the webserver has been setup properly. No payload required within the request.
* /spaceship/optimize (POST): Used to solve the spaceship optimize problem. Payload required for a valid response.

# Setup Guide

Both the Linux and Windows versions assume that >= Python 3.10 is installed within the system.

The Windows setup installs packages into the default Python environment. A virtualenv must be setup by the user beforehand if required.

## Linux
1. Ensure that the make utility is installed within your environment.
2. Navigate to the root of the project folder.
3. Run the following command which will automatically install the required dependencies and start the webserver: 

    make

4. If there are prompts for the restarting of services during the running of the makefile, proceed with the default option.
5. Shut down the webserver using the keyboard shortcut ctrl+c.
6. Run the following command to remove the virtualenv that was created to run the webserver.

    make clean

## Windows
1. Open up cmd and navigate to the root of the project folder.
2. Run the following commands to install the required packages:

    python3 -m pip install httpx

    python3 -m pip install fastapi

    python3 -m pip install "uvicorn[standard]"

    python3 -m pip install install pydantic

    python3 -m pip install gunicorn

3. Run the following command to execute the unit tests. If all tests pass, then the setup was successful.

    python3 unittests.py

4. Start the webserver using the following command:

    python3 src\main.py

5. Shut down the webserver using the keyboard shortcut ctrl+c.

# Getting Started
* Once the webserver is running, access the following page via your browser: localhost:8080/docs
    * This will open up the docs that provide information regarding the payload structure and the expected responses.
    * The docs also provide the functionality to send test payloads to the respective endpoints.
* The server timeout parameter is set to 600 seconds.
    * This means that if the response result cannot be calculated within the timeout limit then a timeout response is returned.

# Sample Benchmarks
## Test Bench \& Assumptions
* Benchmarks run on the following machine: r5.large EC2 instance.
* Benchmarks were run using the sample inputs found in the examples folder.
* Only 1 run used for each benchmark.
* No network delays are considered.
## Benchmarking results
* Input: 50 contracts - 1705.887246 ms
* Input: 100 contracts - 101843.528398 ms