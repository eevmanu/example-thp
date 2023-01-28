<!-- omit in toc -->
# <p align=center> example - take home project </p>

<!-- omit in toc -->
## Table of contents

- [tech stack](#tech-stack)
- [app structure](#app-structure)
- [unzip](#unzip)
- [build](#build)
- [run](#run)
- [testing](#testing)
  - [local](#local)
- [future work](#future-work)

## tech stack

☝ [Table of contents](#table-of-contents)

- Python 3.10
- FastAPI + uvicorn
- PostgreSQL (psycopg2)
- Pydantic
- SQLAlchemy
- Alembic
- Pytest
- GCP

<p align=right><small><a href=#table-of-contents>☝️ Table of contents</a></small></p>

## app structure

☝ [Table of contents](#table-of-contents)

```txt
.
├── docker-compose.yml    ➡️ config file for docker compose to manage all services related
└── src                   ➡️ root package of whole application
    ├── dockerfile        ➡️ docker declaration file to manage only `app` service
    ├── requirements.in   ➡️ package requirements for the app without dependencies
    ├── requirements.txt  ➡️ package requirements for the app with dependencies
    ├── settings.py       ➡️ the settings required for whole app
    ├── prestart.py       ➡️ initial script to test connection from application ORM to database
    ├── initial_data.py   ➡️ initial script to populate random generate data
    ├── db.py             ➡️ module to setup sessions to manage communication with database
    ├── models.py         ➡️ module to map entities in database with objects in the application
    ├── schema.py         ➡️ module which manage structures to receive and return responses on the API endpoitns
    ├── deps.py           ➡️ module to handle dependency injection of database sessions
    ├── crud.py           ➡️ module to handle direct operations on database entities
    ├── endpoitns.py      ➡️ module which manage business logic to execute when API endpoints are called
    ├── main.py           ➡️ module which contains the initial point to run the app
    └── tests/            ➡️ package which contains tests on the app
```
<p align=right><small><a href=#table-of-contents>☝️ Table of contents</a></small></p>

## unzip

<!-- git clone git@github.com:eevmanu/example-thp.git -->

## build

☝ [Table of contents](#table-of-contents)

<!-- Local with docker

```sh
$ docker build -f dockerfile -t example_thp_img .
# $ docker build -f dockerfile -t example_thp_img:0.0.1 .
# $ docker build -f dockerfile -t example_thp_img:0.0.1 --no-cache .
``` -->

requirements:
- `docker`
- `compose` as plugin

with compose

```sh
$ docker compose build
```

to generate a new migration

checklist:
- `app` service is live
- connected to `db` service

```sh
# $ docker exec app alembic -c /code/src/alembic.ini revision --autogenerate -m "< migration title >"

# e.g.:
$ docker exec app alembic -c /code/src/alembic.ini revision --autogenerate -m "first migration"
```

if no data, in case alembic raise an error because a **revision** is not found, recreate volume

```sh
$ docker compose stop
$ docker compoose rm -f
$ docker volume prune
```

to explicitly apply migrations

```sh
$ docker exec app alembic -c /code/alembic.ini upgrade head

# TODO when alembic is managed by poetry
# $ docker exec app poetry run alembic -c /code/alembic.ini upgrade head
```

<p align=right><small><a href=#table-of-contents>☝️ Table of contents</a></small></p>

## run

☝ [Table of contents](#table-of-contents)

<!-- Local with **only** docker

```sh
$ docker run -d --name example_thp_cont -p 80:80 --rm example_thp_img
```

to stop

```sh
$ docker stop example_thp_cont
``` -->

with **compose**

```sh
# $ docker compose up
$ docker compose up -d
```

go to [http://localhost/docs](http://127.0.0.1/docs)

![docs image](https://i.imgur.com/1hnBHz6.png)

to stop

```sh
$ docker compose stop
```

to remove / delete

```sh
$ docker compose rm
# $ docker compose rm -f
# $ docker compose rm -f app
```

to watch `app` logs

```sh
$ docker compose logs -t -f --tail 20 app
```

<p align=right><small><a href=#table-of-contents>☝️ Table of contents</a></small></p>

## testing

### local

☝ [Table of contents](#table-of-contents)

to run tests

```sh
$ docker exec app pytest src/tests
# $ docker exec app pytest -s src/tests/test_users.py::test_search_user_by_email
# $ docker exec app pytest -s src/tests/test_users.py
# $ docker exec app pytest --cov=app --cov-report=term-missing src/tests "${@}"
```

<!-- ```sh
$ docker compose run tests
``` -->

<p align=right><small><a href=#table-of-contents>☝️ Table of contents</a></small></p>

## future work

☝ [Table of contents](#table-of-contents)

simple ones
- create a `makefile` to handle the commands easily
- create a minimal archicture diagram to understand how services interact
- manage python virtual environment with [poetry](https://github.com/python-poetry/poetry) and integrate code quality tools into the `pyproject.toml`
  - code quality tools: [mypy](https://github.com/python/mypy), [ruff](https://github.com/charliermarsh/ruff), [flake8](https://github.com/PyCQA/flake8), [pylint](https://github.com/PyCQA/pylint), [black](https://github.com/psf/black), [isort](https://github.com/PyCQA/isort), [bandit](https://github.com/PyCQA/bandit), [safety](https://github.com/pyupio/safety), [pre-commit](https://github.com/pre-commit/pre-commit)
- deploy as serverless function and test with a disposable serverless database
- on `dockerfile`, run everything as `non-root` for security improvements
- setup `traefik` to handle `https` requests
- activate code coverage tool for tests
- if required for cache purposes, change `search` endpoints from `POST` to `GET`

more thought process
- in case data is sensible (e.g.: healthcare related), take advantage of a common standarization for naming convetion in the industry (FHIR HL7)
  <!-- Fast Healthcare Interoperability Resources  -->
- use OpenID / OAuth for authentication / authorization / security purposes
  - use container security best practices
  - use container scanning tools (like: [trivy](https://github.com/aquasecurity/trivy), [snyk](https://github.com/snyk/cli) or [grype](https://github.com/anchore/grype))
    <!-- - https://docs.docker.com/engine/scan/ -->
  - use dockerfile best practices
  - use [API security checklist](https://github.com/shieldfy/API-Security-Checklist)
- apply **observability** principles (logs, traces, metrics)
  - lever [Google Cloud's operations suite](https://cloud.google.com/products/operations)

    <img src="https://i.imgur.com/LV3XHPF.png" alt="Google Cloud's operations suite" height="200"/>
    <!-- https://cloud.google.com/blog/products/management-tools/observability-on-google-cloud -->
- improve application design for better scalability via concurrency
  - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="logo python" height="18"/> async/await
  - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original-wordmark.svg" alt="logo go" height="18"/> goroutines/channels
- database election
  - if high load, consider a distributed alternative (e.g.: cockroachdb) + replication + sharding (optional)
  - if read-heavy, denormalize + sqlite (lower latency) + WAL + apply CQRS (optional)
  - if write-heavy, normalize + apply CQRS (optional)
  - analyze the consistency level required based on the business requirements for the data
- microservice architecture based on `ownership` (and other constraints)
  - if each action need to scale independently ‣ CQRS + `choreography` style
    - using event-driven architecture via `messaging bus` (e.g.: [Cloud Pub/Sub](https://cloud.google.com/pubsub) + [Cloud Functions](https://cloud.google.com/functions))
  - if team is small enough to have whole ownership ‣ `orchestration` style
    - using workflow architecture (e.g.: [Cloud Workflows](https://cloud.google.com/workflows))
- stress testing - to simulate high load, using tools like [wrk](https://github.com/wg/wrk) or [vegeta](https://github.com/tsenart/vegeta)
- latency SLA (based on hearing pod `communication protocol`)
  - consider the tradeoffs with accuracy
  - any requirement of `p99` for `x` miliseconds
  <!-- - what is the max amount of time client you wait until expect the sound profile algorithm to make effect -->
    <!-- - this is the input for the min consistency level required -->
- availability SLA
  - consider a more eventual consistency approach if data is not real-time human-critical
- bandwidth limit (based on hearing pod `communication protocol`)
  - `mqtt` (e.g.: [Cloud IoT Core](https://cloud.google.com/iot-core))
- optimization for energy consumption (based on battery capacity)
- distributed systems
  - fault-tolerant
    <!-- - prefer loose coupling componentes instead of tightly coupling -->
  - realibility
  - testing
  <!-- testcontainers -->

<!-- TODO
move
from Metadata-managed SSH connections (not recommended)
to OS Login-managed SSH connections (recommended)
https://cloud.google.com/compute/docs/instances/connecting-advanced#provide-key
-->
