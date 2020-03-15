__all__ = ('new_cancel_scope', )
from functools import wraps
import trio

def new_cancel_scope(async_fn):
    @wraps(async_fn)
    async def wrapper(*args, **kwargs):
        task_status = kwargs.pop('task_status', trio.TASK_STATUS_IGNORED)
        with trio.CancelScope() as scope:
            task_status.started(scope)
            await async_fn(*args)
    return wrapper
