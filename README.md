# Forecast Planner API

This project is a a weather app with a planning feature that advises users on what to wear. It is built with Python. It uses FastAPI for the web framework, SQLAlchemy for the ORM, and python-jose for handling JWT tokens.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Python 3.11+ installed on your machine. You can download it from [here](https://www.python.org/downloads/).

### Installing

1\. Clone the repository

```bash

git clone https://github.com/wachira-g/forecastplanner.git

```

2\. Change the directory

```bash

cd ForecastPlanner

```
2\. Create a virtual environment and activate it
```bash

python3.11 venv venv
source venv/bin/activate

```

3\. Install the requirements

```bash

pip install -r requirements.txt

```

## Usage

To run the server, execute the following command:

```bash

uvicorn main:app --reload

```

## Features

- User Registration

- User Authentication

- Token Refresh

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used

- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL Toolkit and ORM

- []() - Python library to encode and decode JWT tokens

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/...) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used

- Inspiration

- etc
