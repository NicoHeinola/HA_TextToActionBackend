# Stage 1: Python Installation
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04 AS python-stage

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Python 3.10 and build essentials in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    curl \
    build-essential \
    g++ \
    cmake \
    git \
    pkg-config \
    ninja-build \
    libopenblas-dev \
    libomp-dev \
    libssl-dev \
    libgomp1 \
    libbz2-dev \
    liblzma-dev \
    ca-certificates \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3.10-venv \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Install pip and upgrade tools
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 \
    && python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel scikit-build-core

# Stage 2: Build and Dependencies
FROM python-stage AS builder

ARG CUDA_ARCH=75
ENV CUDA_ARCHITECTURES=${CUDA_ARCH} CC=gcc CXX=g++

WORKDIR /app
COPY requirements.txt .

# Stage 2a: Install Python dependencies (excluding llama-cpp-python)
FROM builder AS python-deps

RUN grep -v '^llama-cpp-python' requirements.txt | python3 -m pip install --no-cache-dir -r /dev/stdin

# Stage 2b: Build llama-cpp-python with CUDA support
FROM python-deps AS llama-builder

ARG CUDA_ARCH=75
ENV CUDA_ARCHITECTURES=${CUDA_ARCH} \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH \
    LDFLAGS="-L/usr/local/cuda/lib64 -lcuda"

RUN LLAMA_VERSION=$(sed -n 's/^llama-cpp-python==\([0-9.]*\)$/\1/p' requirements.txt) && \
    CMAKE_ARGS="-DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCH}" FORCE_CMAKE=1 \
    python3 -m pip install --no-cache-dir --force-reinstall --verbose "llama-cpp-python==${LLAMA_VERSION}"

# Final Stage - Runtime only
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-distutils \
    libgomp1 \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Copy Python packages from llama-builder (final build stage)
COPY --from=llama-builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=llama-builder /usr/local/bin /usr/local/bin
COPY . .

CMD ["python3", "main.py"]
