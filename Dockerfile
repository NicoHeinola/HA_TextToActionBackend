# Stage 1: Python Installation
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 AS python-stage

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common curl \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
    python3.10 python3.10-dev python3.10-distutils python3.10-venv \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
    && curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.10 get-pip.py \
    && rm get-pip.py \
    && python3 -m pip install --upgrade pip setuptools wheel scikit-build-core

# Stage 2: Python Requirements
FROM python-stage AS requirements-stage
ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Stage 3: CMake Build
FROM requirements-stage AS cmake-stage
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential g++ cmake git pkg-config ninja-build \
    libopenblas-dev libomp-dev libssl-dev libgomp1 libbz2-dev liblzma-dev \
    ca-certificates cuda-drivers \
    && rm -rf /var/lib/apt/lists/*

ENV CC=gcc CXX=g++

RUN CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 \
    python3 -m pip install --no-cache-dir --force-reinstall --verbose llama-cpp-python

# Final Stage
FROM cmake-stage
WORKDIR /app
COPY . .
CMD ["python3", "main.py"]
