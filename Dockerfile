FROM python:3.11 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.11

WORKDIR /tripster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONPATH=/tripster/src/app

COPY --from=requirements-stage /tmp/requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

RUN apt-get update && apt-get -y dist-upgrade

RUN apt install -y netcat-openbsd

COPY ./entrypoint.sh /tripster/entrypoint.sh

RUN chmod +x /tripster/entrypoint.sh

COPY ./ /tripster


ENTRYPOINT ["sh", "/tripster/entrypoint.sh"]
