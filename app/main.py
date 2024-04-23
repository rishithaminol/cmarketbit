#!/usr/bin/env python3

import requests
import json
import datetime
import os
from pathlib import Path


def error_message(message):
    timestamp_ = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    j = {
        "timestamp_": timestamp_,
        "log": {
            "level": 'error'
        },
        "message": message
    }
    log_file = open(os.getenv("CM_LOG_FILE"), "a")
    log_file.write("{}\n".format(json.dumps(j)))
    log_file.close()

# API may return invalid data.
# This function suppress that and give a null
def safe_get_coin_element(coin_data, key_name):
    try:
        return coin_data[key_name]
    except KeyError as ke:
        return None

def cm_rankings():
    try:
        cm_response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',
                            headers={
                                'Accepts': 'application/json',
                                'X-CMC_PRO_API_KEY': os.getenv('CM_API_KEY'),
                                'Accept-Encoding': 'deflate, gzip'
                            },
                            params={
                                'start': os.getenv("CM_CRYPTO_LISTING_START"),
                                'limit': os.getenv("CM_CRYPTO_LISTING_END")
                            }, timeout=5)
    except requests.exceptions.ConnectionError as e:
        error_message(str(e))
        return None

    if cm_response.status_code != 200:
        error_message("No succesfull response from server")
        return None

    j_text = json.loads(cm_response.text)
    cm_timestamp = j_text['status']['timestamp']

    log_file = open(os.getenv("CM_LOG_FILE"), "a")

    for coin in j_text['data']:
        j_data = {
            'timestamp_': cm_timestamp,
            'coin_id': safe_get_coin_element(coin, 'id'),
            'name': safe_get_coin_element(coin, 'name'),
            'symbol': safe_get_coin_element(coin, 'symbol'),
            'cmc_rank': safe_get_coin_element(coin, 'cmc_rank'),
            'num_market_pairs': safe_get_coin_element(coin, 'num_market_pairsss'),
            'circulating_supply': safe_get_coin_element(coin, 'circulating_supply'),
            'total_supply': safe_get_coin_element(coin, 'total_supply'),
            'max_supply': safe_get_coin_element(coin, 'max_supply'),
            'last_updated': safe_get_coin_element(coin ,'last_updated'),
            'date_added': safe_get_coin_element(coin, 'date_added'),
            'quote': {
                'USD': safe_get_coin_element(coin['quote'], 'USD')
            }
        }

        j_data = json.dumps(j_data)
        log_file.write("{}\n".format(j_data))
    
    log_file.close()

cm_rankings()
