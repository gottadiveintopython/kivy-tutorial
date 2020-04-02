        if sview.height < label.height:
            # touchされた時のscroll量
            scroll_y_subtraction = None
            def _update_scroll_y_subctration(*args):
                nonlocal scroll_y_subtraction
                scroll_y_subtraction = (sview.height - label.font_size) / \
                    (label.height - sview.height)
            _update_scroll_y_subctration()
            sview.bind(height=_update_scroll_y_subctration)
            label.bind(
                height=_update_scroll_y_subctration,
                font_size=_update_scroll_y_subctration,
            )
            while sview.scroll_y > 0:
                await event(
                    bubble, 'on_touch_down',
                    return_value=True,
                    filter=lambda w, t: (not t.is_mouse_scrolling) and \
                        w.collide_point(*t.opos),
                )
                sview.scroll_y = max(0, sview.scroll_y - scroll_y_subtraction)
