import pytest


def test_when_there_is_no_active_nursery():
    from kivy_tutorial.triouser import TrioUser
    with pytest.raises(IndexError):
        TrioUser()


async def test_when_there_is_no_active_nursery2(nursery):
    from kivy_tutorial.triouser import TrioUser
    user = TrioUser(nursery=nursery)
    assert user.nursery is nursery


async def test_activate_nursery(nursery):
    import trio
    from kivy_tutorial.triouser import activate_nursery, TrioUser
    with activate_nursery(nursery):
        user = TrioUser()
        assert user.nursery is nursery
        async with trio.open_nursery() as child_nursery:
            with activate_nursery(child_nursery):
                user2 = TrioUser()
                assert user2.nursery is child_nursery
        user3 = TrioUser()
        assert user3.nursery is nursery


async def test_argument_processing(nursery):
    from kivy_tutorial.triouser import TrioUser
    class ArgHolder:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
    class SomeTrioUser(TrioUser, ArgHolder):
        pass
    user = SomeTrioUser(
        1, 2, 3,
        nursery=nursery,
        title='Bumblebee', year=2018,
    )
    assert user.args == (1, 2, 3, )
    assert user.kwargs == {'title': 'Bumblebee', 'year': 2018, }
