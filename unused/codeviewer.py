'''KTCodeViewerの初期版。背景色をpygmentsのstyleの指定通りに塗る'''

__all__ = ('KTCodeViewer', )

from kivy.clock import Clock
from kivy.properties import (
    StringProperty, ObjectProperty, OptionProperty, NumericProperty,
    ColorProperty, ReferenceListProperty,
)
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from pygments import highlight
from pygments import lexers
from pygments import styles
from pygments.formatters import BBCodeFormatter

Builder.load_string(r'''
<KTCodeViewer>:
    minimum_size: label.texture_size
    canvas.before:
        Color:
            rgba: self._background_color
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        id: label
        pos: root.pos
        size: root.size
        markup: True
        font_name: root.font_name
        font_size: root.font_size
        color: root._text_color
''')


class KTCodeViewer(Widget):
    text = StringProperty()
    minimum_width = NumericProperty()
    minimum_height = NumericProperty()
    minimum_size = ReferenceListProperty(minimum_width, minimum_height)
    font_size = NumericProperty(Label.font_size.defaultvalue)
    font_name = StringProperty(Label.font_name.defaultvalue)
    lexer = ObjectProperty()
    style = ObjectProperty()
    style_name = OptionProperty(
        'default', options=tuple(styles.get_all_styles()))
    _background_color = ColorProperty()
    _text_color = ColorProperty()

    def __init__(self, **kwargs):
        self._trigger_update_text = trigger = \
            Clock.create_trigger(self._update_text, -1)
        f = self.fbind
        f('lexer', trigger)
        f('text', trigger)
        super().__init__(**kwargs)

    def on_style_name(self, *args):
        self.style = styles.get_style_by_name(self.style_name)

    def on_style(self, __, style):
        self._formatter = BBCodeFormatter(style=style)
        bg_color = get_color_from_hex(style.background_color)
        self._background_color = bg_color
        self._text_color = _get_text_color_from_background_color(bg_color)
        self._trigger_update_text()

    def _update_text(self, *args):
        self.ids.label.text = highlight(
            self.text, self.lexer, self._formatter)


def _get_text_color_from_background_color(bg_color):
    return (1, 1, 1, 1) if sum(bg_color[:3]) < 1.5 else (0, 0, 0, 1)
