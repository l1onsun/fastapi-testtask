FROM python:3.8-slim

ARG MAKE=False
ENV WORKDIR=/app

COPY . $WORKDIR
WORKDIR $WORKDIR

RUN apt-get -y update
RUN apt-get -y install make
RUN make install install-dev

# CMD ['echo', 'abracadabra']
CMD ['make', 'test', 'run']