import sys
import duckdb
from ingest.paths import DB
con = duckdb.connect(str(DB), read_only=True)
for q in sys.argv[1:]:
    print(con.sql(q))
