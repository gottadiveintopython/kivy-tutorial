__all__ = ('KTSpeechBubble2', )

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ColorProperty, NumericProperty


Builder.load_string('''
<KTSpeechBubble2>:
    canvas.before:
        Color:
            rgba: self.border_color
        Line:
            rounded_rectangle: [*self.pos, *self.size, self.padding, ]
''')


class KTSpeechBubble2(Widget):
    '''Difference from KTSpeechBubble
    
        - 背景を塗らずに境界線を引く
        - 話し手の口に向かって何も突き出ていない
    '''
    padding = NumericProperty('10dp')
    border_color = ColorProperty("#FFFFFF")
    _trigger_layout = None

    def __init__(self, **kwargs):
        if self._trigger_layout is None:
            trigger_layout = Clock.create_trigger(self.do_layout, -1)
            self._trigger_layout = trigger_layout
        super().__init__(**kwargs)
        fbind = self.fbind
        fbind('padding', trigger_layout)
        fbind('children', trigger_layout)
        fbind('parent', trigger_layout)
        fbind('size', trigger_layout)
        fbind('pos', trigger_layout)

    def on_children(self, __, children):
        if len(children) > 1:
            raise ValueError("KTSpeechBubble2 can have only one child.")

    def do_layout(self, *args):
        if self.children:
            c = self.children[0]
            p = self.padding
            c.x = self.x + p
            c.y = self.y + p
            c.width = self.width - p - p
            c.height = self.height - p - p
