FROM ubuntu:16.04
FROM ubuntu:16.04
EXPOSE 5001 8883 8888 8080
ENV PATH /opt/miniconda/bin:$PATH
ARG CONDA_VERSION=4.9.2
ARG PYTHON_VERSION=3.7
ARG AZUREML_SDK_VERSION=1.27.0
ARG INFERENCE_SCHEMA_VERSION=1.1.0

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/miniconda/bin:$PATH
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 && \
    apt-get install -y fuse && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    apt install net-tools -y &&\
    apt install docker -y &&\
    apt install docker-compose -y &&\
    apt-get install pass gnupg2 -y &&\
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home dockeruser
WORKDIR /home/dockeruser
USER dockeruser

# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#     /bin/bash ~/miniconda.sh -b -p ~/miniconda && \
#     rm ~/miniconda.sh && \
#     ~/miniconda/bin/conda clean -tipsy
# ENV PATH="/home/dockeruser/miniconda/bin/:${PATH}"
# RUN conda update -n base -c defaults conda
# RUN conda install -y conda=${CONDA_VERSION} python=${PYTHON_VERSION} && \
#     pip install azureml-defaults==${AZUREML_SDK_VERSION} inference-schema==${INFERENCE_SCHEMA_VERSION} &&\
#     conda clean -aqy && \
#     rm -rf ~/miniconda/pkgs && \
#     find ~/miniconda/ -type d -name __pycache__ -prune -exec rm -rf {} \;

ADD newArchive.tar.gz /
