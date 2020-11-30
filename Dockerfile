FROM python:3.8

ENV IN_DOCKER=True
ENV WORKDIR=/app

COPY . $WORKDIR
WORKDIR $WORKDIR

#RUN apt-get -y update
#RUN apt-get -y install make
#RUN make upgrade upgrade-dev

RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt

# CMD ['echo', 'abracadabra']
CMD ['make', 'test', 'run-gunicorn']