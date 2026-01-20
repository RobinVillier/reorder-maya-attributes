import maya.cmds as cmds


def get_selected_node():
    sel = cmds.ls(selection=True)
    return sel[0] if sel else None


def get_custom_attributes(node):
    attrs = cmds.listAttr(node, userDefined=True) or []
    return attrs
