FROM ubuntu:16.04
WORKDIR /usr/lib/
tar -cvzf newArchive.tar.gz /var/lib/docker
COPY newArchive.tar.gz docker/
