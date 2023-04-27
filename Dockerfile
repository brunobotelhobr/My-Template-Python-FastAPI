FROM python:3.11-alpine

# Update the system
RUN apk update && apk upgrade
# Create User
RUN adduser -D -h /code -s /bin/bash api 

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade wheel
RUN pip install --upgrade poetry

# Install the package
WORKDIR /code
COPY src src
COPY pyproject.toml /code/pyproject.toml
COPY README.md /code/README.md

# Install the packages
# Disable virtualenvs creation
RUN poetry config virtualenvs.create false
RUN poetry install --without dev,docs

# Adjust Permissions
RUN chown -R api:api /code/*

#Enable Api User
USER api

HEALTHCHECK --interval=30s --timeout=3s \
    CMD python /code/src/api/main.py version || exit 1

EXPOSE 8000

# Define the entrypoint
ENTRYPOINT ["python", "/code/src/api/main.py"]