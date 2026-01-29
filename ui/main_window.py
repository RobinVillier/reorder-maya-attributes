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
        self.build_up_down_buttons()

        master_layout.addWidget(self.attr_list)
        master_layout.addLayout(self.up_down_layout)

    def build_attrs_list_widget(self):
        self.attr_list = QtWidgets.QListWidget()
        self.attr_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.attr_list.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.attr_list.model().rowsMoved.connect(lambda: ra.apply_order(self.attr_list, gmi.get_selected_node()))

    def build_up_down_buttons(self):
        down_button = QtWidgets.QPushButton()
        down_button.setIcon(QtGui.QIcon(f"{_ROOT_DIR}/resources/icons/down_arrow_white.png"))
        down_button.setObjectName("down_button")
        down_button.clicked.connect(self.move_item_down)

        up_button = QtWidgets.QPushButton()
        up_button.setIcon(QtGui.QIcon(f"{_ROOT_DIR}/resources/icons/up_arrow_white.png"))
        up_button.setObjectName("up_button")
        up_button.clicked.connect(self.move_item_up)

        self.up_down_layout = QtWidgets.QHBoxLayout()
        self.up_down_layout.addWidget(down_button)
        self.up_down_layout.addWidget(up_button)

    def populate(self):
        QtCore.QTimer.singleShot(0, self._refresh)

    def _refresh(self):
        self.attr_list.clear()

        node = gmi.get_selected_node()
        if not node:
            return

        attrs_list = gmi.get_custom_non_hidden_attributes(node)
        for attr in attrs_list:
            self.attr_list.addItem(attr)

    def move_item_down(self):
        current_row = self.attr_list.currentRow()
        if current_row < 0 or current_row >= self.attr_list.count() - 1:
            return

        item = self.attr_list.takeItem(current_row)
        self.attr_list.insertItem(current_row + 1, item)
        self.attr_list.setCurrentRow(current_row + 1)

        ra.apply_order(self.attr_list, gmi.get_selected_node())

    def move_item_up(self):
        current_row = self.attr_list.currentRow()
        if current_row <= 0:
            return

        item = self.attr_list.takeItem(current_row)
        self.attr_list.insertItem(current_row - 1, item)
        self.attr_list.setCurrentRow(current_row - 1)

        ra.apply_order(self.attr_list, gmi.get_selected_node())

    def closeEvent(self, event):
        if self.selection_watcher:
            self.selection_watcher.stop()
        super(ReorderAttributesWindow, self).closeEvent(event)
