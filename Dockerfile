#
FROM python:3.10

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./src /code/src
COPY ./config /code/config

#
CMD ["uvicorn", "src.main:app","--port", "5000", "--host", "0.0.0.0"]