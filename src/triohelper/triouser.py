__all__ = ('TrioUser', 'activate_nursery', )

from contextlib import contextmanager


class TrioUser:
    def __init__(self, *args, **kwargs):
        nursery = kwargs.pop('nursery', None)
        self.nursery = nursery or _get_current_nursery()
        super().__init__(*args, **kwargs)


_nursery_stack = []


@contextmanager
def activate_nursery(nursery):
    _nursery_stack.append(nursery)
    try:
        yield nursery
    finally:
        _nursery_stack.pop()


def _get_current_nursery():
    return _nursery_stack[-1]
