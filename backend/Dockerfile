FROM python:3.10 as build-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml  /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
RUN apt-get update \
    && apt-get -y install libpq-dev gcc uvicorn \
    && pip install psycopg2 \
    && pip install nltk \
    && pip install sumy

WORKDIR /app
COPY --from=build-stage /tmp/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

# this line is just for debugging
RUN pwd && ls -la

EXPOSE 8080
CMD ["uvicorn", "--host", "0.0.0.0", "--reload", "--reload-dir", "/app", "api:app"]