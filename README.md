-install python
-create a new project for python-behave
-create and initialize the virtual environment for the project:
  python3 -m venv ENVIRONMENT
-activate the env:
  source ENVIRONMENT/bin/activate
-execute the requirements.txt file to get the packages required installed:
  pip install -r requirements.txt

-run tests with:
  behave features/alojamiento.feature
  behave features/vuelos.feature
