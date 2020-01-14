import pytest

@pytest.fixture()
def modify_sys_path(tmp_path):
    import sys
    try:
        sys.path.append(str(tmp_path))
        yield
    finally:
        sys.path.remove(str(tmp_path))


async def test_sceneswitcher(nursery, tmp_path, modify_sys_path):
    from importlib import import_module
    from textwrap import dedent
    from pathlib import Path
    import trio
    from kivy_tutorial.sceneswitcher import SceneSwitcher
    PKGNAME = 'pkg_for_testing_sceneswitcher'
    path_to_mypkg:Path = tmp_path / PKGNAME
    path_to_mypkg.mkdir()
    path_to_mymodule1:Path = path_to_mypkg / 'mymodule1.py'
    path_to_mymodule2:Path = path_to_mypkg / 'mymodule2.py'
    path_to_mymodule1.write_text(
        dedent('''
        value = 'before1'
        async def main(switcher, nursery, *, arg):
            global value
            value = arg + '1'
        '''),
        encoding='utf-8',
    )
    path_to_mymodule2.write_text(
        dedent('''
        value = 'before2'
        async def main(switcher, nursery, *, arg):
            global value
            value = arg + '2'
        '''),
        encoding='utf-8',
    )
    switcher = SceneSwitcher(
        nursery=nursery,
        pkgname=PKGNAME,
        userdata={'arg': 'after', },
    )
    assert switcher.local_nursery is None
    mymodule1 = import_module(f"{PKGNAME}.mymodule1")
    mymodule2 = import_module(f"{PKGNAME}.mymodule2")
    assert mymodule1.value == 'before1'
    assert mymodule2.value == 'before2'
    switcher.switch('mymodule1')
    assert switcher.modules == {
        'mymodule1': mymodule1,
    }
    await trio.sleep(.1)
    assert switcher.local_nursery is not None
    assert mymodule1.value == 'after1'
    assert mymodule2.value == 'before2'
    switcher.switch('mymodule2')
    assert switcher.modules == {
        'mymodule1': mymodule1,
        'mymodule2': mymodule2,
    }
    await trio.sleep(.1)
    assert mymodule1.value == 'after1'
    assert mymodule2.value == 'after2'
