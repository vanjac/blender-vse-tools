bl_info = {
    "name": "DJ Control",
    "author": "Jacob van't Hoog",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "category": "Sequencer",
    }

import time
import pygame.midi
import bpy

midi_in = None
last_update_time = -1.0


def dj_update(scene):
    global midi_in, last_update_time
    t = time.time()
    if t - last_update_time < 1.0/30.0:
        return
    last_update_time = t

    midi_events = midi_in.read(1023)
    for midi_event in midi_events:
        midi_event_data = midi_event[0]
        if midi_event_data[0] == 176 and midi_event_data[1] == 48:
            speed = midi_event_data[2]
            if speed > 63:
                speed -= 128
            frame = scene.frame_current
            scene.frame_set(frame + speed)


class DJStartOperator(bpy.types.Operator):
    bl_idname = "object.dj_start"
    bl_label = "Start DJ Control"

    bl_options = {'REGISTER'}

    device = bpy.props.IntProperty(
        name="Device",
        description="MIDI Device",
        min=0, max=99,
        default=1)

    def invoke(self, context, event):
        pygame.midi.quit()
        pygame.midi.init()
        num_devices = pygame.midi.get_count()
        print("INPUT DEVICES")
        for device_i in range(0, num_devices):
            info = pygame.midi.get_device_info(device_i)
            if info[2]:
                print("Device " + str(device_i) + ":", info[1],
                    "(ALREADY OPEN!)" if info[4] else "")

        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        global midi_in
        print("Start DJ Control")

        if midi_in is None:
            bpy.app.handlers.scene_update_pre.append(dj_update)
        midi_in = pygame.midi.Input(self.device)

        return {'FINISHED'}


class DJStopOperator(bpy.types.Operator):
    bl_idname = "object.dj_stop"
    bl_label = "Stop DJ Control"

    bl_options = {'REGISTER'}

    def execute(self, context):
        global midi_in
        print("Stop DJ Control")

        if midi_in is not None:
            print("Closing stream")
            midi_in.close()
            midi_in = None
            bpy.app.handlers.scene_update_pre.remove(dj_update)
        pygame.midi.quit()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(DJStartOperator)
    bpy.utils.register_class(DJStopOperator)

def unregister():
    bpy.utils.unregister_class(DJStartOperator)
    bpy.utils.unregister_class(DJStopOperator)

if __name__ == "__main__":
    register()
