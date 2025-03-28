-install python
-install allure
-create a new project for python-behave in the IDE
-create and initialize the virtual environment for the project:
  python3 -m venv ENVIRONMENT
-activate the env:
  source ENVIRONMENT/bin/activate
-execute the requirements.txt file to get the packages required installed:
  pip install -r requirements.txt

-run tests with:
  behave features/alojamiento.feature
  behave features/vuelos.feature

  for allure reports:
  behave features/alojamiento.feature -f allure_behave.formatter:AllureFormatter -o allure-results -v
  behave features/vuelos.feature -f allure_behave.formatter:AllureFormatter -o allure-results -v

  to generate alure reports:
  allure generate allure-results -o allure-report --clean  