__all__ = ('animate', )

import trio
from functools import partial
from kivy.clock import Clock
from kivy.animation import AnimationTransition
from asynckivy._animation._simple_ver import _calculate


async def animate(target, **kwargs):
    '''kivy.animation.Animationを真似たもの'''
    duration = kwargs.pop('d', kwargs.pop('duration', 1.))
    transition = kwargs.pop('t', kwargs.pop('transition', 'linear'))
    step = kwargs.pop('s', kwargs.pop('step', 0))
    force_final_value = kwargs.pop('force_final_value', False)
    task_status = kwargs.pop('task_status', trio.TASK_STATUS_IGNORED)
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
        Clock.schedule_once(partial(_set_final_value, target, properties))
        return

    try:
        trio_event = trio.Event()
        ctx = {
            'trio_event': trio_event,
            'target': target,
            'time': 0.,
            'duration': duration,
            'transition': transition,
            'properties': properties,
        }
        clock_event = Clock.schedule_interval(partial(_update, ctx), step)
        await trio_event.wait()
    except trio.Cancelled:
        if force_final_value:
            _set_final_value(target, properties)
        raise
    finally:
        clock_event.cancel()


def _set_final_value(target, properties, *__):
    for key, values in properties.items():
        a, b = values
        setattr(target, key, b)


def _update(ctx, dt):
    time = ctx['time'] + dt
    ctx['time'] = time

    # calculate progression
    progress = min(1., time / ctx['duration'])
    t = ctx['transition'](progress)

    # apply progression on target
    target = ctx['target']
    for key, values in ctx['properties'].items():
        a, b = values
        value = _calculate(a, b, t)
        setattr(target, key, value)

    # time to stop ?
    if progress >= 1.:
        ctx['trio_event'].set()
        return False
