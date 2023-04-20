from PyQt5.QtWidgets import QGridLayout, QPushButton, QLineEdit, QListWidget, QStyledItemDelegate, QStyle, QLabel, QWidget


class StyledItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        option.state &= ~QStyle.State_Selected
        super(StyledItemDelegate, self).initStyleOption(option, index)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Automation - Google Search")
        # Create a central widget instance
        self.centralwidget = QWidget(MainWindow)
        # Create a QGridLayout inside central widget
        layout = QGridLayout(self.centralwidget)
        # Button widget
        self.btn_run = QPushButton("Start")
        self.btn_run.setStyleSheet('font-size: 10pt')
        # Show label
        self.text_label = QLabel()
        self.text_label.setStyleSheet('font-size: 10pt')
        
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setStyleSheet('font-size: 10pt')
        self.btn_stop.hide()
        
        self.line_edit_link = QLineEdit("Enter the search term to search in Google")
        self.line_edit_link.setStyleSheet('font-size: 10pt;color: grey;')

        # List Widget
        self.list_view = QListWidget()
        # Disable clickable list
        delegate = StyledItemDelegate(self.list_view)
        self.list_view.setItemDelegate(delegate)   
        self.list_view.hide()  
        
        # Add widgets to the layout
       
        layout.addWidget(self.btn_run, 2, 1)
        layout.addWidget(self.line_edit_link, 2, 0)
        layout.addWidget(self.text_label, 5, 0)
        layout.addWidget(self.btn_stop, 3, 1)
        layout.addWidget(self.list_view, 6, 0, 1,3)

        # Set the layout on the application's window
        MainWindow.setCentralWidget(self.centralwidget)