FROM python:3.12-slim AS builder

WORKDIR /app

# Install system build tools and dependencies needed to compile wheels (llama_cpp_python, numpy, etc.)
COPY requirements.txt .

# Install OS-level build dependencies, upgrade pip and tooling, then install Python deps
ENV CC=gcc CXX=g++
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
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
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel scikit-build-core \
    && pip install --no-cache-dir -r requirements.txt

FROM builder AS final

WORKDIR /app

# Copy application code
COPY . .

# Default command
CMD ["python", "main.py"]
