FROM ubuntu:18.04

# Copy project
COPY . /aicsimageio

# General upgrades and requirements
RUN apt-get update && apt-get upgrade -y

# Get software props
RUN apt-get install -y \
    software-properties-common

# Add additional apt repository
RUN add-apt-repository universe

# Get python3.7 and pip
RUN apt-get update && apt-get install -y \
    python3.7 \
    python3.7-dev \
    python3-pip \
    git

# Upgrade pip and force it to use python3.7
RUN python3.7 -m pip install --upgrade pip

# Set python3.7 to default python
RUN ln -sf /usr/bin/python3.7 /usr/bin/python
RUN ln -sf /usr/bin/python3.7 /usr/bin/python3

# Set workdir
WORKDIR aicsimageio/

# Install package
RUN pip install prefect
RUN pip install dask[bag]==2.12.0
RUN pip install distributed==2.12.0
RUN pip install bokeh
RUN pip install dask-cloudprovider==0.1.1
RUN pip install aiobotocore[boto3]==0.12.0
RUN pip install git+https://github.com/intake/filesystem_spec.git
RUN pip install .
