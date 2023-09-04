FROM python:3.9.5

USER root

# Update system and install ffmpeg
RUN apt update && \
    apt install --no-install-recommends -y libgl1-mesa-glx && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Create working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# # Copy contents
COPY requirements.txt /usr/src/app/requirements.txt

# # Install packages
RUN pip install --no-cache -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com/pypi

COPY . /usr/src/app  

