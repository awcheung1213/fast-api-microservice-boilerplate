#---------------RELEASE STAGE-----------------------

FROM python:latest as release

# Set up virtualenv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /opt/fast-api-microservice-boilerplate

# Install pip and poetry
RUN pip install --upgrade pip && pip install poetry

# Copy all files
COPY . /opt/fast-api-microservice-boilerplate

# Install dependencies
RUN pip install -r requirements.txt

#---------------TESTING STAGE------------------------

FROM release as testing

# Copy test files
COPY ./tests /opt/fast-api-microservice-boilerplate/tests

# Set PYTHONPATH for module access
ENV PYTHONPATH="${PYTHONPATH}:/opt/fast-api-microservice-boilerplate"

# Set working directory
WORKDIR /opt/fast-api-microservice-boilerplate