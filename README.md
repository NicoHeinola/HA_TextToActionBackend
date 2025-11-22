# Home Assistant Text to Action Backend

A FastAPI backend that converts user text input to Home Assistant actions using LLM models.

## Setup (Local)

### Prerequisites

- Python 3.10 or higher
- CUDA 12.2 (for GPU support with llama-cpp-python)
- pip and virtualenv

### Installation Steps

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Installing `llama-cpp-python` with CUDA support requires:

   - CUDA Toolkit 12.2 installed and in your PATH
   - cuDNN libraries available

   If you need to build with CUDA support explicitly:

   ```bash
   CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install --force-reinstall llama-cpp-python
   ```

3. Run database migrations:

   ```bash
   alembic upgrade head
   ```

4. Run seeders:

   ```bash
   python run_seeders.py
   ```

5. Start the server:

   ```bash
   python main.py
   ```

   The server will be available at `http://localhost:8000`

## Setup (Docker)

To run with Docker instead:

```bash
docker compose up --build
```

## Database

### Migrations

Run database migrations:

```bash
alembic upgrade head
```

### Rollback

To rollback the database to the previous migration:

```bash
alembic downgrade -1
```

You can specify a particular revision by replacing `-1` with the desired revision identifier.
