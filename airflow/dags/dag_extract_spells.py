import sys
import os

from datetime import timedelta
from airflow.models.dag import DAG

from airflow.operators.docker_operator import DockerOperator
from airflow.operators.dummy_operator import DummyOperator

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
    start_dag = DummyOperator(
        task_id='start_dag'
    )
    extract_task = DockerOperator(
        task_id='extract_spells',
        image='dungeonsnpipes-spells-extract:latest',
        container_name='spells-extract',
        docker_url="unix://var/run/docker.sock",
        api_version='auto',
        auto_remove=True,
        network_mode='bridge'
    )
    start_dag >> extract_task
    # spells = extract_batch_spells()
    # batches = transform_batches(spells)
