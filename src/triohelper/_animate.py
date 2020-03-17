__all__ = ('animation', )

import trio


async def animation(target, *, task_status=trio.TASK_STATUS_IGNORED, **kwargs):
    '''kivy.animation.Animationを真似たもの

    warning:
        これはkivyの時計を使わずにtrioの時計を使っているので、描画関係には使うべきでは無い。
        そういった場合は代わりに 'triohelper.kivy_awaitable.animate()' を使うこと。
    '''
    from trio import sleep, current_time as get_current_time
    from kivy.animation import AnimationTransition
    from asynckivy._animation._simple_ver import _calculate
    duration = kwargs.pop('d', kwargs.pop('duration', 1.))
    transition = kwargs.pop('t', kwargs.pop('transition', 'linear'))
    step = kwargs.pop('s', kwargs.pop('step', 0))
    force_final_value = kwargs.pop('force_final_value', False)
    if isinstance(transition, str):
        transition = getattr(AnimationTransition, transition)
    animated_properties = kwargs

    # get current values
    properties = {}
    for key, value in animated_properties.items():
        original_value = getattr(target, key)
        if isinstance(original_value, (tuple, list)):
            original_value = original_value[:]
        elif isinstance(original_value, dict):
            original_value = original_value.copy()
        properties[key] = (original_value, value)

    task_status.started()

    if not duration:
        await sleep(0)
        for key, values in properties.items():
            a, b = values
            setattr(target, key, b)
        return

    start_time = get_current_time()
    try:
        while True:
            await sleep(step)

            # calculate progression
            progress = min(1., (get_current_time() - start_time) / duration)
            t = transition(progress)

            # apply progression on target
            for key, values in properties.items():
                a, b = values
                value = _calculate(a, b, t)
                setattr(target, key, value)

            # time to stop ?
            if progress >= 1.:
                return
    finally:
        if force_final_value and progress < 1:
            for key, values in properties.items():
                a, b = values
                setattr(target, key, b)
