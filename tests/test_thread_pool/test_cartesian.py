import pytest
from project.thread_pool.parallel_cartesian_sum import parallel_cartesian_sum


@pytest.mark.parametrize(
    "expected_sum, list_of_sets",
    [(33, [{22}, {11}]), (20, [{1, 2}, {3, 4}]), (84, [{1, 2}, {3, 4}, {5, 6}])],
)
def test_parallel_cartesian_sum(expected_sum, list_of_sets):
    assert expected_sum == parallel_cartesian_sum(list_of_sets)


@pytest.mark.parametrize(
    "list_of_sets",
    [([{}]), ([{}, {3, 4}]), ([{1, 2}, {}, {5, 6}])],
)
def test_assert_parallel_cartesian_sum(list_of_sets):
    with pytest.raises(ValueError):
        parallel_cartesian_sum(list_of_sets)
