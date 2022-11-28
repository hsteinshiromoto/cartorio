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
RUN apt update && \
    apt install -y build-essential \
    curl \
    git \
    git-flow \
    gnupg2 \
    make \
    pandoc \
    sudo \
    vim \
    wget

RUN pip install --upgrade pip && pip install pytest sphinx sphinx_rtd_theme myst-parser

RUN mkdir -p $HOME
WORKDIR $HOME