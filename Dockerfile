FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED=1
WORKDIR /ChatGPTBlogWebAppRender
COPY ./requirements.txt /requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home ChatGPTBlogWebAppRender && \
    mkdir -p /library && \
    mkdir -p /static && \
    chmod -R 755 /library  && \
    chmod -R 755 /static 

ENV PATH="/scripts:/py/bin:$PATH"

USER ChatGPTBlogWebAppRender

CMD ["run.sh"]