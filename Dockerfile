FROM python:3.6-alpine

MAINTAINER andrew.jackson@bl.uk

COPY docuharv /docuharv

WORKDIR /docuharv

RUN apk add --update build-base libffi libffi-dev openssl openssl-dev git libxml2 libxml2-dev libxslt libxslt-dev && \
#    python setup.py install && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-base libffi-dev openssl-dev git

EXPOSE 6800

CMD scrapy crawl bob
