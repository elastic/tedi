FROM python:3.6

# Add Docker client
RUN apt-get update && \
    apt-get -y install apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get -y install docker-ce && \
    apt-get clean

# Add Tedi
WORKDIR /usr/src/app
COPY setup.* ./
COPY tedi tedi
RUN python setup.py install
WORKDIR /mnt
ENTRYPOINT ["/usr/local/bin/tedi"]
