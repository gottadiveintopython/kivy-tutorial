__all__ = ('KTCodeLabel', )

from kivy.clock import Clock
from kivy.properties import (
    StringProperty, NumericProperty, ColorProperty, ReferenceListProperty,
)
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy_tutorial import theme

Builder.load_string(r'''
<KTCodeLabel>:
    minimum_size: label.texture_size
    Label:
        id: label
        pos: root.pos
        size: root.size
        markup: True
        font_name: root.font_name
        font_size: root.font_size
''')

class KTCodeLabel(Widget):
    text = StringProperty()
    minimum_width = NumericProperty()
    minimum_height = NumericProperty()
    minimum_size = ReferenceListProperty(minimum_width, minimum_height)
    font_size = NumericProperty(theme.code_font_size)
    font_name = StringProperty(theme.code_font_name)
    lexer_name = StringProperty()

    def __init__(self, **kwargs):
        from pygments.formatters import BBCodeFormatter
        from pygments.styles import get_style_by_name
        self._formatter = BBCodeFormatter(style=get_style_by_name('monokai'))
        self._trigger_update_text = Clock.create_trigger(self._update_text, -1)
        super().__init__(**kwargs)

    def on_text(self, *args):
        self._trigger_update_text()

    def on_lexer_name(self, __, name):
        from kivy.extras.highlight import KivyLexer
        from pygments.lexers import get_lexer_by_name
        self._lexer = KivyLexer() if name.lower() == 'kivy' \
            else get_lexer_by_name(name)
        self._trigger_update_text()

    def _update_text(self, *args):
        from pygments import highlight
        self.ids.label.text = highlight(
            self.text, self._lexer, self._formatter)


def _get_text_color_from_background_color(bg_color):
    return (1, 1, 1, 1) if sum(bg_color[:3]) < 1.5 else (0, 0, 0, 1)