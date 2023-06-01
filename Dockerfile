FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED=1
WORKDIR /ChatGPTBlogWebApp
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . .

CMD [ "python", "manage.py", "runserver" ]