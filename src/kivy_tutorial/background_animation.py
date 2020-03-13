__all__ = ('play', )


async def play(
        *, widget, canvas=None, max_sprites=1000, color='#FFFFFF',
        pointsize=1, image='', random=None, max_spawn_interval=.1,
        max_velocity_y=60):
    import trio
    await trio.sleep(0)
    
    if random is None:
        from random import Random
        random = Random()
    if canvas is None:
        canvas = widget.canvas.before

    from array import array
    visible_arr = array('B', [0, ] * max_sprites)
    x_arr = array('f', [0., ] * max_sprites)
    y_arr = array('f', [0., ] * max_sprites)
    velocity_y_arr = array('f', [0., ] * max_sprites)

    from kivy.utils import get_color_from_hex
    from kivy.graphics import Point, Color
    with canvas:
        color_inst = Color(*get_color_from_hex(color))
        point_inst = Point(pointsize=pointsize, source=image)

    async def _spawn_sprite():
        from trio import sleep
        r = random
        min_x = min_y = -pointsize
        while True:
            await sleep(r.random() * max_spawn_interval)
            try:
                # 空いているslotのindexを求める
                i = visible_arr.index(0)
            except ValueError:
                continue
            max_x = int(widget.width + pointsize)
            max_y = widget.height + pointsize
            velocity_y = float(r.randint(1, max_velocity_y) * r.choice((1, -1)))
            velocity_y_arr[i] = velocity_y
            x_arr[i] = r.randint(min_x, max_x)
            y_arr[i] = min_y if velocity_y >= 0. else max_y
            visible_arr[i] = 1

    async def _remove_sprite_if_its_outside_of_the_widget():
        from trio import sleep
        from itertools import compress, count
        min_y = -pointsize
        while True:
            await sleep(2)
            max_y = widget.height + pointsize
            for i in compress(count(), visible_arr):
                y = y_arr[i]
                velocity_y = velocity_y_arr[i]
                if (velocity_y < 0 and y < min_y) or \
                        (velocity_y > 0 and y > max_y):
                    visible_arr[i] = 0

    async def _move_sprites():
        from trio import sleep
        from time import perf_counter as get_current_time
        from itertools import compress, count, chain
        chain_from_iterable = chain.from_iterable

        last = get_current_time()
        while True:
            await sleep(0)
            current = get_current_time()
            delta = current - last
            last = current
            for i in compress(count(), visible_arr):
                y_arr[i] += velocity_y_arr[i] * delta
            # 描画命令を更新
            point_inst.points = tuple(chain_from_iterable(
                compress(zip(x_arr, y_arr), visible_arr)))
    
    try:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(_spawn_sprite)
            nursery.start_soon(_remove_sprite_if_its_outside_of_the_widget)
            nursery.start_soon(_move_sprites)
    finally:
        canvas.remove(point_inst)
        canvas.remove(color_inst)