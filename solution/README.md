# DI US Shopping - Checkout System

## Prerequisites
- Install [Python](https://www.python.org/downloads/) (make sure you install a version that is compatible with this project, this can be found in the [pyproject file](pyproject.toml))
- Install [Poetry](https://python-poetry.org/docs/) to manage your virtual environment.
- Install [Make](https://www.gnu.org/software/make/) to take advantage of shortcuts for running tests.

## Installing Requirements
- Create your virtual environment by running the following command in a terminal:
```
python -m venv .venv
```
- Activate the virtual environment:
```
source .venv/bin/activate
```
- Install the requirements using poetry
```
poetry install
```
- Check requirements have installed successfully by running:
```
poetry show
```
All installed requirements will be returned in blue. If any are not installed they will appear as red. Try running `poetry install` again if this happens, or installing the missing packages individually.

## Running the App

## Running Tests
- To run all tests, run:
```
make test
```
- To run all tests and receive a coverage report, run:
```
make coverage
```