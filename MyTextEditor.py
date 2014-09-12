import sys

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
	QtGui.QMainWindow.__init__(self,parent)

	self.filename = ""

	self.initUI()
    
    def initToolBar(self):

	self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
	self.newAction.setStatusTip("Create a new document.")
	self.newAction.setShortcut("Ctrl+N")
	self.newAction.triggered.connect(self.new)

	self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open",self)
	self.openAction.setStatusTip("Open an existing document.")
	self.openAction.setShortcut("Ctrl+O")
	self.openAction.triggered.connect(self.open)

	self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
	self.saveAction.setStatusTip("Save document.")
	self.saveAction.setShortcut("Ctrl+S")
	self.saveAction.triggered.connect(self.save)

	self.printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print",self)
	self.printAction.setStatusTip("Print document.")
	self.printAction.setShortcut("Ctrl+P")
	self.printAction.triggered.connect(self.do_print)

	self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Preview",self)
	self.previewAction.setStatusTip("Print Preview")
	self.previewAction.setShortcut("Ctrl+;")
	self.previewAction.triggered.connect(self.preview)

	self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut",self)
	self.cutAction.setStatusTip("Cut")
	self.cutAction.setShortcut("Ctrl+X")
	self.cutAction.triggered.connect(self.text.cut)

	self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy",self)
	self.copyAction.setStatusTip("Copy")
	self.copyAction.setShortcut("Ctrl+C")
	self.copyAction.triggered.connect(self.text.copy)

	self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste",self)
	self.pasteAction.setStatusTip("Paste")
	self.pasteAction.setShortcut("Ctrl+V")
	self.pasteAction.triggered.connect(self.text.paste)

	self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo",self)
	self.undoAction.setStatusTip("Undo")
	self.undoAction.setShortcut("Ctrl+Z")
	self.undoAction.triggered.connect(self.text.undo)

	self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo",self)
	self.redoAction.setStatusTip("Redo")
	self.redoAction.setShortcut("Ctrl+Y")
	self.redoAction.triggered.connect(self.text.redo)

	bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"),"Insert bullet List",self)
	bulletAction.setStatusTip("Insert bullet list")
	bulletAction.setShortcut("Ctrl+Shift+B")
	bulletAction.triggered.connect(self.bulletList)

	numberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"),"Insert numbered List",self)
	numberedAction.setStatusTip("Insert numbered list")
	numberedAction.setShortcut("Ctrl+Shift+L")
	numberedAction.triggered.connect(self.numberList)
	
	self.toolbar = self.addToolBar("Options")

	self.toolbar.addAction(self.newAction)
	self.toolbar.addAction(self.openAction)
	self.toolbar.addAction(self.saveAction)
	self.toolbar.addAction(self.printAction)
	self.toolbar.addAction(self.previewAction)
	self.toolbar.addAction(self.cutAction)
	self.toolbar.addAction(self.copyAction)
	self.toolbar.addAction(self.pasteAction)
	self.toolbar.addAction(self.undoAction)
	self.toolbar.addAction(self.redoAction)
	self.toolbar.addAction(bulletAction)
	self.toolbar.addAction(numberedAction)

	self.toolbar.addSeparator()

	# Makes next toolbar appear underneath this one
	self.addToolBarBreak()

    def initFormatBar(self):
	self.formatbar = self.addToolBar("Format")

    def initMenuBar(self):
	menubar = self.menuBar()

	fileMenu = menubar.addMenu("File")
	editMenu = menubar.addMenu("Edit")
	viewMenu = menubar.addMenu("View")

	fileMenu.addAction(self.newAction)
	fileMenu.addAction(self.openAction)
	fileMenu.addAction(self.saveAction)
	fileMenu.addAction(self.printAction)
	fileMenu.addAction(self.previewAction)

	editMenu.addAction(self.cutAction)
	editMenu.addAction(self.copyAction)
	editMenu.addAction(self.pasteAction)
	editMenu.addAction(self.undoAction)
	editMenu.addAction(self.redoAction)

    def initUI(self):

	self.text = QtGui.QTextEdit(self)
	self.setCentralWidget(self.text)

	self.initToolBar()
	self.initFormatBar()
	self.initMenuBar()

	# initialize statusbar for window
	self.statusBar = self.statusBar()	

	# x and y coords on the screen, width, height
	self.setGeometry(100,100,1030,800)
	self.setWindowTitle("MyTextEditor")

	# tabs to 33 pixels
	self.text.setTabStopWidth(33)

	self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

	self.text.cursorPositionChanged.connect(self.cursorPosition)


    def new(self):
	spawn = Main(self)
	spawn.show()

    def open(self):
	# Get filename and show only .writer files
	self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File',".","")

	if self.filename:
	    with open(self.filename,"rt") as file:
		self.text.setText(file.read())
    def save(self):
	# Only open dialog if there is no filename yet
	if not self.filename:
	    self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

	# Append extension if not there yet
	# Nah

	# Store contents along with format in html
	with open(self.filename, "wt") as file:
	    file.write(self.text.toHtml())

    def preview(self):
	# Open preview dialog
	preview = QtGui.QPrintPreviewDialog()
	
	# If a print is requested, open print dialog
	preview.paintRequested.connect(lambda p: self.text.do_print_(p))

	preview.exec_()


    def do_print(self):
	# Open print dialog
	dialog = QtGui.QPrintDialog()

	if dialog.exec_() == QtGui.QDialog.Accepted:
	    self.text.document().do_print_(dialog.printer())
	
    def bulletList(self):
	cursor = self.text.textCursor()
	
	cursor.insertList(QtGui.QTextListFormat.ListDisc)

    def numberList(self):
	cursor = self.text.textCursor()

	cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def cursorPosition(self):
	cursor = self.text.textCursor()
	
	line = cursor.blockNumber() + 1
	col = cursor.columnNumber()
	
	self.statusBar.showMessage("Line: {} | Column: {}".format(line,col))

def main():
    app = QtGui.QApplication(sys.argv)
    
    main = Main()
    main.show()
	
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


