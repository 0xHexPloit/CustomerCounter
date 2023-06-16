FROM python:3.9.10

RUN mkdir /app
COPY pyproject.toml /app
COPY README.md /app/README.md
COPY config.yaml /app/config.yaml
COPY main.py /app/main.py
COPY /customercounter /app/customercounter

WORKDIR /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

ENV PYTHONPATH=${PYTHONPATH}:${PWD}


ENTRYPOINT ["python3", "main.py"]
