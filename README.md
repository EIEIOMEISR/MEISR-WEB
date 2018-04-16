# MEISR-Web
MEISR website and api. Allows users to complete the MEISR online and view scores.

# steps to get running

1. create a virtual env
2. pip install -r requirements.txt
3. django setup
  * $ python manage.py python migrate
  * $ python manage.py createsuperuser
  * $ python manage.py runserver
4. edit the admin site
5. api endpoints:
  * /api/questions (GET)
  * /api/answers (GET POST)
  * /api/answers/\<question id\> (GET PUT PATCH) {"question": "", "rating":""}
  * /api/scores (GET POST)
6. auth endpoints:
  * /api/rest-auth/registration/ (POST) {"username": "", "password1": "", "password2": "", "email": "", "birth_date": "YYYY-MM-DD"}
  * /api/rest-auth/login/ (POST) {"username": "", "password": ""}
  * /api/rest-auth/logout/ (POST) {"token": ""}
