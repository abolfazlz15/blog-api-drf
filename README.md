# API-BLOG
## This project developing with DRF (django rest framework).
## This is a practice project to learn and gain experience.
### some features:
- Compliance with the principles of test writing DRF
- Compliance with the principles of clean coding
- Customize user model
- Dockerized
- use nginx server for static file and media file
- Use JWT and OTP
## Run project :
- In terminal: `https://github.com/abolfazlz15/blog-api-drf.git`
- cd `/blog-api-drf` Where the manage.py is
- In terminal: `python -m venv venv`
- activate your venv: in windows `cd venv\scripts\activate` in linux: `venv/bin/activate`
- Run `pip install -r requirements.txt`
- Run `python manage.py collectstatic`
- Run `python manage.py runserver` to run project.
## Run project with docker :
- In terminal: `https://github.com/abolfazlz15/blog-api-drf.git`
- cd `/blog-api-drf` Where the docker-compose.yaml is
- In terminal: `docker-compose up -d`
- Visit `http://127.0.0.1:8000/`
