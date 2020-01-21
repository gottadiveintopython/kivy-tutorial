# numpyを用いているがそれによって効率が上がったは確めていない。
# 単にnumpyを学ぶ為に用いた。

__all__ = ('play', )

sprite_dtype = [
    ('velocity_y', float, ),
    ('x', float, ),
    ('y', float, ),
    ('visible', bool, )
]

async def play(*, parent, nursery, max_sprites=200):
    import numpy as np
    import trio
    from kivy.graphics import Point, Color
    target_canvas = parent.canvas.before
    with target_canvas:
        color_inst = Color(1, 1, 1, .3, )
        point_inst = Point(pointsize=1)
    sprites = np.zeros(shape=(max_sprites, ), dtype=sprite_dtype)

    async def _spawn_sprite():
        from random import Random
        r = Random()
        sleep = trio.sleep
        while True:
            await sleep(r.random() * .1)
            indices = (sprites['visible'] == 0).nonzero()[0]
            if len(indices) == 0:
                continue
            sprite = sprites[indices[0]]
            velocity_y = float(r.randint(1, 60) * r.choice((1, -1)))
            sprite['velocity_y'] = velocity_y
            sprite['x'] = r.randint(0, parent.width)
            sprite['y'] = 0 if velocity_y >= 0. else parent.height
            sprite['visible'] = True

    async def _remove_sprite_if_its_outside_of_the_parent():
        sleep = trio.sleep
        while True:
            await sleep(2)
            sprites['visible'][
                np.logical_and(
                    sprites['visible'] != False,
                    np.logical_or(
                        np.logical_and(
                            sprites['y'] < 0,
                            sprites['velocity_y'] < 0,
                        ),
                        np.logical_and(
                            sprites['y'] > parent.height,
                            sprites['velocity_y'] > 0,
                        ),
                    )
                )
            ] = False

    async def _move_sprites():
        from numpy.lib.recfunctions import structured_to_unstructured
        sleep = trio.sleep
        get_current_time = trio.current_time
        last_time = get_current_time()
        while True:
            await sleep(0)
            current_time = get_current_time()
            delta_time = current_time - last_time
            indices = sprites['visible'].nonzero()[0]
            sprites['y'][indices] += sprites['velocity_y'][indices] * delta_time
            pos_array = structured_to_unstructured(sprites[['x', 'y']][indices])
            point_inst.points = [] if len(pos_array) == 0 else [*pos_array.flat]
            last_time = current_time

    try:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(_spawn_sprite)
            nursery.start_soon(_remove_sprite_if_its_outside_of_the_parent)
            nursery.start_soon(_move_sprites)
    finally:
        target_canvas.remove(point_inst)
        target_canvas.remove(color_inst)
