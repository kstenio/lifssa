# Imports
from PyQt5 import QtWidgets, uic

# Main class/GUI application
class LIFSSA(QtWidgets.QMainWindow):
	def __init__(self):
		super(LIFSSA, self).__init__()
		self.gui = uic.loadUi('lifssa.ui')
		self.gui.show()

# Main starter
if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	win = LIFSSA()
	app.exec()
	