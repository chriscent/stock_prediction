from get_stock_symbols import fetch_nse_symbols

from fourier_analysis import fetch_and_plot_stock_data

class Controller():
    def __init__(self):
        self.stock_symbols = []
        
    def get_stock_symbols(self):
        return fetch_nse_symbols()
        
    def generate_and_display_graph(self, selected_items, year_selected=1, component_number=5):
        for stock in selected_items:
            if ".BO" in stock:
                modified_stock_symbol = stock
            else:
                modified_stock_symbol = "{}.NS".format(stock)
            
            fetch_and_plot_stock_data(modified_stock_symbol, int(year_selected), (int(component_number)))
        