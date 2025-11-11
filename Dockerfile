FROM python:3.12-slim AS builder

WORKDIR /app

# Build wheels for Python dependencies in a separate stage to keep the final image small
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM builder AS final

WORKDIR /app

# Install ffmpeg so pydub/ffprobe are available at runtime
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Default command
CMD ["python", "main.py"]
