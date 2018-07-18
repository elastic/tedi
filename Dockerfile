FROM python:3.6
RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update
RUN apt-get -y install docker-ce
COPY . /opt/tedi
WORKDIR /opt/tedi
RUN python setup.py install
WORKDIR /mnt
ENTRYPOINT ["/usr/local/bin/tedi"]
