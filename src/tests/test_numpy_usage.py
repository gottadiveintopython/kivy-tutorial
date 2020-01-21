'''
testというよりはnumpyの勉強

Not actual tests. Just for learning numpy.
'''

import pytest


@pytest.fixture(scope='module')
def sprite_dtype():
    import numpy as np
    return np.dtype([
        ('velocity_y', np.float, ),
        ('x', np.float, ),
        ('y', np.float, ),
        ('visible', np.bool, )
    ])


@pytest.fixture()
def sample_sprites(sprite_dtype):
    import numpy as np
    return np.array([
        (20, 0, 0, True, ),
        (-30, 200, 600, False, ),
        (-50, 500, 500, True, ),
        (10, 30, 10, False, ),
    ], dtype=sprite_dtype)


def test_any_all(sample_sprites):
    import numpy as np
    assert np.any(sample_sprites['visible'] == False)
    assert np.any(sample_sprites['visible'])
    assert not np.all(sample_sprites['visible'] == False)
    assert not np.all(sample_sprites['visible'])


def test_search_element_that_matches_some_condition(sample_sprites):
    import numpy as np
    result = sample_sprites['visible'].nonzero()
    assert np.all(result[0] == [0, 2, ])
    assert result[0][0] == 0
    result = (sample_sprites['visible'] == 0).nonzero()
    assert np.all(result[0] == [1, 3, ])
    assert result[0][1] == 3


def test_update_one_element(sample_sprites):
    s = sample_sprites[0]
    print(dir(s))
    s['visible'] = False
    s['x'] = 3
    assert sample_sprites[0].item() == (20, 3, 0, False, )


def test_update_multiple_elements(sample_sprites):
    import numpy as np
    sample_sprites['visible'][[1, 3]] = True
    assert np.all(sample_sprites['visible'])


def test_update_y(sample_sprites):
    import numpy as np
    sample_sprites['y'] += sample_sprites['velocity_y']
    assert np.all(sample_sprites['y'] == [20, 570, 450, 20, ])


def test_update_y_with_indices(sample_sprites):
    import numpy as np
    indices = sample_sprites['visible'].nonzero()[0]
    sample_sprites['y'][indices] += sample_sprites['velocity_y'][indices]
    assert np.all(sample_sprites['y'] == [20, 600, 450, 10, ])


def test_flatten_structured_array(sample_sprites):
    from numpy.lib.recfunctions import structured_to_unstructured
    extracted = structured_to_unstructured(sample_sprites[['x', 'y']]).ravel()
    assert extracted.tolist() == [0, 0, 200, 600, 500, 500, 30, 10, ]
