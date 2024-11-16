import pytest
from project.treap.treap import Treap


@pytest.fixture
def sample_treap():
    threap = Treap()
    threap[5] = "a"
    threap[3] = "b"
    threap[8] = "c"
    threap[1] = "d"
    threap[4] = "e"
    return threap


@pytest.fixture
def longer_treap():
    threap = Treap()
    threap[10] = "x"
    threap[5] = "y"
    threap[15] = "z"
    threap[12] = "a"
    threap[18] = "b"
    threap[3] = "c"
    return threap


@pytest.fixture
def empty_treap():
    return Treap()


@pytest.mark.parametrize(
    "key, val",
    [
        (5, "a"),
        (3, "b"),
        (8, "c"),
        (1, "d"),
        (4, "e"),
    ],
)
def test_getitem(key, val, sample_treap):
    assert sample_treap[key] == val


def test_insert(sample_treap):
    sample_treap[7] = "f"
    sample_treap[6] = "g"
    sample_treap[5] = "z"
    assert sample_treap[5] == "z"
    assert list(sample_treap) == [1, 3, 4, 5, 6, 7, 8]


@pytest.mark.parametrize("key", [1, 3, 4, 5, 8])
def test_contains(key, sample_treap):
    assert key in sample_treap


def test_delitem(sample_treap):
    del sample_treap[3]
    assert 3 not in sample_treap
    assert len(sample_treap) == 4


@pytest.mark.parametrize(
    "keys_to_delete, expected_structure_after_deletion",
    [
        ([1], [3, 4, 5, 8]),
        ([1, 3], [4, 5, 8]),
        ([1, 3, 5], [4, 8]),
    ],
)
def test_deletion_structure(
    keys_to_delete, expected_structure_after_deletion, sample_treap
):
    for key in keys_to_delete:
        del sample_treap[key]

    assert list(sample_treap) == expected_structure_after_deletion


def test_delete_nonexistent_key(sample_treap):
    with pytest.raises(KeyError):
        del sample_treap[10]


def test_mixed_insertion_deletion_structure(longer_treap):

    assert list(longer_treap) == [3, 5, 10, 12, 15, 18]

    del longer_treap[15]
    assert list(longer_treap) == [3, 5, 10, 12, 18]

    del longer_treap[10]
    assert list(longer_treap) == [3, 5, 12, 18]

    longer_treap[6] = "d"
    assert list(longer_treap) == [3, 5, 6, 12, 18]

    del longer_treap[6]
    assert list(longer_treap) == [3, 5, 12, 18]


def test_len(sample_treap):
    assert len(sample_treap) == 5
    del sample_treap[5]
    assert len(sample_treap) == 4


def test_iteration(sample_treap):
    assert list(sample_treap) == [1, 3, 4, 5, 8]


def test_reversed_iteration(sample_treap):
    assert list(reversed(sample_treap)) == [8, 5, 4, 3, 1]
