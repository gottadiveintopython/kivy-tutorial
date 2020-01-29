import pytest
# from kivy.tests import async_run


async def test_props_watching(nursery):
    from kivy_tutorial.magnet import KTMagnet
    magnet = KTMagnet(nursery=nursery)
    assert set(magnet._props_watching.keys()) == \
        {'pos', 'size', }
    magnet.anim_props = ['opacity']
    assert set(magnet._props_watching.keys()) == \
        {'opacity', }


async def test_add_more_than_one_children(nursery):
    from kivy.uix.widget import Widget
    from kivy_tutorial.magnet import KTMagnet
    magnet = KTMagnet(nursery=nursery)
    magnet.add_widget(Widget())
    with pytest.raises(ValueError):
        magnet.add_widget(Widget())


# def basic_app():
#     from kivy.app import App
#     from kivy.tests import UnitKivyApp
#     from kivy.uix.relativelayout import RelativeLayout
#     class TestApp(UnitKivyApp, App):
#         def build(self):
#             return RelativeLayout()
#     return TestApp()


# @async_run(app_cls_func=basic_app)
# async def test_do_nothing_after_add_a_child(kivy_app, nursery):
#     from math import isclose
#     import trio
#     from kivy.uix.widget import Widget
#     from kivy_tutorial.magnet import KTMagnet
#     magnet = KTMagnet(
#         nursery=nursery,
#         x=100, y=200,
#     )
#     w = Widget(x=0, y=0)
#     magnet.add_widget(w)
#     await kivy_app.async_sleep(.5)
#     assert isclose(w.x, 50, abs_tol=10)
#     assert isclose(w.y, 100, abs_tol=10)
#     await kivy_app.async_sleep(.7)
#     assert w.x == 100
#     assert w.y == 200


# @async_run(app_cls_func=basic_app)
# async def test_change_pos_after_add_a_child(kivy_app, nursery):
#     from math import isclose
#     import trio
#     from kivy.uix.widget import Widget
#     from kivy_tutorial.magnet import KTMagnet
#     magnet = KTMagnet(
#         nursery=nursery,
#         x=100, y=200,
#     )
#     w = Widget(x=0, y=0)
#     magnet.add_widget(w)
#     # await kivy_app.async_sleep(.05)
#     magnet.x = -100
#     magnet.y = -200
#     await kivy_app.async_sleep(.5)
#     assert isclose(w.x, -50, abs_tol=10)
#     assert isclose(w.y, -100, abs_tol=10)
#     await kivy_app.async_sleep(.7)
#     assert w.x == -100
#     assert w.y == -200


# @async_run(app_cls_func=basic_app)
# async def test_change_anim_props_after_add_a_child(kivy_app, nursery):
#     from math import isclose
#     import trio
#     from kivy.uix.widget import Widget
#     from kivy_tutorial.magnet import KTMagnet
#     magnet = KTMagnet(
#         nursery=nursery,
#         x=100, y=200,
#     )
#     w = Widget(x=0, y=0)
#     magnet.add_widget(w)
#     magnet.anim_props = ['opacity']
#     await kivy_app.async_sleep(.5)
#     assert w.x == 0
#     assert w.y == 0
#     assert w.opacity == 1
#     magnet.opacity = 0
#     await kivy_app.async_sleep(.5)
#     assert w.x == 0
#     assert w.y == 0
#     assert isclose(w.opacity, .5, abs_tol=10)
#     await kivy_app.async_sleep(.7)
#     assert w.x == 0
#     assert w.y == 0
#     assert w.opacity == 0
