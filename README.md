# Web ADMIN EWP

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/lswms_admin) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/lswms_admin)

This project is the Water Point Database Administrator for Ethiopia. It was developed in Python and Flask and aims to allow administrator users to modify the various contents of this database.

**Important notes**

This web admin must be used in conjunction with the models that was developed for the project, which you can find in this [repository](https://github.com/CIAT-DAPA/lswms_models).

## Getting Started

To use the wep admin, it is necessary to have an instance of MongoDB running, either locally or on a server that is accessible from the internet.

### Prerequisites

- Python 3.x
- MongoDB

## Installation

To use the wep admin, it is necessary to have an instance of MongoDB running. It is also recommended to create a virtual environment to work with this project and make sure that the dependencies are installed in the virtual environment instead of the global system.

1. Clone the repository
````sh
git clone https://github.com/CIAT-DAPA/lswms_admin
````

2. Create a virtual environment
````sh
python -m venv env
````

3. Activate the virtual environment
- Linux
````sh
source env/bin/activate
````
- windows
````sh
env\Scripts\activate.bat
````

4. Install the required packages

````sh
pip install -r requirements.txt
````

5. Running app

````sh
python app.py
````

## Usage

### Configuration

The parameters to be configured are found in the `config.py` file. This file has information on how to connect to the database, when deploying the web admin on a production server these data must be configured as environment variables. Let's see what it has:

| Parameter     |type   | Description|
|---------------|-------|------------|
|DB             |String |Database Name.|
|HOST           |string |IP or hostname of the server in which is the wep admin. By default is: 0.0.0.0|
|PORT           |string |Port in which is available the wep admin in the server. By default is: 5000   |
|CONNECTION_DB  |string |utl for connection to the database                                          |
