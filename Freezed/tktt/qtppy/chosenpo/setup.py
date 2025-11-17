import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Ui_untitled import Ui_MainWindow

class mainmau(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None) -> None:
        super(mainmau, self).__init__(parent)
        self.setupUi(self)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = mainmau()
    mywin.show()
    sys.exit(app.exec_())
    