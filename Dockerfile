FROM python:3.9.0

RUN mkdir /app
COPY /customercounter /app/customercounter
COPY main.py /app/main.py
COPY config.yaml /app/config.yaml
COPY pyproject.toml /app
COPY README.md /app/README.md

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}


RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev



ENTRYPOINT ["python3", "main.py"]