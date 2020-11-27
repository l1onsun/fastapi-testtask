FROM python3.8-slim

ENV WORKDIR=/app

COPY . $WORKDIR
WORKDIR $WORKDIR

# RUN pip install -r requirements.txt
# RUN pip install --pre -r requirements_pre.txt