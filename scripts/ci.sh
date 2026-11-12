#!/bin/sh
set -eu
sample="$MEDICARE_PROJECT_DIR/sample"
MEDICARE_DATA_DIR=$(mktemp -d)
export MEDICARE_DATA_DIR
trap 'rm -rf "$MEDICARE_DATA_DIR"' EXIT
mkdir "$MEDICARE_DATA_DIR/raw"

uv run pytest -q
uv run dbt deps

cp "$sample/inpatient_2022.csv" "$MEDICARE_DATA_DIR/raw"
uv run python -m ingest.load_raw
uv run dbt build

cp "$sample/inpatient_2023.csv" "$MEDICARE_DATA_DIR/raw"
uv run python -m ingest.load_raw
uv run dbt build
uv run python -m ingest.query "select data_year, count(*) as fact_rows from fct_inpatient_discharges group by 1 order by 1"
