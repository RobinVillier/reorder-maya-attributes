from maya import cmds

from PySide2 import QtWidgets

from ReorderAttrs.maya_logic import get_maya_items as gmi


def apply_order(attr_list: QtWidgets.QListWidget, node: str):
    """
    Deletes moved attribute and undo.\n
    Then delete any attribute below the one that has been moved, and undo again.\n
    Make sure to unlock and relock any attributes to make sure it doesn't error.
    """

    selected_attr = [attr_list.currentItem().text()]
    delete_later = [attr_list.item(i).text() for i in range(attr_list.count())[attr_list.currentRow() + 1:]]

    delete_attr_list(node, selected_attr)
    delete_attr_list(node, delete_later)


def delete_attr_list(node: str, moved_attr_list: list):
    lock_later = []
    for attr in moved_attr_list:
        cmds.undoInfo(openChunk=True)
        attr_long_name = f"{node}.{attr}"
        lock_state = cmds.getAttr(attr_long_name, lock=True)
        if lock_state:
            cmds.setAttr(attr_long_name, lock=False)
            lock_later.append(attr_long_name)

        cmds.deleteAttr(attr_long_name)

        cmds.undoInfo(openChunk=False)
        cmds.undo()

    for i in lock_later:
        cmds.setAttr(i, lock=True)
