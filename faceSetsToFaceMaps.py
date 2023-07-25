# Very small add on to start from

bl_info = {
    "name" : "Face Sets to Maps",
    "description" : "Converts Face Sets in Sculpt Mode into Face Maps",
    "author" : "Amos Joseph",
    "version" : (0, 0, 1),
    "blender" : (3, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "support" : "COMMUNITY",
    "doc_url" : "",
    "category" : "3D View"
}

import bpy
import bmesh
from bpy.types import Operator
from bpy.types import Panel

class FS_FM_operator(Operator):
    """ Converts sculpt mode face sets to face maps """
    bl_idname = "fctofm.operator"
    bl_label = "Face Sets to Maps"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):

        obj = bpy.context.active_object
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        custom_data_layer = bm.faces.layers.int.get('.sculpt_face_set') 

        # only run if we find face sets
        if custom_data_layer:
            # initialize blank list and dictionary for face set info
            facelist = []
            facesets = dict()
            
            # loop through faces and get a unique list of face sets
            for face in bm.faces:
                # check if exists in unique_list or not
        
                if face[custom_data_layer] not in facelist:
                    facelist.append(face[custom_data_layer])

            # create a new face map to match every face set and save their faceset index and  facemap index to a dictionary
            for x in facelist:
                print (x)
                facesetname = "Faceset." + str(x)
                map = obj.face_maps.new(name=facesetname)
                facesets[x] = map.index

            #loop through all faces and update the face map indexes to match the face sets
            fm = bm.faces.layers.face_map.verify()

            for face in bm.faces:
                face[fm] = facesets[face[custom_data_layer]]
            bm.to_mesh(obj.data)
            bm.free()
        else:
            self.report({'INFO'},"No face sets on selected mesh")

        return {'FINISHED'}

class FS_FM_delete_operator(Operator):
    """ Converts sculpt mode face sets to face maps """
    bl_idname = "fctofmdelete.operator"
    bl_label = "Delete Face Maps"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):

        obj = bpy.context.active_object
        maps = obj.face_maps

        for x in maps:
            obj.face_maps.remove(x)

        return {'FINISHED'}

class FS_FM_sidebar(Panel):
    """Display face set button"""
    bl_label = "Face Sets to Maps"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Quad Remesh"

    def draw(self, context):
        col = self.layout.column(align=True)
        prop1 = col.operator(FS_FM_operator.bl_idname, text="Create Face Maps")
        col.separator()
        prop2 = col.operator(FS_FM_delete_operator.bl_idname, text="Delete Face Maps")

classes = [
    FS_FM_operator,
    FS_FM_delete_operator,
    FS_FM_sidebar,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()