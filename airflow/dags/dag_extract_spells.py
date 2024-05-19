from datetime import timedelta
import json

from airflow.models.dag import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.decorators import task
from airflow.operators.bash import BashOperator
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
    start_dag = DummyOperator(task_id='start_dag')
    extract_task = DockerOperator(
        task_id='extract_spells',
        image='roqueando/spells:stable',
        container_name='spells',
        docker_url="unix://var/run/docker.sock",
        api_version='auto',
        xcom_all=True,
        auto_remove=True,
        command="extract.main",
        network_mode='dungeonsnpipes_default'
    )
    transform_test = DockerOperator(
        task_id='transform_spells',
        image='roqueando/spells:stable',
        container_name='spells',
        docker_url="unix://var/run/docker.sock",
        api_version='auto',
        command="transform.main",
        auto_remove=True,
        network_mode='dungeonsnpipes_default'
    )

    start_dag >> extract_task >> transform_test
