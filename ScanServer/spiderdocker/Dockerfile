FROM python:3.7-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk add --no-cache curl tcpdump

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /opt/spider

ENTRYPOINT  
