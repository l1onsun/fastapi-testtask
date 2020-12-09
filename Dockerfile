FROM python:3.8-slim

ENV IN_DOCKER=True
ENV WORKDIR=/app

COPY . $WORKDIR
WORKDIR $WORKDIR

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# CMD ["sleep", "300"] # overrideed by docker-compose
