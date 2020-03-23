FROM frolvlad/alpine-python3
COPY requirements.txt /app
COPY games.csv /app
COPY interface.py /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/interface.py"]
