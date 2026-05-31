# __init__.py

bl_info = {
    "name": "Mesh Integrity Toolkit",
    "author": "Gabriel d'Alençon (with AI assistant)",
    "version": (16, 0, 0),
    "blender": (2, 83, 0),
    "location": "View3D > Edit Mode > Right-click Context Menu > Mesh Integrity",
    "description": "A set of tools to fix common topology issues, "
                   "such as vertices overlapping edges and overlapping faces.",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

import bpy

# Imports the classes from the tool files
from .connect_overlaps import MESH_OT_connect_overlaps_auto

# --- Submenu ---
class VIEW3D_MT_mesh_integrity_submenu(bpy.types.Menu):
    bl_label = "Mesh Integrity"
    bl_idname = "VIEW3D_MT_mesh_integrity_submenu"

    def draw(self, context):
        layout = self.layout
        layout.operator(MESH_OT_connect_overlaps_auto.bl_idname)

# --- Registration ---
def menu_draw_call(self, context):
    self.layout.menu(VIEW3D_MT_mesh_integrity_submenu.bl_idname)

# List of all classes Blender needs to know about
classes = [
    MESH_OT_connect_overlaps_auto,
    VIEW3D_MT_mesh_integrity_submenu,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Adds our submenu to the right-click context menu
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_draw_call)

def unregister():
    # Removes our submenu
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_draw_call)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
