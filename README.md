# MEISR-Web
Backend for MEISR App

# steps to get running

1. create a new virtual env
2. run 'pip install -r requirements.txt'
3. go into /meisr and setup the site
  * $ python manage.py makemigrations; python migrate
  * $ python manage.py createsuperuser
  * $ python manage.py runserver
4. edit the admin site as you wish
5. api endpoints:
  * /api/questions (GET)
  * /api/answers (GET POST)
  * /api/answers/\<question id\> (GET PUT PATCH) {"question": "", "rating":""}
  * /api/scores (GET POST)
6. auth endpoints:
  * /rest-auth/registration/ (POST) {"username": "", "password1": "", "password2": "", "email": ""}
  * /rest-auth/login/ (POST) {"username": "", "password": ""}
  * /rest-auth/logout/ (POST)
  * /refresh-token/ (POST)
