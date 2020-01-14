__all__ = ('event', )

from trio import Event, TASK_STATUS_IGNORED


async def event(ed, name, *, filter=None, return_value=None, wants_kwargs=False,
                task_status=TASK_STATUS_IGNORED):
    '''注意点
    on_touch_xxx系のeventには向いていないかもしれない。理由はuserが素早くclickした場合に
    on_touch_upを取りそこねるから。例えば以下のcodeのにおいて

        await event(widget, 'on_touch_down')
        print('buttonが押し下げられました')
    
    print式の前にon_touch_upが起きてしまう。
    '''
    def _callback(*args, **kwargs):
        nonlocal parameter
        if (filter is not None) and not filter(*args, **kwargs):
            return
        parameter = (args, kwargs, )
        ed.unbind_uid(name, bind_id)
        event_.set()
        return return_value

    parameter = None
    bind_id = ed.fbind(name, _callback)
    assert bind_id > 0  # check if binding succeeded
    event_ = Event()
    task_status.started()
    await event_.wait()
    return parameter if wants_kwargs else parameter[0]
