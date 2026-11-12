from airflow.models import DagBag

from ingest.paths import DAGS_DIR


def test_dag_loads_and_runs_download_then_load_then_dbt():
    bag = DagBag(dag_folder=str(DAGS_DIR))

    assert bag.import_errors == {}
    dag = bag.dags["medicare_warehouse"]
    assert [t.task_id for t in dag.topological_sort()] == ["download", "load_raw", "dbt_build"]
