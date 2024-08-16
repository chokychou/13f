FROM python:3.11-slim

RUN mkdir -p /src/data_import_jobs
RUN mkdir -p /src/proto

WORKDIR /

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
    protobuf-compiler

# Copy requirements.txt
COPY /requirements.txt /
RUN pip install -r requirements.txt

# Copy source files
COPY /src/data_import_jobs/.  /src/data_import_jobs
COPY /src/proto/.  /src/proto

RUN protoc -I=. --proto_path=src/proto sample.proto \
    --python_out=/src/proto/.

# Hacks to avoid python modules not found
COPY /src/data_import_jobs/.  .
RUN mkdir -p /src/daily_import_jobs/src/proto
RUN cp -r /src/proto/.  /src/daily_import_jobs/src/proto/.

CMD ["python3", "-u", "daily_importer.py"]