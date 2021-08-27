from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QShortcut
from PyQt5.QtCore import QSize, Qt
import os

class ScriptList(QListWidget):

    def __init__(self, root=None, parent=None, *args, **kwargs):
        QListWidget.__init__(self, parent, *args, **kwargs)
        
        home = os.path.expanduser("~")

        self.scripts = {}

        try:
            self.scripts_dir_path = f"{home}/.emily/scripts"
            self.scripts_files = os.listdir(self.scripts_dir_path)
            for filename in self.scripts_files:
                file_path = f"{self.scripts_dir_path}/{filename}"
            
                with open(file_path, "r") as file:
                    self.scripts[filename.replace('.sh', '')] = {
                        'script': file.read()
                    }
        except:
            self.scripts_dir_path = f"{os.path.dirname(os.path.abspath(__file__))[:-4]}/scripts"
            self.scripts_files = os.listdir(self.scripts_dir_path)
            for filename in self.scripts_files:
                file_path = f"{self.scripts_dir_path}/{filename}"
            
                with open(file_path, "r") as file:
                    self.scripts[filename.replace('.sh', '')] = {
                        'script': file.read()
                    }

        try:
            self.icons_dir_path = f"{home}/.emily/icons"
            self.icon_files = os.listdir(self.icons_dir_path)
            for filename in self.icon_files:
                file_path = f"{self.icons_dir_path}/{filename}"

                filename = filename[:-4]
                if filename in self.scripts.keys():
                    self.scripts[filename]['icon'] = file_path
        except:
            self.icons_dir_path = f"{os.path.dirname(os.path.abspath(__file__))[:-4]}/icons"
            self.icon_files = os.listdir(self.icons_dir_path)
            for filename in self.icon_files:
                file_path = f"{self.icons_dir_path}/{filename}"

                filename = filename[:-4]
                if filename in self.scripts.keys():
                    self.scripts[filename]['icon'] = file_path

        if len(self.scripts.keys()) > 1:
            del self.scripts['Test Script']

        self.root = root

        self._init_widget()

    def _init_widget(self):
        for script in self.scripts.keys():
            try: icon = QIcon(self.scripts[script]['icon'])
            except: icon = QIcon()

            item = QListWidgetItem(icon, script, parent=self, type=2)
            self.addItem(item)

        self.sortItems()

        self.setGeometry(5, 35, self.root.max_width / 2, 365)

        self.setStyleSheet('QListWidget { border: none; font-size: 20px; }')
        self.itemClicked.connect(lambda: self.root.return_key())
        self.setIconSize(QSize(32,32))

        down_shortcut = QShortcut(QKeySequence('Down'), self, context=Qt.WidgetShortcut)
        down_shortcut.activated.connect(self.scroll_down)
        
        up_shortcut = QShortcut(QKeySequence('Up'), self, context=Qt.WidgetShortcut)
        up_shortcut.activated.connect(self.scroll_up)

    def keyPressEvent(self, event):
        if not event.key in (Qt.Key_Up, Qt.Key_Down):
            self.root.textbox.setFocus()
            self.root.textbox.insert(event.text())

    def get_widget_items(self):
        items = []
        for index in range(self.count()):
            items.append(self.item(index))

        return items

    def scroll_to_item(self, item):
        item.setSelected(True)
        self.scrollToItem(item, QAbstractItemView.PositionAtBottom)

    def scroll_up(self):
        items = self.get_widget_items()

        current_index = items.index(self.selectedItems()[0])
        if current_index > 0:
            self.setCurrentItem(items[current_index-1])
        else:
            self.setCurrentItem(items[-1])


    def scroll_down(self):
        items = self.get_widget_items()

        current_index = items.index(self.selectedItems()[0])
        if current_index < len(items)-1:
            self.setCurrentItem(items[current_index+1])
        else:
            self.setCurrentItem(items[0])

    def redraw_script_list(self):
        self.clear()

        index = 0
        for script in self.scripts:
            if self.root.search_text.lower() in script.lower():
                try: icon = QIcon(self.scripts[script]['icon'])
                except: icon = QIcon()

                item = QListWidgetItem(icon, script, parent=self, type=2)
                self.addItem(item)

                index += 1

        self.sortItems()

        self.root.counter.setText(f'{index}/{len(self.scripts)}')

        self.setCurrentItem(self.item(0))
