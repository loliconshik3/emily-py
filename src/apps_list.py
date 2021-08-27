from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QShortcut
from PyQt5.QtCore import QSize, Qt
import utils
import os

class AppsList(QListWidget):

    def __init__(self, root=None, parent=None, *args, **kwargs):
        QListWidget.__init__(self, parent, *args, **kwargs)
        
        self.apps = {}
        self.apps_dir_path = f"/usr/share/applications"
        self.apps_files = os.listdir(self.apps_dir_path)
        for filename in self.apps_files:
            file_path = f"{self.apps_dir_path}/{filename}"

            with open(file_path, "r") as file:
                filetext = file.readlines()
                find_name = None
                execute = None
                icon = None

                for line in filetext:
                    need_str = line[:5] 
                    replace_str = line[5:-1]

                    if need_str == "Name=" and find_name == None:
                        find_name = replace_str
                    if need_str == "Exec=" and execute == None:
                        execute = replace_str
                        find_index = execute.find('%')
                        if find_index != -1: execute = execute[:find_index]
                    if need_str == "Icon=" and icon == None:
                        icon = replace_str
                    if line[:14] == "NoDisplay=true":
                        find_name = None
                        execute = None
                        icon = None
                        break
                    if find_name != None and execute != None and icon != None:
                        break

                if icon:
                    if icon[0] != '/':
                        icon = utils.find_icon_path(icon)

                self.apps[find_name] = {
                    'script': f'{execute}',
                    'icon' : f'{icon}'
                }
            
        del self.apps[None]

        self.root = root

        self._init_widget()

    def _init_widget(self):
        for app in self.apps.keys():
            try: icon = QIcon(self.apps[app]['icon'])
            except: icon = QIcon()

            item = QListWidgetItem(icon, app, parent=self, type=2)
            self.addItem(item)

        self.sortItems()

        self.setGeometry(5, 35, self.root.max_width / 2, 365)

        self.setStyleSheet('QListWidget { border: none; font-size: 20px; }')
        self.itemClicked.connect(self.item_clicked)
        self.setIconSize(QSize(32,32))

        QShortcut(QKeySequence('Down'), self, context=Qt.WidgetShortcut).activated.connect(self.scroll_down)

        QShortcut(QKeySequence('Up'), self, context=Qt.WidgetShortcut).activated.connect(self.scroll_up)


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

    def item_clicked(self):
        self.root.return_key()

    def redraw_app_list(self):
        self.clear()

        index = 0
        for app in self.apps:
            if self.root.search_text.lower() in app.lower():
                try: icon = QIcon(self.apps[app]['icon'])
                except: icon = QIcon()

                item = QListWidgetItem(icon, app, parent=self, type=2)
                self.addItem(item)
                index += 1

        self.sortItems()

        self.root.counter.setText(f'{index}/{len(self.apps)}')

        self.setCurrentItem(self.item(0))
