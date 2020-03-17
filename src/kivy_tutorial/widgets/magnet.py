'''
Trio version of:
https://github.com/kivy-garden/garden.magnet
'''
__all__ = ('KTMagnet', )

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ListProperty
from triohelper.triouser import TrioUser


class KTMagnet(TrioUser, Widget):
    duration = NumericProperty(1)
    transition = StringProperty('out_quad')
    anim_props = ListProperty(['pos', 'size', ])

    def __init__(self, **kwargs):
        from kivy.clock import Clock
        super().__init__(**kwargs)
        self._props_watching = {}
        self._trigger_start_anim = \
            Clock.create_trigger(self._start_anim, -1)
        self.bind(anim_props=self._on_anim_props)
        self.property('anim_props').dispatch(self)
        self._sub_nursery = None
        
    def _on_anim_props(self, __, anim_props):
        for prop, uid in self._props_watching.items():
            self.unbind_uid(prop, uid)
        self._props_watching = {
            prop: self.fbind(prop, self._trigger_start_anim)
            for prop in anim_props
        }

    def on_children(self, *args):
        if len(self.children) > 1:
            raise ValueError('Magnet can have only one child')
        self._trigger_start_anim()

    def _start_anim(self, *args):
        if self._sub_nursery is not None:
            self._sub_nursery.cancel_scope.cancel()
            self._sub_nursery = None
        if self.children:
            self.nursery.start_soon(self._start_anim_core)

    async def _start_anim_core(self):
        from functools import partial
        import trio
        from triohelper.kivy_awaitable import animation
        child = self.children[0]
        async with trio.open_nursery() as sub_nursery:
            self._sub_nursery = sub_nursery
            sub_nursery.start_soon(partial(
                animation, child,
                d=self.duration,
                t=self.transition,
                **{prop: getattr(self, prop) for prop in self.anim_props}
            ))
