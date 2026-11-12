import duckdb

from ingest.download import to_utf8
from ingest.load_raw import load


def test_windows_1252_bytes_become_utf8():
    assert to_utf8(b"Uci Health \x96 Los Alamitos") == "Uci Health – Los Alamitos".encode()


def test_utf8_bytes_pass_through_unchanged():
    assert to_utf8("Café".encode()) == "Café".encode()


def test_load_stacks_yearly_files_and_takes_the_year_from_the_filename(tmp_path):
    header = "Rndrng_Prvdr_CCN,DRG_Cd,Tot_Dschrgs\n"
    (tmp_path / "inpatient_2022.csv").write_text(header + "010001,003,14\n")
    (tmp_path / "inpatient_2023.csv").write_text(header + "010001,003,20\n010001,023,26\n")
    db = tmp_path / "w.duckdb"

    load(tmp_path, db)

    rows = duckdb.connect(str(db)).execute(
        "select data_year, Rndrng_Prvdr_CCN, DRG_Cd, Tot_Dschrgs from raw.inpatient order by all"
    ).fetchall()
    assert rows == [(2022, "010001", "003", "14"), (2023, "010001", "003", "20"), (2023, "010001", "023", "26")]


def test_discover_maps_each_year_to_its_csv_and_ignores_other_datasets():
    from ingest.download import discover

    catalog = {
        "dataset": [
            {
                "title": "Medicare Inpatient Hospitals - by Provider and Service : 2023-12-31",
                "distribution": [
                    {"mediaType": "application/json", "downloadURL": "https://x/2023.json"},
                    {"mediaType": "text/csv", "downloadURL": "https://x/2023.csv"},
                ],
            },
            {
                "title": "Medicare Inpatient Hospitals - by Provider and Service : 2022-12-01",
                "distribution": [{"mediaType": "text/csv", "downloadURL": "https://x/2022.csv"}],
            },
            {
                "title": "Medicare Inpatient Hospitals - by Provider : 2023-12-31",
                "distribution": [{"mediaType": "text/csv", "downloadURL": "https://x/other.csv"}],
            },
        ]
    }

    assert discover(catalog) == {2022: "https://x/2022.csv", 2023: "https://x/2023.csv"}
