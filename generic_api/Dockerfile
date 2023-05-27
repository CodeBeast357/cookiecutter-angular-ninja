FROM python:3.11

RUN apt update
RUN apt install -y postgresql-client
    # postgresql-dev \
    # linux-headers \
    # musl-dev \
    # libffi-dev \
    # jpeg-dev \
    # zlib-dev \
    # postgresql-client
RUN pip install django-ninja


WORKDIR /usr/src
ADD requirements.txt .
RUN pip install -r requirements.txt
COPY . .

WORKDIR /usr/src/generic_api
RUN python /usr/src/generic_api/manage.py collectstatic --no-input
RUN mkdir -p /mnt/data

EXPOSE 8000

CMD python /usr/src/generic_api/manage.py runserver 0.0.0.0:8000
