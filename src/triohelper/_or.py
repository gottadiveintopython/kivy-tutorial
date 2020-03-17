__all__ = ('or_', 'or2', )


from functools import partial
import trio


async def or_(*coros, **kwargs):
    async with trio.open_nursery() as nursery:
        async def wrapper(coro):
            await coro
            nursery.cancel_scope.cancel()
        for coro in coros:
            nursery.start_soon(partial(wrapper, coro))
        kwargs.get('task_status', trio.TASK_STATUS_IGNORED).started()


async def or2(*async_funcs, **kwargs):
    async with trio.open_nursery() as nursery:
        async def wrapper(async_func, *, task_status=trio.TASK_STATUS_IGNORED):
            await async_func(task_status=task_status)
            nursery.cancel_scope.cancel()
        for async_func in async_funcs:
            await nursery.start(partial(wrapper, async_func))
        kwargs.get('task_status', trio.TASK_STATUS_IGNORED).started()
