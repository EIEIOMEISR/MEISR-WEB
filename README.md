# MEISR-Web
Backend for MEISR App

# steps to get running

1. install virtualenvwrapper and make a new venv
2. run 'pip install -r requirements.txt'
3. go into /meisr and setup the site
  * $ python manage.py makemigrations; python migrate
  * $ python manage.py createsuperuser
  * $ python manage.py runserver
4. edit the admin site as you wish
5. api endpoints:
  * /api/questions
  * /api/answers
  * /api/update
