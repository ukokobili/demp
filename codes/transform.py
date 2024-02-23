import pandas as pd
from unix_time import get_utc_from_unix_time

def transform_exchange_data(results) -> pd.DataFrame:
    results = results

    coincap = []

    for result in results:
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
            'updated_at': get_utc_from_unix_time(result.get('updated'))
        }
        coincap.append(exchange)
    data_ = pd.DataFrame(coincap)

    return data_