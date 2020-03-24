FROM alpine

COPY requirements.txt .
COPY games.csv .
COPY interface.py .

RUN apk update \
    && apk --no-cache --update add build-base
RUN apk add python3
RUN apk add python3-dev
RUN apk add libc-dev
RUN pip3 install --no-cache-dir --upgrade pip

RUN apk add less
RUN export PAGER=less

RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip

RUN pip install -r requirements.txt

HEALTHCHECK CMD curl -fsSL "http://$(hostname --ip-address):9200/_cat/health?h=status" | grep -E '^green'

ENTRYPOINT ["python"]
CMD ["interface.py"]
