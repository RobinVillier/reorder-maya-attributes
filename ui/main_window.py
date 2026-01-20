from pathlib import Path

from PySide2 import QtWidgets, QtCore

from ReorderAttrs.config import load
from ReorderAttrs.maya_logic import get_custom_attributes as ra

_ROOT_DIR = Path(__file__).parent.parent


class ReorderAttributesWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ReorderAttributesWindow, self).__init__(parent)

        self.setWindowTitle("Reorder Custom Attributes")
        self.setMinimumWidth(300)

        print('hello world')

        stylesheet = load.load_stylesheet(f"{_ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.build_ui()
        self.populate()

    def build_ui(self):
        master_layout = QtWidgets.QVBoxLayout(self)
        master_layout.setContentsMargins(0, 0, 0, 0)
        master_layout.setSpacing(0)
        master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.build_attrs_list()
        self.build_buttons()

        master_layout.addWidget(self.attr_list)
        master_layout.addLayout(self.buttons_layout)

    def build_attrs_list(self):
        self.attr_list = QtWidgets.QListWidget()
        self.attr_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.attr_list.setDefaultDropAction(QtCore.Qt.MoveAction)

    def build_buttons(self):
        refresh_btn = QtWidgets.QPushButton("Refresh Selection")
        apply_btn = QtWidgets.QPushButton("Apply Order")

        refresh_btn.clicked.connect(self.populate)
        apply_btn.clicked.connect(self.apply_order)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addWidget(refresh_btn)
        self.buttons_layout.addWidget(apply_btn)

    def populate(self):
        self.attr_list.clear()

        node = ra.get_selected_node()
        if not node:
            return

        attrs = ra.get_custom_attributes(node)
        for attr in attrs:
            item = QtWidgets.QListWidgetItem(attr)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.attr_list.addItem(item)

    def apply_order(self):
        node = ra.get_selected_node()
        if not node:
            return

        ordered_attrs = [
            self.attr_list.item(i).text()
            for i in range(self.attr_list.count())
        ]

        print("New order:", ordered_attrs)
        # Étape suivante : rebuild réel des attributs
