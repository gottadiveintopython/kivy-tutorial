__all__ = ('async_event', )

from trio import Event


async def async_event(ed, name, *, filter=None, return_value=None, wants_kwargs=False):
    def _callback(*args, **kwargs):
        nonlocal parameter
        if (filter is not None) and not filter(*args, **kwargs):
            return
        parameter = (args, kwargs, )
        ed.unbind_uid(name, bind_id)
        event.set()
        return return_value

    parameter = None
    bind_id = ed.fbind(name, _callback)
    assert bind_id > 0  # check if binding succeeded
    event = Event()
    await event.wait()
    return parameter if wants_kwargs else parameter[0]
