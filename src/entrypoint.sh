#!/bin/bash
# to debug, un-comment line below
# set -euxo pipefail

# --------------------------------------------------------------------------------

# step 1 validate `app` is able to connect to `db` via container networking

echo "DB Connection --- Establishing . . ."

while ! nc -z db 5432; do

    echo "DB Connection -- Failed!"

    sleep 1

    echo "DB Connection -- Retrying . . ."

done

echo "DB Connection --- Successfully Established!"

# --------------------------------------------------------------------------------

# step 2 validate `app` ORM is able to connect to `db`

# PYTHONPATH=$(pwd) python /code/src/prestart.py
python -m src.prestart

# --------------------------------------------------------------------------------

# step 3 validate `db` model is updated, if not, run migrations

if command -v alembic 1>/dev/null 2>&1; then
  # TODO manage a condition to remove all tables when you want a clean start
  # $ PYTHONPATH=$(pwd) python -c "from src.models import Base; from src.db import engine; Base.metadata.drop_all(bind=engine); Base.metadata.create_all(bind=engine)"

  # PYTHONPATH=$(pwd) alembic -c /code/src/alembic.ini upgrade head
  alembic -c /code/src/alembic.ini upgrade head
  # TODO change when using poetry to manage command executing and virtual environment
  # $ PYTHONPATH=$(pwd) ; poetry run alembic -c /code/alembic.ini upgrade head
  # $ poetry run alembic -c /code/alembic.ini upgrade head
else
  echo "no \`alembic\` command"
  exit 1
fi

# --------------------------------------------------------------------------------

# step 4 validate `db` has initial data, if not, insert initial data

# PYTHONPATH=$(pwd) python /code/src/initial_data.py
python -m src.initial_data

# --------------------------------------------------------------------------------

# step 5 up the `app` (or command passed from docker compose file or dockerfile)

exec "$@"
