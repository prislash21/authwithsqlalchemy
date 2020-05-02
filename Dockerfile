FROM python:3

RUN python3 -m pip install --upgrade pip

WORKDIR / app
COPY ./ app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD ["app.py", "-h", "0.0.0.0", "-p", "5000", "-d"]

EXPOSE 5000