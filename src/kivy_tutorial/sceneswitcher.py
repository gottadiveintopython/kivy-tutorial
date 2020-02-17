__all__ = ('SceneSwitcher', )

from kivy_tutorial.triouser import TrioUser


class SceneSwitcher(TrioUser):
    def __init__(self, *, pkgname:str, userdata:dict=None, **kwargs):
        super().__init__(**kwargs)
        self.pkgname = pkgname
        self.userdata = {} if userdata is None else userdata
        self.local_nursery = None
    def switch(self, name):
        from importlib import import_module
        module = import_module('.' + name, self.pkgname)
        if self.local_nursery is not None:
            self.local_nursery.cancel_scope.cancel()
            self.local_nursery = None
        self.nursery.start_soon(self._start_scene_inside_local_nursery, module)
    async def _start_scene_inside_local_nursery(self, module):
        import trio
        from functools import partial
        async with trio.open_nursery() as local_nursery:
            self.local_nursery = local_nursery
            local_nursery.start_soon(partial(
                module.main,
                self, local_nursery,
                **self.userdata,
            ))
