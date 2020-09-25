FROM node:10-stretch-slim as client-builder

WORKDIR /app
COPY ./package.json /app
RUN npm install && npm cache clean --force
COPY . /app
RUN npm run build

# Python build stage
FROM python:3.8-slim-buster as production

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # curl for heroku
  && apt-get install -y curl \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/release /app/release
RUN sed -i 's/\r$//g' /app/release
RUN chmod +x /app/release
RUN chown django /app/release

COPY --from=client-builder --chown=django:django /app /app

WORKDIR /app

USER django
