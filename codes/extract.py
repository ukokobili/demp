import logging
import sys
import requests
from typing import Any, Dict, List, Optional

def get_exchange_data() -> List[Dict[str, str]]:
    url = 'https://api.coincap.io/v2/exchanges'
    try:
        r = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request, {ce}")
        sys.exit(1)
    return r.json().get('data', [])
    
# get_exchange_data()