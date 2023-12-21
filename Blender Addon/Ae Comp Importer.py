bl_info = {
    "name": "AE Comp Import",
    "author": "Xude",
    "version": (1, 2),
    "blender": (2, 93, 0),
    "location": "File > Import > AE Comp JSON (.json)",
    "description": "Import JSON from Adobe After Effects",
    "category": "Import-Export",
}

import bpy
import json
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty, BoolProperty
from math import radians

def convert_coordinates(ae_coords):
    x, y, z = ae_coords
    return [x / 100, z / 100, -y / 100]

def convert_rotations(ae_rots):
    x, y, z = ae_rots
    return [radians(x), radians(z), radians(-y)]

def convert_time_to_frame(time, fps, startFrame):
    return int(time * fps) + startFrame

def apply_keyframes(obj, keyframe_data, data_path, fps, startFrame):
    for frame_data in keyframe_data:
        time = frame_data['time']
        frame = convert_time_to_frame(time, fps, startFrame)
        if data_path == "rotation_euler":
            value = convert_rotations(frame_data['value'])
        else:
            value = convert_coordinates(frame_data['value'])
        setattr(obj, data_path, value)
        obj.keyframe_insert(data_path=data_path, frame=frame)


def set_active_collection(collection_name):
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)

    # Set the new collection as the active collection
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collection_name]


def create_camera_parent(camera_data, fps, startFrame):
    set_active_collection("Comp from AE")

    bpy.ops.object.empty_add(type='PLAIN_AXES')
    camera_parent = bpy.context.active_object
    camera_parent.name = 'CameraParent'

    apply_keyframes(camera_parent, camera_data['positionKeyframes'], "location", fps, startFrame)
    apply_keyframes(camera_parent, camera_data['rotationKeyframes'], "rotation_euler", fps, startFrame)

    bpy.ops.object.camera_add()
    camera = bpy.context.active_object
    camera.name = 'ImportedCamera'
    camera.parent = camera_parent

    camera.location = (0, 0, 0)
    camera.rotation_euler = (radians(90), 0, 0)
    camera.data.sensor_width = camera_data['sensorWidth']
    camera.data.lens = camera_data['focalLength']

def create_static_object(obj_data):
    set_active_collection("Track Points")

    if obj_data['type'] == 'null':
        bpy.ops.object.empty_add()
    else:
        bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object
    obj.name = obj_data['name']
    position = convert_coordinates(obj_data['position'])
    obj.location = position

def convert_nulls_to_points(objects_data, fps, startFrame):
    mesh = bpy.data.meshes.new(name='TrackPoints_mesh')
    obj = bpy.data.objects.new('TrackPoints_mesh', mesh)
    bpy.context.collection.objects.link(obj)
    vertices = []
    for obj_data in objects_data:
        if obj_data['type'] == 'null':
            position = convert_coordinates(obj_data['position'])
            vertices.append(position)
    mesh.from_pydata(vertices, [], [])
    mesh.update()

def import_ae_json(operator, context, filepath, startFrame, importCam, importTPs, convertNulls):
    with open(filepath, 'r') as file:
        data = json.load(file)
    bpy.context.scene.render.fps = data['fps']
    options = data.get('options', {})
    if options.get('exportCamera', False):
        if importCam:
            create_camera_parent(data['camera'], data['fps'], startFrame)
    if options.get('exportNulls', False):
        if importTPs:   
            if convertNulls:
                convert_nulls_to_points(data.get('objects', []), data['fps'], startFrame)
            else:
                for obj_data in data.get('objects', []):
                    create_static_object(obj_data)
    return {'FINISHED'}

class ImportAEJSON(Operator, ImportHelper):
    bl_idname = "import_scene.ae_json"
    bl_label = "Import AE Comp"
    filename_ext = ".json"
    filter_glob: StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)
    startFrame: IntProperty(name="Start Frame", description="Start frame for the animation", default=1)
    importCam: BoolProperty(name="Import Camera", description="Import Camera data if available", default=True)
    importTPs: BoolProperty(name="Import TrackPoints", description="Import TrackPoints if available", default=True)
    convertNulls: BoolProperty(name="Convert Nulls to Points", description="Convert After Effects nulls to points in a mesh", default=False)


    def execute(self, context):
        return import_ae_json(self, context, self.filepath, self.startFrame, self.importCam, self.importTPs, self.convertNulls)

def menu_func_import(self, context):
    self.layout.operator(ImportAEJSON.bl_idname, text="AE Comp JSON (.json)")

def register():
    bpy.utils.register_class(ImportAEJSON)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportAEJSON)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()
