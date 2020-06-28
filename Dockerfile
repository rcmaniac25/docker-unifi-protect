#
# UniFi Protect Dockerfile
# Copyright (C) 2020 Vinnie Simonetti
# Copyright (C) 2019 James T. Lee
#

FROM ubuntu:18.04

LABEL maintainer="rcmaniac25"
LABEL version="1.12.5"

ARG tz=America/New_York
RUN ln -fs /usr/share/zoneinfo/$tz /etc/localtime

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y gnupg2 software-properties-common sudo curl tzdata \
 && dpkg-reconfigure --frontend noninteractive tzdata \
 && apt-get upgrade -y

RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash - \
 && apt-get install -y nodejs

RUN apt-get install -y postgresql

COPY ubnt-tools-0.1.0.deb /ubnt-tools-0.1.0.deb

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv 97B46B8582C6571E \
 && add-apt-repository 'deb http://apt.ubnt.com bionic main' \
 && apt install -y /ubnt-tools-0.1.0.deb \
 && apt-get install -y unifi-protect \
 && rm /ubnt-tools-0.1.0.deb \
 && mkdir /srv/unifi-protect \
 && chown unifi-protect:unifi-protect /srv/unifi-protect

# Supply simple script to run postgres and unifi-protect
COPY script_setup.py /script_setup.py
COPY init /init
ENTRYPOINT ["/init"]
