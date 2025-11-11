# MovieBrowser2 Backend

A simple backend for managing and browsing shows/movies.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run database migrations:

   ```bash
   alembic upgrade head
   ```

3. Run seeders

   ```bash
   python run_seeders.py
   ```

4. Start the server:
   ```bash
   python main.py
   ```

## Rollback

To rollback the database to the previous migration, run:

```bash
alembic downgrade -1
```

You can specify a particular revision by replacing `-1` with the desired revision identifier.
