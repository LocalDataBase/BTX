bl_info = {
    "name": "BTX (Batch Texture Exporter)",
    "description": "Export textures from selected objects in a scene.",
    "author": "StayWithMe",
    "blender": (4, 0, 0),
    "version": (1, 0, 0),
    "warning": "",
    "location": "View3D > N-Panel > Tool > Batch Texture Exporter",
    "category": "Tool",
    "doc_url": "https://github.com/LocalDataBase/BTX",
    "tracker_url": "https://github.com/LocalDataBase/BTX/issues",
}

from . import batch_texture_exporter

def register():
    batch_texture_exporter.register()

def unregister():
    batch_texture_exporter.unregister()

if __name__ == "__main__":
    register()