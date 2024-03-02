import os
import sys
from typing import *
import requests
import duckdb as db
import pandas as pd
import datetime

import pendulum
from airflow.models import Variable as vr
from airflow.decorators  import task, dag

motherduck_token = vr.get('motherduck_token')
#motherduck_token = os.environ.get('motherduck_token')
database_name = 'marketcap'
table_name = 'exchange'


@dag(
    schedule="1 * * * *", # Run at 8:00 AM every day
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["coin_cap"],
)
def exchange_trade_data():

    @task()
    def get_exchange_data() -> List[Dict[str, str]]:
            url = 'https://api.coincap.io/v2/exchanges'
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise exception for non-200 status codes
                data = response.json().get('data', []) 

                return data
            except requests.RequestException as e:
                # logging.error(f"Error fetching exchange data: {e}")
                return None  

    @task()
    def transform_exchange_data(from_api) -> pd.DataFrame:
        results = from_api 

        # Create an empty list to store the transformed data
        transformed_data = []
        try:

            for result in results:
                # Assuming 'updated' is the UNIX timestamp you want to convert
                updated_at_unix = result.get('updated')
                
                # Direct conversion within the transform_exchange_data function
                # Check if 'updated_at_unix' is not None and convert; otherwise, set as None
                updated_at = datetime.datetime.utcfromtimestamp(int(updated_at_unix) / 1000).isoformat() if updated_at_unix else None

                exchange = {
                    'exchangeId': str(result['exchangeId']),
                    'name': str(result['name']),
                    'rank': int(result['rank']) if result['rank'] is not None else None,
                    'percentTotalVolume': float(result['percentTotalVolume']) if result['percentTotalVolume'] is not None else None,
                    'volumeUsd': float(result['volumeUsd']) if result['volumeUsd'] is not None else None,
                    'tradingPairs': int(result['tradingPairs']) if result['tradingPairs'] is not None else None,
                    'socket': bool(result['socket']),
                    'exchangeUrl': str(result['exchangeUrl']),
                    'updated': int(result['updated']) if result['updated'] is not None else None,
                    'updated_at': updated_at  # Use the direct conversion result
                }

                transformed_data.append(exchange)
            # Create DataFrame from the transformed data
            return pd.DataFrame(transformed_data)
        except requests.RequestException as e:
                # logging.error(f"Error fetching exchange data: {e}")
            return None        

    @task()
    def write_to_motherduck_from_data_frame(database_name: str, motherduck_token: str,
                                             table_name: str, data_frame: pd.DataFrame):
        con = db.connect(f'md:{database_name}?motherduck_token={motherduck_token}')
        con.execute("SELECT 1")
        
        curr= con.cursor()           
        curr.execute(
                    f"""
                    INSERT INTO {table_name}
                    SELECT * FROM {'data_frame'}
                    ON CONFLICT (exchangeId) DO UPDATE SET 
                    name = EXCLUDED.name,
                    rank = EXCLUDED.rank,
                    percentTotalVolume = EXCLUDED.percentTotalVolume,
                    volumeUsd = EXCLUDED.volumeUsd,
                    tradingPairs = EXCLUDED.tradingPairs,
                    socket = EXCLUDED.socket,
                    exchangeUrl = EXCLUDED.exchangeUrl,
                    updated = EXCLUDED.updated,
                    updated_at = EXCLUDED.updated_at;      
                    """
                )

        # Commit the changes and close the connection
        con.commit()
        con.close()

        print(f"Successfully inserted {len(data_frame)} rows in {table_name}")

    api_raw_data = get_exchange_data()
    data_frame = transform_exchange_data(api_raw_data)
    write_to_motherduck_from_data_frame(database_name, motherduck_token,
                                             table_name, data_frame)
    
exchange_trade_data()