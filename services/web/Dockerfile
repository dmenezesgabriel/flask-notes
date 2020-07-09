# Pull official base image
FROM python:3.8.1-slim-buster
# Set work directory
WORKDIR /usr/src/app
# Set envrionment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONBUFFERED 1
# Install system dependencies
RUN apt-get update && apt-get install -y netcat
# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
# Copy project
COPY . /usr/src/app/
# Run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]