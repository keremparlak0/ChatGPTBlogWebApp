FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED=1
WORKDIR /ChatGPTBlogWebApp
COPY ./requirements.txt /requirements.txt


RUN pip install requirements.txt && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home ChatGPTBlogWebApp

ENV PATH="/py/bin:$PATH"

USER ChatGPTBlogWebApp

CMD ["run.sh"]