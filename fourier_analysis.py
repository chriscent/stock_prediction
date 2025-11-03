import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json
import numpy as np
from scipy.fft import fft, ifft
import csv

import matplotlib
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QScrollArea
years = 1

stock_symbol = "HDFCBANK.NS"


def get_stock_data(stock_symbol, number_of_years):
    # Define the period (last year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*number_of_years)
    
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    print("stock_symbol: ", stock_symbol)
    print("start_date: ", start_date)
    print("end_date: ", end_date)
    print("stock_data: ", stock_data)
    
    all_data = pd.DataFrame()
    
    stock_data['Ticker'] = stock_symbol
    all_data = pd.concat([all_data, stock_data[['Ticker', 'Close']]], axis=0)
    
    # Reset index to have a clean DataFrame
    all_data.reset_index(inplace=True)
    
    # Write the data to a CSV file
    all_data.to_csv('stockdata.csv', index=False)
    
    
def convert_to_json():
    csv_file = 'stockdata.csv'
    data = pd.read_csv(csv_file)
    
    # Create a dictionary to hold the JSON structure
    json_data = {}
    
    # Populate the dictionary with the required structure
    for index, row in data.iterrows():
        stock = row['Ticker']
        date = row['Date']
        price = row['Close']
        
        if stock not in json_data:
            json_data[stock] = {"stock price": {}}
        
        json_data[stock]["stock price"][date] = price
    
    # Write the dictionary to a JSON file
    json_file = 'stockdata.json'
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)
        
def plot_fourier_transformed_graph(stock_name, num_components=5):
    with open('stockdata.json', 'r') as json_file:
        data = json.load(json_file)
    # Extract stock prices
    stock_prices = data[stock_name]["stock price"]
    
    price = []
    
    for date, price_each_day in stock_prices.items():
        price.append(price_each_day)
        
    time = np.arange(0, len(price))
    
    # Perform Fourier Transform
    fft_values = fft(price)
    print("fft_values:", fft_values)
    print("price:", price)
    
    # Reconstruct the signal using a limited number of components
    fft_values_reconstructed = np.copy(fft_values)
    fft_values_reconstructed[num_components:] = 0
    price_reconstructed = ifft(fft_values_reconstructed)
    
    # Plot original and reconstructed price data
    plt.figure(figsize=(12, 6))
    plt.plot(time, price, label='Original Price Data')
    plt.plot(time, price_reconstructed, label=f'Reconstructed Price Data ({num_components} Components - {stock_name})', linestyle='--')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()
    

def fetch_and_plot_stock_data(stock_symbol, years=1, num_components=5):     
  
    get_stock_data(stock_symbol, years)      
    convert_to_json()
    plot_fourier_transformed_graph(stock_symbol, num_components)
    
class PlotCanvas(FigureCanvas):
    def __init__(self, stock_name, number_of_years, num_components=5, width=12, height=6, dpi=100):
        self.number_of_years = number_of_years
        self.num_components = num_components
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.stock_name = stock_name
        super().__init__(self.fig)

    def plot_random(self):
        x = range(10)
        y = [random.randint(1, 10) for _ in x]
        x2 = range(10)
        y2 = [random.randint(10, 100) for _ in x]
        self.ax.plot(x, y, label='Original Price Data')
        self.ax.plot(x, y, label='Original Price Data') 
        self.ax.plot(x2, y2, label='Test 2') 
        self.ax.set_xlabel('Time') 
        self.ax.set_ylabel('Price') 
        self.ax.legend() 
        self.ax.grid(True)
        self.draw()
        
    def get_stock_data(self):
        # Define the period (last year)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*self.number_of_years)
        
        stock_data = yf.download(self.stock_name, start=start_date, end=end_date)
        
        all_data = pd.DataFrame()
        
        stock_data['Ticker'] = self.stock_name
        all_data = pd.concat([all_data, stock_data[['Ticker', 'Close']]], axis=0)
        
        # Reset index to have a clean DataFrame
        all_data.reset_index(inplace=True)
        
        # Write the data to a CSV file
        all_data.to_csv('stockdata.csv', index=False)
        
        
    def convert_to_json(self):
        csv_file = 'stockdata.csv'
        data = pd.read_csv(csv_file)
        
        # Create a dictionary to hold the JSON structure
        json_data = {}
        
        # Populate the dictionary with the required structure
        for index, row in data.iterrows():
            stock = row['Ticker']
            date = row['Date']
            price = row['Close']
            
            if stock not in json_data:
                json_data[stock] = {"stock price": {}}
            
            json_data[stock]["stock price"][date] = price
        
        # Write the dictionary to a JSON file
        json_file = 'stockdata.json'
        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=4)
    
    def plot_fourier_transformed_graph(self):
        self.get_stock_data()
        self.convert_to_json()
        with open('stockdata.json', 'r') as json_file:
            data = json.load(json_file)
        # Extract stock prices
        stock_prices = data[self.stock_name]["stock price"]
        
        price = []
        
        for date, price_each_day in stock_prices.items():
            price.append(price_each_day)
            
        time = np.arange(0, len(price))
        
        # Perform Fourier Transform
        fft_values = fft(price)
        print("self.num_components:", self.num_components)
        # print("price:", price)
        
        # Reconstruct the signal using a limited number of components
        fft_values_reconstructed = np.copy(fft_values)
        fft_values_reconstructed[self.num_components:] = 0
        price_reconstructed = ifft(fft_values_reconstructed)
        
        # Plot original and reconstructed price data
        plt.figure(figsize=(12, 6))
        self.ax.plot(time, price, label='Original Price Data')
        self.ax.plot(time, price_reconstructed, label=f'Reconstructed Price Data ({self.num_components} Components - {self.stock_name})', linestyle='--')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Price')
        self.ax.legend() 
        self.ax.grid(True)
        self.draw()
    
class ScrollableGraphs(QWidget):
    def __init__(self, stock_names, years, components):
        super().__init__()
        self.stock_names = stock_names
        self.years = int(years)
        self.components = int(components)
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout(scroll_area_widget)

        # self.plots = [PlotCanvas(stock, self.years, self.components) for stock in self.stock_names]
        # for plot in self.plots:
        #     # plot.plot_random()
        #     plot.plot_fourier_transformed_graph()
        #     scroll_area_layout.addWidget(plot)

        scroll_area.setWidget(scroll_area_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.setWindowTitle('Scrollable Graphs')
    
