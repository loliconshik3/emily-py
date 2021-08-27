from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QShortcut, QLabel
from PyQt5.QtCore import QSize, Qt
import script_list
import subprocess
import apps_list
import textbox
import time
import sys
import os

class MainWindow():

    def __init__(self):
        ttime = time.time()

        self.app = QApplication(sys.argv)

        # Init window sizes
        available_rect = QDesktopWidget().availableGeometry()
        self.max_width = available_rect.width()
        self.max_height = available_rect.height()

        # 3. Create an instance of your application's GUI
        self.window = QWidget()
        self._init_window()

        #Init label
        self.label = QLabel(parent=self.window)
        self.label.setStyleSheet('QLabel { font-size: 18px; text-align: center;}')
        self.label.setGeometry(5, 0, 50, 30)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('arun:')

        # Init script list
        self.script_list = script_list.ScriptList(root=self, parent=self.window)

        # Init apps list
        self.apps_list = apps_list.AppsList(root=self, parent=self.window)

        #Init counter
        self.counter = QLabel(parent=self.window)
        self.counter.setStyleSheet('QLabel { font-size: 18px; text-align: center; color: gray}')
        self.counter.setGeometry(self.max_width / 2 - 60, 0, 50, 30)
        self.counter.setAlignment(Qt.AlignCenter)
        self.counter.setText(f'{len(self.apps_list.get_widget_items())}/{len(self.apps_list.get_widget_items())}')

        # Move window to center
        self.screen = self.window.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.screen.moveCenter(centerPoint)
        self.window.move(self.screen.topLeft())

        # Create textbox
        self.textbox = textbox.TextBox(root=self, parent=self.window)
        self.search_text = ""

        # 4. Show your application's GUI
        self.window.show()
        self.apps_list.show()
        self.script_list.hide()
        self.textbox.setFocus()

        try:
            self.apps_list.setCurrentItem(self.apps_list.item(0))
        except: pass
        try:
            self.script_list.setCurrentItem(self.script_list.item(0))
        except: pass

        print(time.time()-ttime)

    def _init_window(self):
        self.window.setWindowTitle('neomenu')
        self.window.setMinimumSize(QSize(self.max_width / 2, 400))
        self.window.setMaximumSize(QSize(self.max_width / 2, 400))
        self.window.setWindowFlags(Qt.CustomizeWindowHint)
        #self.window.setGeometry(0, 0, self.max_width / 2, 200)

        # Bind return key
        QShortcut(QKeySequence('Return'), self.window).activated.connect(self.return_key)
        
        # Bind escape key
        QShortcut(QKeySequence('Escape'), self.window).activated.connect(lambda: exit())

        # Bind change key
        QShortcut(QKeySequence('Tab'), self.window).activated.connect(self.change_list)

    def change_list(self):
        self.textbox.clear()

        if self.apps_list.isHidden():
            self.script_list.hide()
            self.apps_list.show()
            
            self.label.setText('arun:')
            self.counter.setText(f'{len(self.apps_list.get_widget_items())}/{len(self.apps_list.get_widget_items())}')

            try:
                self.apps_list.setCurrentItem(self.apps_list.item(0))
            except: pass
        else:
            self.apps_list.hide()
            self.script_list.show()

            self.label.setText('srun:')
            self.counter.setText(f'{len(self.script_list.get_widget_items())}/{len(self.script_list.get_widget_items())}')

            try:
                self.script_list.setCurrentItem(self.script_list.item(0))
            except: pass

    def return_key(self):
        if self.apps_list.isHidden():  
            selected_items = self.script_list.selectedItems()
            script_list = "scripts"
        else:
            selected_items = self.apps_list.selectedItems()
            script_list = "apps"

        selected_item = None
        launch_script = None

        if selected_items != []:
            selected_item = selected_items[0].text()
        else:
            try:
                if script_list == 'scripts':
                    selected_item = self.script_list.item(0).text()
                else:
                    selected_item = self.apps_list.item(0).text()
            except:
                print('non items!')

        if selected_item != None:
            if script_list == "scripts":
                launch_script = self.script_list.scripts[selected_item]['script']
            else:
                launch_script = self.apps_list.apps[selected_item]['script']

            if launch_script != None:
                self.window.hide()

                commands = launch_script.split('\n')
                for command in commands:
                    subprocess.Popen(command, shell=True)

                exit()

        self.textbox.clear()