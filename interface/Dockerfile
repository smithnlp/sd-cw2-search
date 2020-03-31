FROM alpine

# add a custom label to make it easy to delete the images programatically
LABEL sdproto="true"

# get all the necessary files
COPY requirements.txt .
COPY games.csv .
COPY interface.py .

# updates and installs
RUN apk update \
    && apk --no-cache --update add build-base
RUN apk add python3
RUN apk add python3-dev
RUN apk add libc-dev
RUN pip3 install --no-cache-dir --upgrade pip

# we need less for results presentation but it's not included in alpine linux
RUN apk add less
RUN export PAGER=less

RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip

RUN pip install -r requirements.txt

HEALTHCHECK CMD curl -fsSL "http://$(hostname --ip-address):9200/_cat/health?h=status" | grep -E '^green'

# open directly into python, running the interface program
ENTRYPOINT ["python"]
CMD ["interface.py"]
