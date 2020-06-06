# Python 3.8 Release
FROM python:3.8.1-alpine as development

# Maintainer Information
LABEL maintainer="Giovanni Armane <giovanniarmane@gmail.com>"
LABEL license="MIT"

# Set environment variables
ENV PYTHON_VERSION=3.8.1 \
  APP_PATH=/home/python/app \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH=/home/python/.local/lib/python3.8/site-packages:/usr/local/bin:/home/python:/home/python/app/bin:$PATH

# Install and configure dependencies
RUN apk add --no-cache build-base libressl-dev musl-dev libffi-dev postgresql-dev
RUN pip install --no-cache-dir poetry

# Configure user, groups and working directory for application
RUN adduser -u 1000 -D python && \
  mkdir -p /home/python/app

# Set workdir
WORKDIR /home/python/app

# Copy project file and pre-install
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Expose ports
EXPOSE 5000

# Declare volumes
VOLUME [ "/home/python/app" ]

# Run the app
CMD ["ash"]
