# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

#Settings for Docker project
#FROM python:3.8
#ENV PYTHONUNBUFFERED=1
#ENV PYTHONDONTWRITEBYTECODE 1
#WORKDIR /code
#RUN pip install --upgrade pip
#COPY requirements.txt /code/
#RUN pip install -r requirements.txt

## pull the official base image
#FROM python:3.8
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
## set work directory
#RUN mkdir /code
#WORKDIR /code
#
## install dependencies
#RUN pip install --upgrade pip
#COPY requirements.txt /code/
#RUN pip install -r requirements.txt
#
## copy project
#COPY . /code/
#
#EXPOSE 8000
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
