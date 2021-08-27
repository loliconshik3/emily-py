from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit, QShortcut
from PyQt5.QtCore import Qt

class TextBox(QLineEdit):

    def __init__(self, root=None, parent=None, *args, **kwargs):
        QLineEdit.__init__(self, parent, *args, **kwargs)
        
        self.root = root

        self._init_widget()

    def _init_widget(self):
        self.setGeometry(3, 0, self.root.max_width/2-9, 30)
        #self.resize(self.root.max_width / 2, 30)

        self.setPlaceholderText('Type to filter...')
        self.setTextMargins(45,0,45,0)

        self.setStyleSheet('QLineEdit { font-size: 18px; }')

        # Bind down key
        down_shortcut = QShortcut(QKeySequence('Down'), self, context=Qt.WidgetShortcut)
        down_shortcut.activated.connect(self.down_key)

        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        self.root.search_text = self.text()

        if not self.root.script_list.isHidden():
            self.root.script_list.redraw_script_list()
        else:
            self.root.apps_list.redraw_app_list()

    def down_key(self):
        if self == self.root.app.focusWidget():
            if not self.root.script_list.isHidden():
                self.root.script_list.setFocus()

                try:
                    if self.root.script_list.currentItem() == self.root.script_list.item(0):
                        self.root.script_list.scroll_down()
                    else:
                        self.root.script_list.setCurrentItem(self.root.script_list.item(0))
                        self.root.script_list.setCursor(self.root.script_list.item(0))
                except: pass
            else:
                self.root.apps_list.setFocus()

                try: 
                    if self.root.apps_list.currentItem() == self.root.apps_list.item(0):
                        self.root.apps_list.scroll_down()
                    else:
                        self.root.apps_list.setCurrentItem(self.root.apps_list.item(0))
                        self.root.apps_list.setCursor(self.root.apps_list.item(0))
                except: pass