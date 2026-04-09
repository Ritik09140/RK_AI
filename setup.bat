@echo off
echo [*] Initializing Django project for RK AI...
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install django djangorestframework openai gtts python-dotenv
django-admin startproject rk_ai_project .
python manage.py startapp assistant
python manage.py startapp csc_services
echo [*] Project setup complete!
