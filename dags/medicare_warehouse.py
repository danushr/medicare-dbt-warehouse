import os
from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PROJECT_DIR = os.environ["MEDICARE_PROJECT_DIR"]

with DAG(
    dag_id="medicare_warehouse",
    description="Pick up any newly published CMS year, reload the raw table and rebuild the warehouse.",
    schedule="@monthly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
):
    download = BashOperator(task_id="download", bash_command="python -m ingest.download", cwd=PROJECT_DIR)
    load_raw = BashOperator(task_id="load_raw", bash_command="python -m ingest.load_raw", cwd=PROJECT_DIR)
    dbt_build = BashOperator(task_id="dbt_build", bash_command="dbt deps && dbt build", cwd=PROJECT_DIR)

    download >> load_raw >> dbt_build
