import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QListView, QAbstractItemView, QLabel
from PySide6.QtCore import Qt, QSortFilterProxyModel, QStringListModel
from PySide6.QtGui import QFont

from app_controller import Controller

controller = Controller()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.selected_options = self.load_selected_options()
        self.make_selected_items_unique()
        self.setWindowTitle("Stock App")
        self.setGeometry(100, 100, 400, 400)

        # Create a text box
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setFont(QFont("Arial", 12))

        self.list_view = QListView()
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_view.setFont(QFont("Arial", 12))

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type to search...")
        self.search_box.setFont(QFont("Arial", 12))
        self.search_box.textChanged.connect(self.filter_list)
        stock_list = controller.get_stock_symbols()
        self.model = QStringListModel(stock_list)
        
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.model)

        self.list_view.setModel(self.proxy_model)
        
        self.label = QLabel("Years")

        # Create combo boxes
        self.combo2 = QComboBox()
        self.combo2.addItems(["1", "2", "3", "4", "5"])
        self.combo2.setCurrentText("1")
        self.combo2.setFont(QFont("Arial", 12))
        
        self.label2 = QLabel("Number of Components")

        self.combo3 = QComboBox()
        self.combo3.addItems(["5", "6", "7", "10", "15"])
        self.combo3.setCurrentText("5")
        self.combo3.setFont(QFont("Arial", 12))

        # Create a buttons
        self.button1 = QPushButton("Add")
        self.button1.setFont(QFont("Arial", 14))
        self.button1.clicked.connect(self.add_stocks)
        
        self.button2 = QPushButton("Remove")
        self.button2.setFont(QFont("Arial", 14))
        self.button2.clicked.connect(self.remove_stocks)
        
        self.button3 = QPushButton("Save")
        self.button3.setFont(QFont("Arial", 14))
        self.button3.clicked.connect(self.save_options)
        
        self.button4 = QPushButton("Submit")
        self.button4.setFont(QFont("Arial", 14))
        self.button4.clicked.connect(self.print_selected_options)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(self.search_box)
        layout.addWidget(self.list_view)
        layout.addWidget(self.label)
        layout.addWidget(self.combo2)
        layout.addWidget(self.label2)
        layout.addWidget(self.combo3)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(self.button1)
        layout2.addWidget(self.button2)
        layout2.addWidget(self.button3)
        layout2.addWidget(self.button4)
        
        layout.addLayout(layout2)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        
        self.update_stocks_in_textbox()

        # Apply CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
            }
            QTextEdit {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #555555;
            }
            QComboBox {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #444444;
                color: #ffffff;
                selection-background-color: #555555;
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border: 1px solid #666666;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QLineEdit {
                background-color: #444444;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 5px;
            }
            QListView {
                background-color: #1E1E1E;
                border: 1px solid #BB86FC;
                border-radius: 5px;
                padding: 5px;
                color: #FFFFFF;
            }
            QListView::item {
                padding: 10px;
            }
            QListView::item:selected {
                background-color: #BB86FC;
                color: #121212;
            }
            QLineEdit:hover, QListView:hover {
                border: 1px solid #03DAC6;
            }
            QLabel {
                background-color: #555555;
                color: #ffffff;
            }
        """)
        
    def update_stocks_in_textbox(self, save=False):
        text_to_print = ""
        if save:
            text_to_print = "Options Saved!\n"
            
        text_to_print = text_to_print + " ".join(self.selected_options["selected_items"])
        self.text_box.setText(text_to_print)
        
    def make_selected_items_unique(self):
        self.selected_options["selected_items"] = list(set(self.selected_options["selected_items"]))
    
    def fetch_wishlist(self):
        with open('wishlist_stocks.txt', 'r') as file:
            lines = file.readlines()
            # Remove newline characters
            symbols = [line.strip() for line in lines]
            
        return symbols
    
    def load_selected_options(self):
        return { "selected_items": self.fetch_wishlist()}
        

    def filter_list(self, text):
        self.proxy_model.setFilterFixedString(text)
        
    def get_selected_items(self):
        selected_indexes = self.list_view.selectionModel().selectedIndexes()
        return [index.data() for index in selected_indexes]
        
    def add_stocks(self):
        selected_items = self.get_selected_items()
        self.selected_options["selected_items"].extend(selected_items)
        self.make_selected_items_unique()
        self.update_stocks_in_textbox()
        
    def remove_stocks(self):
        selected_items = self.get_selected_items()
        self.selected_options["selected_items"] = [stock for stock in self.selected_options["selected_items"] if stock not in selected_items]
        self.make_selected_items_unique()
        self.update_stocks_in_textbox()
        
    def save_options(self):
        # Open the file nums.txt in write mode
        with open('wishlist_stocks.txt', 'w') as file:
            # Write each element of list1 to the file, one per line
            for item in self.selected_options["selected_items"]:
                file.write(f"{item}\n")
                
        self.update_stocks_in_textbox(save=True)


    def print_selected_options(self):
        selected_items = self.get_selected_items()
        self.selected_options["selected_items"].extend(selected_items)
        self.make_selected_items_unique()
        year_selected = self.combo2.currentText()
        self.selected_options["year"] = "year:" + year_selected
        component_number = self.combo3.currentText()
        self.selected_options["components"] = "components:" + component_number
        self.text_box.setText(
            "\n".join(
                [
                    " ".join(self.selected_options["selected_items"]),
                    self.selected_options["year"],
                    self.selected_options["components"]
                ]
            )
        )
        
        controller.generate_and_display_graph(self.selected_options["selected_items"], year_selected, component_number)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
