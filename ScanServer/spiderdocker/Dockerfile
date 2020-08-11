FROM python:3.7-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk add --no-cache curl tcpdump python3-dev gcc libc-dev

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /opt/spider

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod u+x /docker-entrypoint.sh 

ENTRYPOINT ./docker-entrypoint.sh

# docker run -it --env-file=.env [image] 
