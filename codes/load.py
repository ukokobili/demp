import duckdb as db
import pandas as pd

def get_database_connection():
  con= db.connect('crypto.db')
  return con

def write_to_duckdb_from_dataframe(con, table_name: str, data_frame: pd.DataFrame):

  con.sql(
      f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            exchangeId VARCHAR(50) PRIMARY KEY,
            name VARCHAR(50),
            rank INTEGER,
            percentTotalVolume NUMERIC(8, 5),
            volumeUsd NUMERIC(18, 5),
            tradingPairs INTEGER,
            socket BOOLEAN,
            exchangeUrl VARCHAR(255),
            updated BIGINT,
            updated_at TIMESTAMP
        ); """
      )

  con.execute(
      f"""
        INSERT INTO {table_name}
        SELECT
        *
        FROM {'data_frame'}
        ON CONFLICT (exchangeId) DO UPDATE SET
        name = EXCLUDED.name,
        rank = EXCLUDED.rank,
        percentTotalVolume = EXCLUDED.percentTotalVolume,
        volumeUsd = EXCLUDED.volumeUsd,
        tradingPairs = EXCLUDED.tradingPairs,
        socket = EXCLUDED.socket,
        exchangeUrl = EXCLUDED.exchangeUrl,
        updated = EXCLUDED.updated,
        updated_at = EXCLUDED.updated_at
              """)
  

def connect_to_md(con, motherduck_token: str):
  con.sql(f"INSTALL md;")
  con.sql(f"LOAD md;")
  con.sql(f"SET motherduck_token='{motherduck_token}';")

def write_to_motherduck_from_duckdb(con, table:str, database:str):
  con.sql(f"SELECT CURRENT_DATABASE()")
  con.sql(f"USE {database}")
  con.sql(f"CREATE DATABASE IF NOT EXISTS marketcap FROM CURRENT_DATABASE()")
  con.sql(
      f"""
            CREATE TABLE IF NOT EXISTS {table} (
            exchangeId VARCHAR(50) PRIMARY KEY,
            name VARCHAR(50),
            rank INTEGER,
            percentTotalVolume NUMERIC(8, 5),
            volumeUsd NUMERIC(18, 5),
            tradingPairs INTEGER,
            socket BOOLEAN,
            exchangeUrl VARCHAR(255),
            updated BIGINT,
            updated_at TIMESTAMP
        );
      """)

  # Insert new data
  con.sql(
        f"""
    INSERT INTO {table} (
      exchangeId,
          name,
          rank,
          percentTotalVolume,
          volumeUsd,
          tradingPairs,
          socket,
          exchangeUrl,
          updated,
          updated_at
    )
    SELECT
      *
    FROM {table}
        ON CONFLICT (exchangeId) DO UPDATE SET
        name = EXCLUDED.name,
        rank = EXCLUDED.rank,
        percentTotalVolume = EXCLUDED.percentTotalVolume,
        volumeUsd = EXCLUDED.volumeUsd,
        tradingPairs = EXCLUDED.tradingPairs,
        socket = EXCLUDED.socket,
        exchangeUrl = EXCLUDED.exchangeUrl,
        updated = EXCLUDED.updated,
        updated_at = EXCLUDED.updated_at"""
    )

