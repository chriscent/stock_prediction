import pandas as pd
import json
from app_controller import Controller

def fetch_wishlist():
    with open('wishlist_stocks.txt', 'r') as file:
        lines = file.readlines()
    # Remove newline characters
    symbols = [line.strip() for line in lines]
    return symbols
    
stocks = fetch_wishlist()
controller = Controller()
controller.generate_and_display_graph(stocks)
    