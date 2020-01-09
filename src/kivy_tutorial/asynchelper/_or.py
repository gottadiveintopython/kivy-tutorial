__all__ = ('or_', )


from functools import partial
import trio

async def or_(*coros):
    async with trio.open_nursery() as nursery:
        async def wrapper(coro):
            await coro
            nursery.cancel_scope.cancel()
        for coro in coros:
            nursery.start_soon(partial(wrapper, coro))
