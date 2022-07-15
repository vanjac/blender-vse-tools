bl_info = {
    "name": "Titler",
    "author": "chroma zone",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "category": "Sequencer",
    }

import bpy
import wand.image

def make_title(self, context):
    svg = ""
    for line in context.edit_text.lines:
        svg += line.body + "\n"
    filename = bpy.path.abspath('//' + context.edit_text.name + '.png')
    with wand.image.Image(blob=svg.encode('utf-8'), format='svg') as img:
        img.save(filename=filename)
    return filename

class TEXT_MT_make_title(bpy.types.Operator):
    """Save SVG as an image"""
    bl_idname = "text.make_title"
    bl_label = "Update Title"
    bl_options = {'REGISTER'}

    def execute(self, context):
        make_title(self, context)
        return {'FINISHED'}

def make_title_menu(self, context):
    self.layout.operator(
        TEXT_MT_make_title.bl_idname)

def register():
    bpy.utils.register_class(TEXT_MT_make_title)
    bpy.types.TEXT_MT_edit.append(make_title_menu)

def unregister():
    bpy.utils.unregister_class(TEXT_MT_make_title)
    bpy.types.TEXT_MT_edit.remove(make_title_menu)

if __name__ == "__main__":
    register()
