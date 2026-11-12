"""Stack the yearly CSV files into one raw table, every column kept as text."""
from pathlib import Path

import duckdb


def load(raw_dir: Path, db: Path) -> int:
    db.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db)) as con:
        con.execute("create schema if not exists raw")
        con.execute(
            f"""
            create or replace table raw.inpatient as
            select
                * exclude (filename),
                cast(regexp_extract(filename, 'inpatient_(\\d{{4}})', 1) as integer) as data_year
            from read_csv('{raw_dir}/inpatient_*.csv', all_varchar = true, filename = true)
            """
        )
        return con.execute("select count(*) from raw.inpatient").fetchone()[0]


if __name__ == "__main__":
    from ingest.paths import DB, RAW_DIR

    print(f"loaded {load(RAW_DIR, DB)} rows into raw.inpatient")
