from pathlib import Path

from PySide2 import QtWidgets, QtCore, QtGui

from ReorderAttrs.config import load
from ReorderAttrs.config import settings
from ReorderAttrs.maya_logic import get_maya_items as gmi
from ReorderAttrs.maya_logic import reorder_attributes as ra

_ROOT_DIR = Path(__file__).parent.parent


class ReorderAttributesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ReorderAttributesWindow, self).__init__(parent)

        self.setWindowTitle(f"{settings.APP_NAME}  |  v{settings.VERSION}")
        self.setMinimumSize(300, 300)
        self.setWindowIcon(QtGui.QIcon(f"{_ROOT_DIR}/resources/icons/list_icon_black.svg"))

        print('hello world')

        stylesheet = load.load_stylesheet(f"{_ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.selection_watcher = gmi.SelectionWatcher(self.populate)
        self.selection_watcher.start()

        self.build_ui()
        self.populate()

    def build_ui(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(10, 10, 10, 10)
        master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.build_attrs_list_widget()

        master_layout.addWidget(self.attr_list)

    def build_attrs_list_widget(self):
        self.attr_list = QtWidgets.QListWidget()
        self.attr_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.attr_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.attr_list.model().rowsMoved.connect(lambda: ra.apply_order(self.attr_list, gmi.get_selected_node()))

    def populate(self):
        QtCore.QTimer.singleShot(0, self._refresh)

    def _refresh(self):
        self.attr_list.clear()

        node = gmi.get_selected_node()
        if not node:
            return

        attrs_list = gmi.get_custom_not_hidden_attributes(node)
        for attr in attrs_list:
            self.attr_list.addItem(attr)

    def closeEvent(self, event):
        if self.selection_watcher:
            self.selection_watcher.stop()
        super(ReorderAttributesWindow, self).closeEvent(event)
