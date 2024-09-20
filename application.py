import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QComboBox, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QListView, QAbstractItemView, QLabel
from PySide6.QtCore import Qt, QSortFilterProxyModel, QStringListModel
from PySide6.QtGui import QFont

from app_controller import Controller

controller = Controller()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cool Futuristic App")
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

        # Create a button
        self.button = QPushButton("Submit")
        self.button.setFont(QFont("Arial", 14))
        self.button.clicked.connect(self.print_selected_options)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_box)
        layout.addWidget(self.search_box)
        layout.addWidget(self.list_view)
        layout.addWidget(self.label)
        layout.addWidget(self.combo2)
        layout.addWidget(self.label2)
        layout.addWidget(self.combo3)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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

    def filter_list(self, text):
        self.proxy_model.setFilterFixedString(text)

    def print_selected_options(self):
        selected_options = []
        selected_indexes = self.list_view.selectionModel().selectedIndexes()
        selected_items = [index.data() for index in selected_indexes]
        selected_options.extend(selected_items)
        year_selected = self.combo2.currentText()
        selected_options.append("year:" + year_selected)
        component_number = self.combo3.currentText()
        selected_options.append("component:" + component_number)
        self.text_box.setText("\n".join(selected_options))
        
        controller.generate_and_display_graph(selected_items, year_selected, component_number)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
