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

handler_active = False
midi_in = None
midi_out = None
last_update_time = -1.0

def get_area_context(name):
    for area in bpy.context.screen.areas:
        if area.type == name:
            ctx = bpy.context.copy()
            ctx['area'] = area
            ctx['region'] = area.regions[-1]
            return ctx

def dj_update(scene):
    global midi_in, last_update_time
    t = time.time()
    if t - last_update_time < 1.0/30.0:
        return
    last_update_time = t

    midi_events = midi_in.read(1023)
    for midi_event in midi_events:
        midi_event_data = midi_event[0]
        if midi_event_data[0] == 176:
            # control change
            if midi_event_data[1] == 48:
                # JOG_DA
                speed = midi_event_data[2]
                if speed > 63:
                    speed -= 128
                frame = scene.frame_current
                scene.frame_set(frame + speed)
            elif midi_event_data[1] == 49:
                # JOG_DB
                speed = midi_event_data[2]
                if speed > 63:
                    speed -= 128
                bpy.ops.transform.seq_slide(get_area_context('SEQUENCE_EDITOR'),
                    value=(speed, 0))


class DJStartOperator(bpy.types.Operator):
    DEVICE_NAME = b'Hercules DJControl Instinct'

    bl_idname = "object.dj_start"
    bl_label = "Start DJ Control"

    bl_options = {'REGISTER'}

    def execute(self, context):
        global midi_in, midi_out, handler_active
        stop()
        pygame.midi.init()

        input_device = -1
        output_device = -1

        print("MIDI Devices:")
        num_devices = pygame.midi.get_count()
        for device_i in range(0, num_devices):
            info = pygame.midi.get_device_info(device_i)
            # (interface name, device name, is input?, is output?, in use?)
            print(device_i, info)
            if info[1] == DJStartOperator.DEVICE_NAME:
                if info[4]:
                    self.report({'ERROR'}, "Device is already in use!")
                    pygame.midi.quit()
                    return {'CANCELLED'}
                if info[2]:
                    input_device = device_i
                elif info[3]:
                    output_device = device_i
        print("Input device:", input_device)
        print("Output device:", output_device)

        if input_device == -1:
            self.report({'ERROR'}, "Couldn't find input device!")
            pygame.midi.quit()
            return {'CANCELLED'}
        if output_device == -1:
            self.report({'ERROR'}, "Couldn't find output device!")
            pygame.midi.quit()
            return {'CANCELLED'}

        midi_in = pygame.midi.Input(input_device)
        midi_out = pygame.midi.Output(output_device)
        bpy.app.handlers.scene_update_pre.append(dj_update)
        handler_active = True

        return {'FINISHED'}


def stop():
    global midi_in, midi_out, handler_active
    print("Stop DJ Control")

    if midi_in is not None:
        midi_in.close()
        midi_in = None
    if midi_out is not None:
        midi_out.close()
        midi_out = None
    if handler_active:
        bpy.app.handlers.scene_update_pre.remove(dj_update)
        handler_active = False
    pygame.midi.quit()

class DJStopOperator(bpy.types.Operator):
    bl_idname = "object.dj_stop"
    bl_label = "Stop DJ Control"

    bl_options = {'REGISTER'}

    def execute(self, context):
        stop()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(DJStartOperator)
    bpy.utils.register_class(DJStopOperator)

def unregister():
    bpy.utils.unregister_class(DJStartOperator)
    bpy.utils.unregister_class(DJStopOperator)
    stop()

if __name__ == "__main__":
    register()
