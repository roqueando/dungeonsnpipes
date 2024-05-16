FROM python:3.12 as builder

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

FROM builder as poetry-builder
RUN python3 -m venv $POETRY_VENV \
      && $POETRY_VENV/bin/pip install -U pip setuptools \
      && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM poetry-builder as pipeline

COPY --from=poetry-builder ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry check
RUN poetry install --no-interaction --no-cache

COPY . /app

ENTRYPOINT ["poetry", "run", "python", "-m", "dungeonsnpipes.main"]
