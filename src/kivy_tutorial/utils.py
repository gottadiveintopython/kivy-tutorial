from contextlib import asynccontextmanager


@asynccontextmanager
async def fade_transition(*widgets):
    from triohelper.kivy_awaitable import animate
    first_one = widgets[0]
    bind_uids = [
        first_one.fbind('opacity', w.setter('opacity'))
        for w in widgets[1:]
    ]
    try:
        await animate(first_one, opacity=0, d=.4)
        yield
        await animate(first_one, opacity=1, d=.4)
    finally:
        first_one.opacity = 1
        for uid in bind_uids:
            first_one.unbind_uid('opacity', uid)


def add_border(widget):
    from kivy.graphics import Line, Color
    with widget.canvas.after:
        Color(1, 1, 1, 1)
        line = Line(dash_length=4, dash_offset=8)
    def update_inst(w, *args):
        line.rectangle = [*w.pos, *w.size, ]
    widget.bind(pos=update_inst, size=update_inst)
    update_inst(widget)
