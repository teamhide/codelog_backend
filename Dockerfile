FROM python:3.7.5
MAINTAINER hide <padocon@naver.com>

RUN pip3 install pipenv
COPY . home
WORKDIR /home
RUN pipenv install --system

CMD gunicorn -w4 "apps:create_app()" -b 0.0.0.0:8000 --access-logfile=- --error-logfile=- --capture-output