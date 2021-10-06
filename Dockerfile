# https://github.com/docker-library/python/blob/master/3.9/alpine3.14/Dockerfile
#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:3.9.7-slim
	
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/app

COPY src src/

CMD ["/bin/sh", "-c", "while sleep 1000; do :; done"]