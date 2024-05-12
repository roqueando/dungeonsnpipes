FROM python-3.12-buster

RUN pip install poetry

COPY . . 

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "dungeonsnpipes.main"]
