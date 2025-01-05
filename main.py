# APP Imports
import sys
import os
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

# Import user interface file
from ui_main_window import *

from flowlayout4 import FlowLayout
#from flowlayout4 import NoteW


# IMPORT FUNCTIONS
from ui_functions import *
# Global value for the windows status
import sqlite3
x_userid = 0;
active_note_id=None
WINDOW_SIZE = 0;
# This will help us determine if the window is minimized or maximized
class NoteW(QWidget):
    def __init__(self,color,b_note,d_note,n_id,parent=None):
        super().__init__()
        self.parent=parent
        self.setAutoFillBackground(True)
        self.ui = Ui_MainWindow()
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
        #self.note_id = n_id 
        #print(parent)
        x_pushButton.setText("Open")
        x_pushButton.clicked.connect(lambda: self.parent.open_existing_note_page(n_id))
        
        x_verticalLayout.addWidget(x_pushButton)
        self.setLayout(x_verticalLayout)

# Main class
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
       
        global x_userid
        global active_note_id
        # Remove window tlttle bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 

        # Set main background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #FlowLayout(self.note_widget)
        
        #self.ui.notes_layout.setObjectName("notes_layout")

        #self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)
        
        # Apply shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 150))
        
        # Appy shadow to central widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        
        # Ana layout
        self.layout = self.ui.verticalLayout;#QVBoxLayout(self)
        #-----------------------
        # UI'den gelen notes_page zaten QStackedWidget içinde
        self.scroll_area = QScrollArea(self.ui.notes_page)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidgetResizable(True) 
        self.notes_layout = QVBoxLayout(self.ui.notes_page)
        self.notes_layout.setContentsMargins(0, 0, 0, 0)  # Kenar boşluklarını sıfırla
        self.notes_layout.addWidget(self.scroll_area) 
        # Scroll içerik
        self.scroll_content = QWidget()
        self.scroll_content.setMinimumSize(self.scroll_area.size())  # Minimum boyutu ayarla
        self.scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.flow_layout = FlowLayout(self.scroll_content)
        self.scroll_content.setLayout(self.flow_layout)

        self.scroll_area.setWidget(self.scroll_content)

        # Notları ekle
        #self.add_notes()

        # Sayfayı aktif yap
        #self.stacked_widget.setCurrentWidget(self.notes_page)

        #---------------------------
        self.login=False
        self.ui.left_menu_notes.hide()
        
        #self.ui.left_side_menu.width=50
        # HIDE ERROR
        #self.ui.frame_error.hide()
        # Button click events to our top bar buttons
        # 
        #Minimize window
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized())
        #Close window
        self.ui.closeButton.clicked.connect(lambda: self.close())
        #Restore/Maximize window
        self.ui.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())
        # ###############################################
        #self.ui.UserButton.clicked.connect(lambda: self.slideRightMenu())
        
        # BT CLOSE POPUP
        self.ui.pushButton_close_pupup.clicked.connect(lambda: self.mesajhide())
       

        # BT LOGIN
        self.ui.pushButton_login.clicked.connect(lambda: self.checkFields())
        
        
        # ###############################################
        # Move window on mouse drag event on the tittle bar
        # ###############################################
        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size  
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
            # ###############################################

        
        # ###############################################
        # Add click event/Mouse move event/drag event to the top header to move the window
        # ###############################################
        self.ui.main_header.mouseMoveEvent = moveWindow
        # ###############################################






        # SLIDABLE LEFT MENU/////////////////
        #Left Menu toggle button
        self.ui.left_menu_toggle_btn.clicked.connect(lambda: self.slideLeftMenu())
        # ###############################################
        # //////////////////////////////////////
        #self.ui.left_menu_toggle_btn.clicked.connect(lambda: self.toggleMenu(150, True))




        # STACKED PAGES (DEFAUT /CURRENT PAGE)/////////////////
        #Set the page that will be visible by default when the app is opened 
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)
        # ###############################################
        # //////////////////////////////////////

        # STACKED PAGES NAVIGATION/////////////////
        #Using side menu buttons

        #navigate to Home page
        self.ui.home_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.home_page))
        

        #navigate to Accounts page
        self.ui.accounts_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.login_page))
            
        self.ui.Login_reg.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.register_page))
        self.ui.Reg_login.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.login_page))
        #navigate to Settings page
        self.ui.settings_button.clicked.connect(lambda: self.widgetler())
        #lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page))
        self.ui.logoutBtn.clicked.connect(lambda: self.logoutUser())
        #navigate to Notes_page
        self.ui.notes_button.clicked.connect(lambda: self.load_notes())
        self.ui.changepassword_Btn.clicked.connect(lambda: self.UserChangePassword())
        #DB Connection..
        self.db_baglan()
        self.setup_database()
        


        # ###############################################
        # //////////////////////////////////////
        self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page)
        self.ui.changepasBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.passchange_page))
        
        self.ui.RegisterBtn.clicked.connect(lambda:self.UserRegister())
        
        self.ui.stackedWidget.setCurrentWidget(self.ui.home_page)
        self.ui.newnoteBtn.clicked.connect(lambda:self.New_note())    
        self.ui.newnote_cancel.clicked.connect(self.cancel_note_edit)   
        self.ui.newnote_save.clicked.connect(lambda:self.save_note(x_userid))
        # ############################################
        # Show window
        self.show()
        # ###############################################


    # ###############################################
    #
    # STYLES
    #
    styleLineEditOk = ("QLineEdit {\n"
    "    border: 2px solid rgb(45, 45, 45);\n"
    "    border-radius: 5px;\n"
    "    padding: 15px;\n"
    "    background-color: rgb(30, 30, 30);    \n"
    "    color: rgb(100, 100, 100);\n"
    "}\n"
    "QLineEdit:hover {\n"
    "    border: 2px solid rgb(55, 55, 55);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "    border: 2px solid rgb(255, 207, 0);    \n"
    "    color: rgb(200, 200, 200);\n"
    "}")

    styleLineEditError = ("QLineEdit {\n"
    "    border: 2px solid rgb(255, 85, 127);\n"
    "    border-radius: 5px;\n"
    "    padding: 15px;\n"
    "    background-color: rgb(30, 30, 30);    \n"
    "    color: rgb(100, 100, 100);\n"
    "}\n"
    "QLineEdit:hover {\n"
    "    border: 2px solid rgb(55, 55, 55);\n"
    "}\n"
    "QLineEdit:focus {\n"
    "    border: 2px solid rgb(255, 207, 0);    \n"
    "    color: rgb(200, 200, 200);\n"
    "}")

    stylePopupError = ("background-color: rgb(255, 85, 127); border-radius: 5px;")
    stylePopupOk = ("background-color: rgb(0, 255, 123); border-radius: 5px;")




    # ###############################################
    # Add mouse events to the window
    # ###############################################
    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
        # ###############################################
    def setup_database(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT, priority INTEGER DEFAULT 3, date TEXT)")
            self.db_connection.commit()
            
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı oluşturulurken bir hata oluştu: {e}")
    def mesajhide(self):
        self.ui.frame_error.hide()
   

    def db_baglan(self):
        
        self.db_connection = sqlite3.connect("notes.db")
        self.cursor = self.db_connection.cursor()
    def checkFields(self):
        textUser = ""
        textPassword = ""

        def showMessage(message):
            self.ui.frame_error.show()
            self.ui.label_error.setText(message)

        # CHECK USER
        if not self.ui.lineEdit_user.text():
            textUser = " User Empyt. "
            self.ui.lineEdit_user.setStyleSheet(self.styleLineEditError)
        else:
            textUser = ""
            self.ui.lineEdit_user.setStyleSheet(self.styleLineEditOk)

        # CHECK PASSWORD
        if not self.ui.lineEdit_password.text():
            textPassword = " Password Empyt. "
            self.ui.lineEdit_password.setStyleSheet(self.styleLineEditError)
        else:
            textPassword = ""
            self.ui.lineEdit_password.setStyleSheet(self.styleLineEditOk)


        # CHECK FIELDS
        if textUser + textPassword != '':
            text = textUser + textPassword
            showMessage(text)
            self.ui.frame_error.setStyleSheet(self.stylePopupError)
        else:
            text = " Login OK. "
            if self.ui.checkBox_save_user.isChecked():
                text = text + " | Saver user: OK "
            showMessage(text)
            self.ui.frame_error.setStyleSheet(self.stylePopupOk)
            self.handle_login()
    def handle_login(self):
        global x_userid
        username = self.ui.lineEdit_user.text()
        password = self.ui.lineEdit_password.text()
        #print(username,password)
        self.cursor.execute("SELECT id,username,password FROM users WHERE username = ? AND password = ?", (username, password))
        result = self.cursor.fetchone()
        #print(result)
        if result:
            x_userid=result[0]    
            #QtWidgets.QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
            
            #self.ui.UserButton.show()
            #self.ui.accounts_button.hide()
            self.ui.left_menu_notes.show()
            self.login=True
            #self.ui.login_area.hide()
            self.ui.loggedUser.setText(username)
            self.ui.loggedUser_chpass.setText(username)
            self.ui.lineEdit_oldPassword.setText(password)
            self.ui.frame_error_logged.setStyleSheet(self.stylePopupOk)
            self.ui.accounts_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page))
            #print(str(result[0]))
            self.load_notes()
            self.ui.stackedWidget.setCurrentWidget(self.ui.notes_page)
        else:
            QtWidgets.QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre hatalı!")
    def logoutUser(self):
        self.login=False
        self.ui.left_menu_notes.hide()
        self.ui.accounts_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.login_page))
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
    def UserChangePassword(self):
        username = self.ui.loggedUser_chpass.text()
        oldpassword=self.ui.lineEdit_oldPassword.text()
        password0 = self.ui.lineEdit_newPassword.text()
        cpassword =self.ui.lineEdit_newPassword_confrm.text()
        if cpassword == password0 :
           self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, oldpassword))
           result = self.cursor.fetchone()
           #print(result)
           if result:
            user_id=result[0]
            #print(user_id)
            self.cursor.execute("UPDATE users SET password = ? WHERE id = ?", (password0, user_id))
            self.db_connection.commit()
            self.db_connection.close()
            self.db_baglan()
            self.ui.frame_error_logged.setStyleSheet(self.stylePopupOk)
            self.ui.label_error_4.setText('USER LOGGED IN PASSWORD CHANGED')
            self.ui.stackedWidget.setCurrentWidget(self.ui.accounts_page)
            #self.ui.frame_error_logged.setStyleSheet(self.stylePopupError)
            #self.ui.label_error_4.setText('USER LOGGED IN PASSWORD NOT CHANGED')
                
    def UserRegister(self):
        username = self.ui.lineEdit_Ruser.text()
        password=self.ui.lineEdit_Rpassword.text()
        cpassword =self.ui.lineEdit_Rpassword_confrm.text()
        if cpassword == password :
           self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
           result = self.cursor.fetchone()
           #print(result)
           if not result:
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username.strip(), password.strip()))
                self.db_connection.commit()
                self.db_connection.close()
                self.db_baglan()
                self.ui.frame_error_reg.setStyleSheet(self.stylePopupOk)
                self.ui.label_error_3.setText('USER SAVED Succesfully..')
                #QtWidgets.QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
            except sqlite3.IntegrityError:
                #QtWidgets.QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten kayıtlı!")
                self.ui.frame_error_reg.setStyleSheet(self.stylePopupError)
                self.ui.label_error_3.setText('ERROR : This username is already registered!')
            except sqlite3.Error as e:
                QtWidgets.QMessageBox.critical(self, "Database Error", f"An error occurred while registering: {e}")

            
            
            self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
           
    def clearLayout(layout: QtWidgets.QLayout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QtWidgets.QLayout):
                clearLayout(item)
            elif item.widget():
                item.widget().setParent(None)
            else:
                layout.removeItem(item)              
    def update_notes(self, notes):
        self.clear_notes()
        for note in notes:
            note_widget=NoteW('red',
                               note[1],
                               f"{note[2]} \n \n Priority: {note[3]} | Date: {note[4] if note[4] else 'N/A'}",
                               str(note[0]),
                               parent=self)
                               
            self.flow_layout.addWidget(note_widget)
    def fetch_notes_from_db(self):
        import sqlite3
        global x_userid
        userid=str(x_userid)
        connection = sqlite3.connect("notes.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, content, priority, date FROM notes WHERE user_id = ? ORDER BY priority ASC, date ASC",(userid))
        rows = cursor.fetchall()
        connection.close()
        return rows    
    def clear_notes(self):
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()    
    def load_notes(self):
        notes = self.fetch_notes_from_db()
        self.update_notes(notes)
    def New_note(self):
        global active_note_id
        active_note_id=None
        self.ui.title_text.setText("")
        d = QDate().currentDate()
        self.ui.dateEdit.setDate(d)
        self.ui.note_content.document().clear()
        self.ui.stackedWidget.setCurrentWidget(self.ui.newnote_page)
    def cancel_note_edit(self):
        # Aktif not ID'sini sıfırla
        self.active_note_id = None

        # StackedWidget içindeki notes_page sayfasına geçiş yap
        self.ui.stackedWidget.setCurrentWidget(self.ui.notes_page)
    def open_existing_note_page(self, note_id):
        global active_note_id
        active_note_id=note_id
        #QtWidgets.QMessageBox.information(self, "Note", "Note id"+note_id)
        self.cursor.execute("SELECT id, title, content, priority, date FROM notes WHERE id = ?", (note_id,))
        note = self.cursor.fetchone()
        if note:
            self.ui.title_text.setText(note[1])
            d = QtCore.QDate.fromString(note[4], "yyyy-MM-dd")
            self.ui.dateEdit.setDate(d)
            self.ui.priority_combo.setCurrentIndex(note[3] - 1 if note[3] else 2)
            self.ui.note_content.document().setPlainText(note[2])
            
            self.ui.stackedWidget.setCurrentWidget(self.ui.newnote_page) 
         
    def save_note(self,userid):
        global active_note_id
        content = self.ui.note_content.document().toPlainText()
        if not content.strip():
            QtWidgets.QMessageBox.warning(self, "Hata", "Not boş olamaz!")
            return

        title = self.ui.title_text.text() 
        if title=="":
            title="Untitled"
        # content.split()[0] if content.split() else "Untitled"
        priority = int(self.ui.priority_combo.currentText())
        date = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        
        if  active_note_id is None:
            self.cursor.execute("INSERT INTO notes (user_id, title, content, priority, date) VALUES (?, ?, ?, ?, ?)", (str(userid), title, content, priority, date if date else None))
        else:
            self.cursor.execute("UPDATE notes SET title = ?, content = ?, priority = ?, date = ? WHERE id = ?", (title, content, priority, date if date else None, active_note_id))

        self.db_connection.commit()
        self.db_connection.close()
        self.db_baglan()
        #QtWidgets.QMessageBox.information(self, "Başarılı", "Not kaydedildi!")
        self.load_notes()
        self.ui.stackedWidget.setCurrentWidget(self.ui.notes_page)
    # Restore or maximize your window
    def restore_or_maximize_window(self):
        # Global windows state
        global WINDOW_SIZE #The default value is zero to show that the size is not maximized
        win_status = WINDOW_SIZE

        if win_status == 0:
        	# If the window is not maximized
        	WINDOW_SIZE = 1 #Update value to show that the window has been maxmized
        	self.showMaximized()

        	# Update button icon  when window is maximized
        	self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-restore.png"))#Show minized icon
        else:
        	# If the window is on its default size
            WINDOW_SIZE = 0 #Update value to show that the window has been minimized/set to normal size (which is 800 by 400)
            self.showNormal()

            # Update button icon when window is minimized
            self.ui.restoreButton.setIcon(QtGui.QIcon(u":/icons/icons/cil-window-maximize.png"))#Show maximize icon

    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.ui.left_side_menu.width()
            maxExtend = maxWidth
            standard = 50
            print(str(width))
            # SET MAX WIDTH
            if width == 50:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    ########################################################################
    # Slide left menu
    ########################################################################
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.ui.left_side_menu.width

        # If minimized
        if width == 50:
            # Expand menu
            newWidth = 150
        # If maximized
        else:
            # Restore menu
            newWidth = 50

        # Animate the transition
        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
        
    # /////////////////////////////////////////////////////////////////////////
    ########################################################################
    # Slide right menu
    ########################################################################
    def slideRightMenu(self):
        # Get current left menu width
        width = self.ui.right_side_menu.width()
        
        # If minimized
        if width == 0:
            # Expand menu
            newWidth = 150
        # If maximized
        else:
            # Restore menu
            newWidth = 0

        # Animate the transition
        self.animation = QPropertyAnimation(self.ui.right_side_menu, b"minimumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    # /////////////////////////////////////////////////////////////////////////






# Execute app
# 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
else:
	print(__name__, "hh")

# press ctrl+b in sublime to run

