# Imports
from PyQt5 import QtWidgets, uic
from pathlib import Path
import pandas as pd

# Main class/GUI application
class LIFSSA(QtWidgets.QMainWindow):
	def __init__(self):
		super(LIFSSA, self).__init__()
		self.gui = uic.loadUi('lifssa.ui')
		self.gui.show()
		# Connects
		self.gui.spectraselect_pb.clicked.connect(self.openfile)
	
	def openfile(self):
		file = QtWidgets.QFileDialog.getOpenFileName(self, 'Select spectrum file', str(Path.cwd()), 'Text files (*.txt)')
		if file[0] == '':
			QtWidgets.QMessageBox.warning(None, 'Warning', 'Cancelled by the user')
		else:
			matrix = pd.read_csv(file[0], header=None, sep=' ').to_numpy()
			self.gui.graphic.plot(matrix[:, 0], matrix[:, 1])

# Main starter
if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	win = LIFSSA()
	app.exec()
	