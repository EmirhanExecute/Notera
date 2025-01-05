from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QLayout, QPushButton, QSizePolicy,
        QWidget)
#from main import *
class NoteWidget(QWidget):
    def __init__(self, title, content):
        super().__init__()
        self.setStyleSheet("border: 1px solid black; padding: 10px; margin: 5px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.title_label = QLabel(f"<b>{title}</b>")
        self.content_label = QLabel(content)

        layout.addWidget(self.title_label)
        layout.addWidget(self.content_label)
        self.setLayout(layout)
class Container(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self._widgets = []

    def sizeHint(self):
        w = self.size().width()
        h = 0
        for widget in self._widgets:
            h += widget.layout().heightForWidth(w)

        sh = super().sizeHint()
        print(sh)
        print(w, h)
        return sh

    def add_widget(self, widget):
        self._widgets.append(widget)
        self.layout().addWidget(widget)

    def add_stretch(self):
        self.layout().addStretch()
class NoteW(QWidget):
    def __init__(self,color,b_note,d_note,n_id):
        super().__init__()
        self.setAutoFillBackground(True)
        
        self.xnotes = QtWidgets.QWidget(self)
        #self.setGeometry(QtCore.QRect(230, 210, 281, 231))
        #self.setStyleSheet("background-color: rgb(255, 255, 127);\nborder-radius: 10px;")
        self.xnotes.setGeometry(QtCore.QRect(230, 210, 297, 266))
        self.xnotes.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.xnotes.setAutoFillBackground(False)
        self.setStyleSheet("QWidget {\n"
"    background-color: rgb(255, 255, 27);\n"
"    border-radius: 3px;\n"
"border:none\n"
"\n"
"}")
        x_verticalLayout = QtWidgets.QVBoxLayout(self.xnotes)
        x_verticalLayout.setContentsMargins(0, 0, 0, 0)
        x_verticalLayout.setSpacing(1)
     
        x_label = QtWidgets.QLabel(self.xnotes)
     
        x_label.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        x_label.setFont(font)
        x_label.setStyleSheet("")
        x_label.setScaledContents(False)
        x_label.setAlignment(QtCore.Qt.AlignCenter)
        x_label.setWordWrap(True)
        x_label.setText(b_note);
        x_label.setContentsMargins(0, 0, 0, 0)
        x_verticalLayout.addWidget(x_label)
        
        line = QtWidgets.QFrame(self.xnotes)
        line.setStyleSheet("background-color: rgb(255, 125, 27);")
        line.setMinimumSize(QtCore.QSize(0, 1))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        x_verticalLayout.addWidget(line)
        
        details_label = QtWidgets.QLabel(self.xnotes)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(details_label.sizePolicy().hasHeightForWidth())
        details_label.setMinimumSize(QtCore.QSize(275, 150))
        details_label.setMaximumSize(QtCore.QSize(16777215, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        details_label.setFont(font)
        details_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        details_label.setFrameShadow(QtWidgets.QFrame.Plain)
        details_label.setAlignment(QtCore.Qt.AlignCenter)
        details_label.setWordWrap(True)
        details_label.setText(d_note)
        details_label.setContentsMargins(0, 0, 0, 0)
        details_label.setStyleSheet("")
        x_verticalLayout.addWidget(details_label)
        
        x_pushButton = QtWidgets.QPushButton(self.xnotes)
        x_pushButton.setMinimumSize(QtCore.QSize(0, 30))
        x_pushButton.setStyleSheet("QPushButton{\n"
"            background-color:rgba(85, 98, 112, 255);\n"
"            color:rgba(255, 255, 255, 200);\n"
"            border-radius:3px;\n"
"        }\n"
"        QPushButton:pressed{\n"
"            padding-left:5px;\n"
"            padding-top:5px;\n"
"            background-color:rgba(255, 107, 107, 255);\n"
"            background-position:calc(100% - 10px)center;\n"
"        }\n"
"        QPushButton:hover{\n"
"            background-color:rgba(255, 107, 107, 255);\n"
"        }")
        x_pushButton.setText("Open")
        x_pushButton.clicked.connect(lambda _, note_id=n_id: MainWindow().open_existing_note_page(note_id))
        
        x_verticalLayout.addWidget(x_pushButton)
        self.setLayout(x_verticalLayout)
class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
class FlowLayout(QLayout):

    widthChanged = pyqtSignal(int)

    def __init__(self, parent=None, margin=0, spacing=-1, orientation=Qt.Orientation.Horizontal):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)
        self.itemList = []
        self.orientation = orientation

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        if (self.orientation == Qt.Orientation.Horizontal):
            return self.doLayoutHorizontal(QRect(0, 0, width, 0), True)
        elif (self.orientation == Qt.Orientation.Vertical):
            return self.doLayoutVertical(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        if (self.orientation == Qt.Orientation.Horizontal):
            self.doLayoutHorizontal(rect, False)
        elif (self.orientation == Qt.Orientation.Vertical):
            self.doLayoutVertical(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayoutHorizontal(self, rect, testOnly):
        # Get initial coordinates of the drawing region (should be 0, 0)
        x = rect.x()
        y = rect.y()
        lineHeight = 0
        i = 0
        for item in self.itemList:
            wid = item.widget()
            # Space X and Y is item spacing horizontally and vertically
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)
            # Determine the coordinate we want to place the item at
            # It should be placed at : initial coordinate of the rect + width of the item + spacing
            nextX = x + item.sizeHint().width() + spaceX
            # If the calculated nextX is greater than the outer bound...
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x() # Reset X coordinate to origin of drawing region
                y = y + lineHeight + spaceY # Move Y coordinate to the next line
                nextX = x + item.sizeHint().width() + spaceX # Recalculate nextX based on the new X coordinate
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX # Store the next starting X coordinate for next item
            lineHeight = max(lineHeight, item.sizeHint().height())
            i = i + 1

        return y + lineHeight - rect.y()

    def doLayoutVertical(self, rect, testOnly):
        # Get initial coordinates of the drawing region (should be 0, 0)
        x = rect.x()
        y = rect.y()
        # Initalize column width and line height
        columnWidth = 0
        lineHeight = 0

        # Space between items
        spaceX = 0
        spaceY = 0

        # Variables that will represent the position of the widgets in a 2D Array
        i = 0
        j = 0
        for item in self.itemList:
            wid = item.widget()
            # Space X and Y is item spacing horizontally and vertically
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical)
            # Determine the coordinate we want to place the item at
            # It should be placed at : initial coordinate of the rect + width of the item + spacing
            nextY = y + item.sizeHint().height() + spaceY
            # If the calculated nextY is greater than the outer bound, move to the next column
            if nextY - spaceY > rect.bottom() and columnWidth > 0:
                y = rect.y() # Reset y coordinate to origin of drawing region
                x = x + columnWidth + spaceX # Move X coordinate to the next column
                nextY = y + item.sizeHint().height() + spaceY # Recalculate nextX based on the new X coordinate
                # Reset the column width
                columnWidth = 0

                # Set indexes of the item for the 2D array
                j += 1
                i = 0

            # Assign 2D array indexes
            item.x_index = i
            item.y_index = j

            # Only call setGeometry (which place the actual widget using coordinates) if testOnly is false
            # For some reason, Qt framework calls the doLayout methods with testOnly set to true (WTF ??)
            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            y = nextY # Store the next starting Y coordinate for next item
            columnWidth = max(columnWidth, item.sizeHint().width()) # Update the width of the column
            lineHeight = max(lineHeight, item.sizeHint().height()) # Update the height of the line

            i += 1 # Increment i

        # Only call setGeometry (which place the actual widget using coordinates) if testOnly is false
        # For some reason, Qt framework calls the doLayout methods with testOnly set to true (WTF ??)
        if not testOnly:
            self.calculateMaxWidth(i)
            #print("Total width : " + str(totalWidth))
            self.widthChanged.emit(self.totalMaxWidth + spaceX * self.itemsOnWidestRow)
            #self.widthChanged.emit(self.totalMaxWidth)
        return lineHeight

    # Method to calculate the maximum width among each "row" of the flow layout
    # This will be useful to let the UI know the total width of the flow layout
    def calculateMaxWidth(self, numberOfRows):
        # Init variables
        self.totalMaxWidth = 0
        self.itemsOnWidestRow = 0

        # For each "row", calculate the total width by adding the width of each item
        # and then update the totalMaxWidth if the calculated width is greater than the current value
        # Also update the number of items on the widest row
        for i in range(numberOfRows):
            rowWidth = 0
            itemsOnWidestRow = 0
            for item in self.itemList:
                # Only compare items from the same row
                if (item.x_index == i):
                    rowWidth += item.sizeHint().width()
                    itemsOnWidestRow += 1
                if (rowWidth > self.totalMaxWidth):
                    self.totalMaxWidth = rowWidth
                    self.itemsOnWidestRow = itemsOnWidestRow
