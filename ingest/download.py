"""Download every published year of the CMS inpatient file into the raw folder as UTF-8."""
import json
import re
import urllib.request

CATALOG_URL = "https://data.cms.gov/data.json"
TITLE = re.compile(r"^Medicare Inpatient Hospitals - by Provider and Service : (\d{4})-")


def discover(catalog: dict) -> dict[int, str]:
    found = {}
    for dataset in catalog["dataset"]:
        match = TITLE.match(dataset["title"])
        if match:
            found[int(match[1])] = next(
                d["downloadURL"] for d in dataset["distribution"] if d.get("mediaType") == "text/csv"
            )
    return dict(sorted(found.items()))


def to_utf8(raw: bytes) -> bytes:
    try:
        raw.decode("utf-8")
        return raw
    except UnicodeDecodeError:
        return raw.decode("cp1252").encode("utf-8")


def main() -> None:
    from ingest.paths import RAW_DIR

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(CATALOG_URL) as response:
        sources = discover(json.load(response))
    for year, url in sources.items():
        target = RAW_DIR / f"inpatient_{year}.csv"
        if target.exists():
            continue
        print(f"downloading {year}")
        with urllib.request.urlopen(url) as response:
            target.write_bytes(to_utf8(response.read()))


if __name__ == "__main__":
    main()
