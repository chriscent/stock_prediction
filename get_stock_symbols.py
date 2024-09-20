import pandas as pd
import json


def fetch_nse_symbols():
    with open('stock_symbols_list.txt', 'r') as file:
        lines = file.readlines()
    # Remove newline characters
    symbols = [line.strip() for line in lines]
    return symbols
    

    
