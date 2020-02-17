import pytest


@pytest.fixture(scope='module', autouse=True)
def add_resource_search_path(assets_dir):
    from kivy.resources import resource_add_path, resource_remove_path
    resource_add_path(str(assets_dir))
    yield
    resource_remove_path(str(assets_dir))


# async def test_bgm_resumability(nursery):
#     '''私の環境ではこのtestに失敗するとPCを再起動するまでPC上における全ての音が完全に
#     鳴らなくなりやっかいなので、comment outしておく。'''
#     import trio
#     from kivy.core.audio import SoundLoader
#     from kivy_tutorial.bgmplayer import Bgm
    
#     bgm = Bgm(SoundLoader.load("sound/n74.ogg"))
#     prev_pos = bgm.pos
#     await bgm.play()
#     curr_pos = bgm.pos
#     assert prev_pos < curr_pos
#     await bgm.stop()
#     prev_pos, curr_pos = curr_pos, bgm.pos
#     assert prev_pos < curr_pos
#     await bgm.play()
#     prev_pos, curr_pos = curr_pos, bgm.pos
#     assert prev_pos < curr_pos
#     await bgm.stop()
#     prev_pos, curr_pos = curr_pos, bgm.pos
#     assert prev_pos < curr_pos

    
async def test_play_then_stop_then_play_the_same_one(nursery):
    import trio
    from kivy_tutorial.bgmplayer import BgmPlayer
    
    player = BgmPlayer(
        nursery=nursery,
        polling_interval=.1,
        file_prefix='sound/'
    )
    bgms = player._bgms

    player.play('n75.ogg')
    assert player._next_file == 'n75.ogg'
    assert 'n75.ogg' not in bgms
    assert player._current_bgm is None

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    player.stop()
    assert player._next_file == ''
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is None

    player.play('n75.ogg')
    assert player._next_file == 'n75.ogg'
    assert 'n75.ogg' in bgms
    assert player._current_bgm is None

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    player.stop()
    await trio.sleep(1.5)


async def test_play_then_play_the_same_one(nursery):
    import trio
    from kivy_tutorial.bgmplayer import BgmPlayer
    
    player = BgmPlayer(
        nursery=nursery,
        polling_interval=.1,
        file_prefix='sound/'
    )
    bgms = player._bgms

    player.play('n75.ogg')
    assert player._next_file == 'n75.ogg'
    assert 'n75.ogg' not in bgms
    assert player._current_bgm is None

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    player.play('n75.ogg')
    assert player._next_file == 'n75.ogg'
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    player.stop()
    await trio.sleep(1.5)


async def test_play_then_stop_then_play_another_one(nursery):
    import trio
    from kivy_tutorial.bgmplayer import BgmPlayer
    
    player = BgmPlayer(
        nursery=nursery,
        polling_interval=.1,
        file_prefix='sound/'
    )
    bgms = player._bgms

    player.play('n75.ogg')
    assert player._next_file == 'n75.ogg'
    assert 'n75.ogg' not in bgms
    assert player._current_bgm is None

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    player.stop()
    assert player._next_file == ''
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is None

    player.play('n74.ogg')
    assert player._next_file == 'n74.ogg'
    assert 'n75.ogg' in bgms
    assert player._current_bgm is None

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n74.ogg' in bgms
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n74.ogg']

    player.stop()
    await trio.sleep(1.5)


async def test_play_then_play_another_one(nursery):
    import trio
    from kivy_tutorial.bgmplayer import BgmPlayer
    
    player = BgmPlayer(
        nursery=nursery,
        polling_interval=.1,
        file_prefix='sound/'
    )
    bgms = player._bgms

    player.play('n75.ogg')
    assert player._next_file == 'n75.ogg'
    assert 'n75.ogg' not in bgms
    assert player._current_bgm is None

    await trio.sleep(1.5)
    assert player._next_file is None
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    player.play('n74.ogg')
    assert player._next_file == 'n74.ogg'
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n75.ogg']

    await trio.sleep(2.5)
    assert player._next_file is None
    assert 'n74.ogg' in bgms
    assert 'n75.ogg' in bgms
    assert player._current_bgm is bgms['n74.ogg']

    player.stop()
    await trio.sleep(1.5)
