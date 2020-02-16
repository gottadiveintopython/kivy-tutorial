__all__ = ('KTSpeechBubble', )

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import (
    ObjectProperty, VariableListProperty, ColorProperty, NumericProperty,
    ReferenceListProperty,
)


Builder.load_string('''
<KTSpeechBubble>:
    canvas.before:
        Color:
            rgba: self.background_color
        Quad:
            points: self._quad_points
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius:
                (
                (self.padding[0], self.padding[1]),
                (self.padding[2], self.padding[1]),
                (self.padding[2], self.padding[3]),
                (self.padding[0], self.padding[3]),
                )
''')


class KTSpeechBubble(Widget):
    padding = VariableListProperty(['10dp', '10dp', '10dp', '10dp'])
    '''Padding between layout box and children: [padding_left, padding_top,
    padding_right, padding_bottom].

    padding also accepts a two argument form [padding_horizontal,
    padding_vertical] and a one argument form [padding].
    '''

    content = ObjectProperty(None, allownone=True)
    background_color = ColorProperty("#FFFFFF")
    speaker_x = NumericProperty(None, allownone=True)
    speaker_y = NumericProperty(None, allownone=True)
    speaker_pos = ReferenceListProperty(speaker_x, speaker_y)
    _quad_points = ObjectProperty((0, ) * 8)
    _trigger_layout = None
    _trigger_update_points = None

    def __init__(self, **kwargs):
        if self._trigger_layout is None:
            trigger_layout = Clock.create_trigger(self.do_layout, -1)
            self._trigger_layout = trigger_layout
        if self._trigger_update_points is None:
            trigger_update_points = Clock.create_trigger(self._update_points, -1)
            self._trigger_update_points = trigger_update_points
        super().__init__(**kwargs)
        fbind = self.fbind
        fbind('padding', trigger_layout)
        fbind('children', trigger_layout)
        fbind('parent', trigger_layout)
        fbind('size', trigger_layout)
        fbind('pos', trigger_layout)
        fbind('size', trigger_update_points)
        fbind('pos', trigger_update_points)
        fbind('speaker_pos', trigger_update_points)

    def on_children(self, __, children):
        if len(children) > 1:
            raise ValueError("KTSpeechBubble can have only one child.")

    def do_layout(self, *args):
        if self.children:
            c = self.children[0]
            p = self.padding
            c.x = self.x + p[0]
            c.y = self.y + p[3]
            c.width = self.width - p[0] - p[2]
            c.height = self.height - p[1] - p[3]

    def _update_points(self, *args):
        speaker_x, speaker_y = self.speaker_pos
        center_x, center_y = self.center
        if speaker_x is None or speaker_y is None:
            points = (center_x, center_y, ) * 4
        else:
            width_1_8 = self.width / 8
            height_1_8 = self.height / 8
            points = [
                center_x - width_1_8,
                center_y - height_1_8,
                center_x - width_1_8,
                center_y + height_1_8,
                center_x + width_1_8,
                center_y + height_1_8,
                center_x + width_1_8,
                center_y - height_1_8,
            ]
            # relies on True == 1 and False == 0
            index = (0, 6, 2, 4, )[
                (speaker_x > self.center_x) + (speaker_y > self.center_y) * 2
            ]
            points[index:index + 2] = (speaker_x, speaker_y, )
        self._quad_points = points
