bl_info = {
    "name": "DJ Control",
    "author": "Jacob van't Hoog",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "category": "Sequencer",
    }

import pygame.midi
import bpy


class DJControlOperator(bpy.types.Operator):
    bl_idname = "object.dj_control"
    bl_label = "DJ Control"

    def invoke(self, context, event):
        wm = context.window_manager
        self._timer = wm.event_timer_add(1.0/30.0, context.window)
        wm.modal_handler_add(self)
        
        pygame.midi.quit()
        pygame.midi.init()
        self.midi_in = pygame.midi.Input(1)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == "TIMER":
            midi_events = self.midi_in.read(1023)
            for midi_event in midi_events:
                midi_event_data = midi_event[0]
                if midi_event_data[0] == 176 and midi_event_data[1] == 48:
                    speed = midi_event_data[2]
                    if speed > 63:
                        speed -= 128
                    frame = context.scene.frame_current
                    context.scene.frame_set(frame + speed)
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(DJControlOperator)

def unregister():
    bpy.utils.unregister_class(DJControlOperator)

if __name__ == "__main__":
    register()
