__all__ = ('SceneSwitcher', )

import trio
import asynckivy as ak
from asynckivy.compatibility.trio import run_coro_under_trio
from triohelper.triouser import TrioUser


class SceneSwitcher(TrioUser):
    def __init__(self, *, pkgname:str, userdata:dict=None, **kwargs):
        super().__init__(**kwargs)
        self.pkgname = pkgname
        self.userdata = {} if userdata is None else userdata
        self._child_nursery = None
        self._next_scene_name = None

    def ask_to_switch(self, next_scene_name):
        self._next_scene_name = next_scene_name
        self._child_nursery.cancel_scope.cancel()

    async def attach(self, widget, *, task_status=trio.TASK_STATUS_IGNORED):
        from importlib import import_module
        from functools import partial
        import trio
        from triohelper import animate

        widget.opacity = 0
        async with trio.open_nursery() as child_nursery:
            self._child_nursery = child_nursery
            child_nursery.start_soon(trio.sleep_forever)
            task_status.started()
        next_scene_name = self._next_scene_name

        while True:
            module = import_module(
                '.' + next_scene_name,
                self.pkgname,
            )
            async with trio.open_nursery() as child_nursery:
                self._child_nursery = child_nursery
                await child_nursery.start(partial(
                    module.main,
                    self, child_nursery,
                    **self.userdata,
                ))
                await animate(widget, opacity=1, d=.3)
            next_scene_name = self._next_scene_name
            await animate(widget, opacity=0, d=.3)
            widget.clear_widgets()
            await trio.sleep(.1)
