__all__ = ('new_nursery', )
from functools import wraps, partial
import trio

def new_nursery(async_fn):
    '''新しくnurseryを作ってその中で渡されたasync_fnを実行するasync関数を返す。
    async_fnには'new_nursery'という名前のkeyword引数としてそのnursery
    が渡される。基本decorator構文で利用すべし。
    '''
    @wraps(async_fn)
    async def wrapper(*args, **kwargs):
        task_status = kwargs.pop('task_status', trio.TASK_STATUS_IGNORED)
        async with trio.open_nursery() as nursery:
            nursery.start_soon(partial(
                async_fn,
                *args,
                new_nursery=nursery,
                **kwargs,
            ))
            task_status.started(nursery)
    return wrapper
