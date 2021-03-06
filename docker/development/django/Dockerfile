FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client

# Requirements are installed here to ensure they will be cached.
COPY ./Pipfile .
RUN pip install pipenv && pipenv install -d --skip-lock --system

#COPY ./docker/production/django/entrypoint /entrypoint
#RUN sed -i 's/\r//' /entrypoint
#RUN chmod +x /entrypoint

COPY . .
#RUN sed -i 's/\r//' /docker/development/start
#RUN chmod +x /start

# COPY ./docker/development/django/celery/worker/start /start-celeryworker
# RUN sed -i 's/\r//' /start-celeryworker
# RUN chmod +x /start-celeryworker

# COPY ./docker/development/django/celery/beat/start /start-celerybeat
# RUN sed -i 's/\r//' /start-celerybeat
# RUN chmod +x /start-celerybeat

#COPY ./compose/development/django/celery/flower/start /start-flower
#RUN sed -i 's/\r//' /start-flower
#RUN chmod +x /start-flower

#RUN sed -i 's/\r//' start.sh
#RUN chmod +x ./docker/development/django/start.sh
#ENTRYPOINT ['./docker/development/django/start.sh']
CMD ["sh","docker/local/django/start.sh"]
