# Lab Appoinment
A django application for making virtual lab appoinments.

# Commands
- `pip install virtualenv` (Run Once)
    - Installing virtual environment.
- `python -m venv venv` (Run Once)
    - Creates a virtual environment named `venv` in the project directory.
- `venv\Scripts\activate` (Run on every terminal once)
    - To activate the virtual environment.
- `pip install -r requirements.txt` (Run Once)
    - For installing the project dependencies.
- `python manage.py migrate` (Run on every pull from GitHub)
    - To apply model changes if any.
- `python manage.py loaddata` (Run Once)
    - To load data to `Test` model.
- `python manage.py runserver` (Run everytime)
    - To run the server
