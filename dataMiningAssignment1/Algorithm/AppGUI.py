import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QFileDialog, QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QFont, QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt

from data_transformation import transform_data
from Apriori import FP_itemsets, assosiation_ruls, Apriori

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.precentage = None
        self.result_window1 = None
        self.result_window2 = None
        self.file_path = ""
        self.setWindowTitle("Assignment1")
        self.setGeometry(600,300, 800,500)
        self.setStyleSheet("background:#31619C")
        self.read_file = QPushButton("Open CSV File", self)
        self.button = QPushButton("Submit",self)
        self.data_percentage = QLineEdit(self)
        self.support_input = QLineEdit(self)
        self.confidence_input = QLineEdit(self)
        self.initUI()

    def initUI(self):
        title = QLabel("Find Associations System", self)
        title.setGeometry(190, 0, 410, 100)
        title.setFont(QFont("Arial", 20))
        title.setStyleSheet("Color:white;"
                            "font-weight:bold;"
                            "background:#31619C")
        title.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)

        self.read_file.setGeometry(320,100,160,50)
        self.read_file.setStyleSheet("background:white;"
                                     "border-radius:20px;"
                                     "ont-size:20px;")
        self.read_file.clicked.connect(self.open_csv_file)

        validator = QDoubleValidator(0.0, 1.0, 120)
        validator.setNotation(QDoubleValidator.StandardNotation)

        self.data_percentage.setGeometry(320, 160, 160, 50)
        self.data_percentage.setPlaceholderText("% Of Data")
        self.data_percentage.setStyleSheet("Color:black;"
                                         "border-radius:20px;"
                                         "background:white;"
                                         "font-size:20px;"
                                         "font-family:Arial")
        self.data_percentage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.support_input.setValidator(validator)

        self.data_percentage.setValidator(QIntValidator(0,100))
        self.support_input.setGeometry(320, 220, 160, 50)
        self.support_input.setPlaceholderText("Support value")
        self.support_input.setStyleSheet("Color:black;"
                                        "border-radius:20px;"
                                        "background:white;"
                                        "font-size:20px;"
                                         "font-family:Arial")
        self.support_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.support_input.setValidator(QIntValidator())
        #0.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
        self.confidence_input.setGeometry(320, 280, 160, 50)
        self.confidence_input.setPlaceholderText("confidence value")
        self.confidence_input.setStyleSheet("Color:black;"
                                         "border-radius:20px;"
                                         "background:white;"
                                         "font-size:20px;"
                                         "font-family:Arial")
        self.confidence_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.confidence_input.setValidator(QIntValidator(0,100))

        self.button.setGeometry(350, 340, 80, 40)
        self.button.setStyleSheet("background: white;"
                                  "border-radius: 20px;")
        self.button.clicked.connect(self.on_clicked)


    def on_clicked(self):
        path = self.file_path
        sup = int(self.support_input.text())
        conf = int(self.confidence_input.text()) / 100
        self.precentage = float(self.data_percentage.text())
        if (path != ""):

            transformed_data, unique_itemsets, num_records = transform_data(path, self.precentage)
            #print("test")
            FP_result = FP_itemsets(transformed_data, unique_itemsets, num_records, sup)
            print(len(FP_result))
            #print([ key for key in FP_result.keys() if len(key) == 3])
            association_result = assosiation_ruls(FP_result, conf)
            association_result = [f'{key} : {value}' for key, value in association_result.items()]
            FP_result = [f'{list(key)} : {value}' for key, value in FP_result.items()]
            print(len(association_result))
            #print("test2")
            #print(len(FP_result))
            #print(sup)
            self.result_window1 = ResultWindow(FP_result)
            self.result_window2 = ResultWindow(association_result)
            self.result_window1.show()
            self.result_window2.show()

    def open_csv_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")



class ResultWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setStyleSheet("background:#31619C;")
        self.setGeometry(600,250,700,650)


        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)


        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        formatted_text = "\n".join(data)
        self.results = QLabel(formatted_text,self)
        self.results.setGeometry(0, 0, 900, 1000)
        self.results.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.results.setWordWrap(True)
        self.results.setStyleSheet("color:white;"
                                   "font-size:20px;")

        layout.addWidget(self.results)
        content_widget.setLayout(layout)


        scroll_area.setWidget(content_widget)


        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()