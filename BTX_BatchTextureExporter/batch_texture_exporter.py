import bpy
import os
import shutil
from bpy.props import StringProperty, BoolProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup

def update_directory(self, context):
    if self.directory:
        abs_path = os.path.abspath(bpy.path.abspath(self.directory))
        self.directory = abs_path

class TextureExportSettings(PropertyGroup):
    directory: StringProperty(
        name="Output Directory",
        description="Select directory for texture copies",
        subtype='DIR_PATH',
        default="//Textures",
        update=update_directory
    )

    create_subfolder: BoolProperty(
        name="Create Subfolder",
        description="Create a subfolder with object's name",
        default=True
    )

    overwrite: BoolProperty(
        name="Overwrite Existing",
        description="Overwrite existing files",
        default=False
    )

    symlink: BoolProperty(
        name="Create Symlinks",
        description="Create symbolic links instead of copies",
        default=False
    )

class TEXTURE_OT_CopyTextures(Operator):
    """Copy all textures from selected objects"""
    bl_idname = "texture.copy_textures"
    bl_label = "Export Textures"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.texture_export_settings
        directory = settings.directory

        if not directory:
            self.report({'ERROR'}, "Output directory not specified")
            return {'CANCELLED'}

        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        copied_count = 0
        skipped_count = 0
        error_count = 0

        def process_image(img, export_dir):
            nonlocal copied_count, skipped_count, error_count
            if img and img.filepath_raw:
                src_path = bpy.path.abspath(img.filepath_raw)
                if os.path.exists(src_path):
                    dst_path = os.path.join(export_dir, os.path.basename(src_path))

                    if os.path.exists(dst_path) and os.path.islink(dst_path):
                        if settings.overwrite and not settings.symlink:
                            try:
                                os.remove(dst_path)
                            except Exception as e:
                                error_count += 1
                                self.report({'ERROR'}, f"Failed to remove symlink {dst_path}: {str(e)}")
                                return

                    try:
                        if os.path.exists(dst_path) and os.path.samefile(src_path, dst_path):
                            skipped_count += 1
                            return
                    except FileNotFoundError:
                        pass

                    if not settings.overwrite and os.path.exists(dst_path):
                        skipped_count += 1
                        return

                    try:
                        if settings.symlink:
                            if os.path.exists(dst_path):
                                os.remove(dst_path)
                            os.symlink(src_path, dst_path)
                        else:
                            shutil.copy2(src_path, dst_path)
                        copied_count += 1
                    except Exception as e:
                        error_count += 1
                        self.report({'ERROR'}, f"Failed to copy {img.name}: {str(e)}")

        for obj in selected_objects:
            if obj.type not in {'MESH', 'FONT'}:
                continue

            export_dir = os.path.join(directory, obj.name) if settings.create_subfolder else directory
            os.makedirs(export_dir, exist_ok=True)

            materials = []
            if obj.type == 'MESH':
                materials = [m.material for m in obj.material_slots if m.material]
            elif obj.type == 'FONT' and hasattr(obj.data, 'materials'):
                materials = [m for m in obj.data.materials if m]

            for mat in materials:
                if mat and mat.use_nodes:
                    for node in mat.node_tree.nodes:
                        if hasattr(node, 'image') and node.image:
                            process_image(node.image, export_dir)

        msg = f"Copied {copied_count} textures"
        if skipped_count:
            msg += f", skipped {skipped_count}"
        if error_count:
            msg += f", errors: {error_count}"
        
        self.report({'INFO'}, msg)
        return {'FINISHED'}

class TEXTURE_PT_Panel(Panel):
    bl_label = "Batch Texture Exporter"
    bl_idname = "TEXTURE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.texture_export_settings

        layout.prop(settings, "directory", text="Output Directory")
        layout.prop(settings, "create_subfolder")
        layout.prop(settings, "overwrite")
        layout.prop(settings, "symlink")

        layout.separator()
        layout.operator("texture.copy_textures", icon='EXPORT')

def register():
    bpy.utils.register_class(TextureExportSettings)
    bpy.types.Scene.texture_export_settings = PointerProperty(type=TextureExportSettings)

    bpy.utils.register_class(TEXTURE_OT_CopyTextures)
    bpy.utils.register_class(TEXTURE_PT_Panel)

def unregister():
    bpy.utils.unregister_class(TEXTURE_PT_Panel)
    bpy.utils.unregister_class(TEXTURE_OT_CopyTextures)

    del bpy.types.Scene.texture_export_settings
    bpy.utils.unregister_class(TextureExportSettings)

if __name__ == "__main__":
    register()
