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

RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/interface.py"]
