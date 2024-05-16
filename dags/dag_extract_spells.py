from datetime import timedelta
from airflow.models.dag import DAG

from airflow.operators.python import PythonOperator

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
    extract_spell = PythonOperator(task_id="extract_spell", bash_command="date")
    task2 = BashOperator(task_id="sleep", bash_command="sleep 5")
    task1 >> [task2]
