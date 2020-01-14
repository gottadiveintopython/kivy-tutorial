__all__ = ('SceneSwitcher', )


class SceneSwitcher:
    def __init__(self, *, nursery, pkgname:str, userdata:dict=None):
        self.nursery = nursery
        self.pkgname = pkgname
        self.modules = {}
        self.userdata = {} if userdata is None else userdata
        self.local_nursery = None
    def switch(self, name):
        from importlib import import_module
        if name not in self.modules:
            self.modules[name] = import_module('.' + name, self.pkgname)
        if self.local_nursery is not None:
            self.local_nursery.cancel_scope.cancel()
            self.local_nursery = None
        self.nursery.start_soon(self._start_scene_inside_local_nursery, name)
    async def _start_scene_inside_local_nursery(self, name):
        import trio
        from functools import partial
        async with trio.open_nursery() as local_nursery:
            self.local_nursery = local_nursery
            local_nursery.start_soon(partial(
                self.modules[name].main,
                self, local_nursery,
                **self.userdata,
            ))
