import duckdb as db
import pandas as pd
import os

from extract import get_exchange_data
from transform import transform_exchange_data
from load import (
    get_database_connection,
    write_to_duckdb_from_dataframe,
    connect_to_md,
    write_to_motherduck_from_duckdb
) 

motherduck_token = os.environ.get("motherduck_token")

def run() -> None:
    data = get_exchange_data()
    clean_data = transform_exchange_data(data)
    con = get_database_connection()

    write_to_duckdb_from_dataframe(con, table_name = 'exchange', data_frame = clean_data)

    connect_to_md(con, motherduck_token)

    write_to_motherduck_from_duckdb(con, table = 'exchange', database = 'crypto')

if __name__ == '__main__':
    run()

