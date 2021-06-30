# Imports
from PyQt5 import QtWidgets, uic
from pathlib import Path
import pandas as pd
import pyqtgraph
from scipy.signal import savgol_filter
from numpy import array, column_stack, trapz

# Major configs
pyqtgraph.setConfigOption('background', 'w')
pyqtgraph.setConfigOption('foreground', 'k')

# Main class/GUI application
class LIFSSA(QtWidgets.QMainWindow):
	def __init__(self):
		super(LIFSSA, self).__init__()
		self.gui = uic.loadUi('lifssa.ui')
		self.gui.show()
		# Global variables
		self.matrix = array([None])
		self.filtered = array([None])
		self.area, self.height = 0, 0
		# Connects
		self.connects()
		# Extra settings
		self.setup()
		
	def connects(self):
		self.gui.spectraselect_pb.clicked.connect(self.openfile)
		self.gui.apply_pb.clicked.connect(self.apply)
		
	def setup(self):
		# Configures graphic
		self.gui.graphic.setTitle('LIFS Spectrum')
		self.gui.graphic.setLabel('bottom', 'Wavelength', units='nm')
		self.gui.graphic.setLabel('left', 'Counts', units='a.u.')
		self.gui.graphic.setXRange(0, 1000)
		self.gui.graphic.enableAutoRange()
		self.gui.graphic.addLegend()
	
	def openfile(self):
		file = QtWidgets.QFileDialog.getOpenFileName(self, 'Select spectrum file', str(Path.cwd()), 'Text files (*.txt)')
		if file[0] == '':
			QtWidgets.QMessageBox.warning(None, 'Warning', 'Cancelled by the user')
			self.gui.spectrapath_le.setText('')
			self.gui.spectrapath_le.setEnabled(False)
			self.gui.graphic.clear()
			self.gui.spectrafilter_cb.setEnabled(False)
			self.gui.spectraarea_cb.setEnabled(False)
			self.gui.apply_pb.setEnabled(False)
		else:
			# Load data from file (hardcoded)
			self.matrix = pd.read_csv(file[0], header=None, sep='\t', skiprows=1).to_numpy()
			# Setup gui elements
			self.gui.graphic.clear()
			self.gui.spectrapath_le.setText(str(file[0]))
			self.gui.spectrapath_le.setEnabled(True)
			self.gui.spectrafilter_cb.setEnabled(True)
			self.gui.spectraarea_cb.setEnabled(True)
			self.gui.apply_pb.setEnabled(True)
			self.gui.graphic.plot(self.matrix[:, 0], self.matrix[:, 1], name='Data', pen='#000099')
	
	def apply(self):
		name = ''
		color = ''
		# Checks if filter is checked
		if self.gui.spectrafilter_cb.isChecked():
			self.filtered = savgol_filter(self.matrix[:, 1], 19, 13)
			name = 'Filtered'
			color = '#990099'
		else:
			self.filtered = self.matrix[:, 1]
			name = 'Data'
			color = '#000099'
		# Checks if area is needed
		if self.gui.spectraarea_cb.isChecked():
			self.height = max(self.filtered)
			self.area = trapz(self.filtered, self.matrix[:, 0])
			self.gui.spectraarea_dsb.setValue(self.area)
			self.gui.spectraheight_dsb.setValue(self.height)
		else:
			self.height = 0
			self.area = 0
			self.gui.spectraarea_dsb.setValue(0)
			self.gui.spectraheight_dsb.setValue(0)
		# Continue
		self.gui.graphic.clear()
		self.gui.graphic.plot(self.matrix[:, 0], self.filtered, name=name, pen=color)
	

# Main starter
if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	win = LIFSSA()
	app.exec()
	