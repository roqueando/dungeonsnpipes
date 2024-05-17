import sys
import os
print(sys.path)
sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

from datetime import timedelta
from airflow.models.dag import DAG

from airflow.operators.python import PythonOperator
from airflow.decorators import task

import mod.base as api_extractor
import mod.transform as transformer

@task(task_id="extract_batch_spells")
def extract_batch_spells():
    print("extracting spells...")
    spells = api_extractor.get_spells_from_api()
    return transformer.turn_into_batches(spells)

@task(task_id="transform_batches")
def transform_batches(batches):
    print("transforming...")
    for batch in batches:
        proc = Process(target=execute_transformer, args=(batch,))
        proc.start()

def execute_transformer(batch: transformer.SpellBatch):
    return transformer.Transformer(batch=batch.spells) \
            .apply(transformer.transform_description) \
            .apply(transformer.transform_components) \
            .apply(transformer.transform_range) \
            .apply(transformer.transform_damage)

with DAG(
    "spells",
    default_args={
        "depends_on_past": False,
        "email": ["vitor.roquep@gmail.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1)
    },
    description="The Spells Ingestion DAG"
) as dag:
    spells = extract_batch_spells()
    batches = transform_batches(spells)
