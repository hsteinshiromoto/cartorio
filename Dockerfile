# ---
# Build arguments
# ---
ARG DOCKER_PARENT_IMAGE="python:3.10-slim"
FROM $DOCKER_PARENT_IMAGE

# NB: Arguments should come after FROM otherwise they're deleted
ARG BUILD_DATE
ARG PROJECT_NAME
# Silence debconf
ARG DEBIAN_FRONTEND=noninteractive

# ---
# Enviroment variables
# ---
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8
ENV TZ Australia/Sydney
ENV SHELL /bin/bash
ENV HOME /home/$PROJECT_NAME

# Set container time zone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

LABEL org.label-schema.build-date=$BUILD_DATE \
    maintainer="Humberto STEIN SHIROMOTO <h.stein.shiromoto@gmail.com>"

# ---
# Set up the necessary Debian packages
# ---
RUN apt-get update && \
    apt-get install -y build-essential \
    curl \
    git \
    gnupg2 \
    make \
    pandoc \
    sudo \
    vim \
    wget \
    apt-get clean && \
    apt-get --purge remove -y .\*-doc$ && \
    apt-get clean -y

RUN mkdir -p $HOME

COPY requirements.txt /usr/local/ 
RUN pip install -r /usr/local/requirements.txt