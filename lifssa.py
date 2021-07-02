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
		self.matrix = array([0])
		self.filtered = array([0])
		self.area, self.height = 0, 0
		# Connects
		self.connects()
		# Extra settings
		self.setup()
		
	def connects(self):
		self.gui.spectraselect_pb.clicked.connect(self.openfile)
		self.gui.apply_pb.clicked.connect(self.apply)
		self.gui.actionAbout.triggered.connect(self.showabout)
		self.gui.actionQuit.triggered.connect(self.quitapp)
		self.gui.actionExport.triggered.connect(self.exportdata)
	
	def showabout(self):
		QtWidgets.QMessageBox.about(None, 'About LIFSsa', 'This program was developed during Python classes')
	
	def quitapp(self):
		self.gui.close()
		self.close()
		
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
	
	def exportdata(self):
		if self.matrix.mean() == 0.0 and self.filtered.mean() == 0.0 and self.area == 0 and self.height == 0:
			QtWidgets.QMessageBox.warning(None, 'Warning', 'There are no data to be exported')
		else:
			fd = QtWidgets.QFileDialog.getSaveFileName(None, 'Choose name to save file', directory=str(Path.cwd().joinpath('Data.xlsx')), filter='Excel Files (*.xlsx)')
			if fd[0] == '':
				QtWidgets.QMessageBox.warning(None, 'Cancelled', 'Cancelled py the user')
			else:
				# User properly choose file to save
				exit_data = pd.DataFrame(columns=['Wavelength', 'Count', 'Filtered'], data=column_stack((self.matrix, self.filtered)))
				exit_data['Area'] = [self.area] + [None]*(self.filtered.size-1)
				exit_data['Height'] = [self.height] + [None]*(self.filtered.size-1)
				exit_data.to_excel(Path(fd[0]).with_suffix('.xlsx'), index=False)
				QtWidgets.QMessageBox.information(None, 'Done', 'Data saved!')
			

# Main starter
if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	win = LIFSSA()
	app.exec()
	