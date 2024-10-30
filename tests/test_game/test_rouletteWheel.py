import pytest
from project.game.RouletteWheel import RouletteWheel


@pytest.fixture
def roulette():
    return RouletteWheel()


def test_initialization(roulette):
    for number, data in roulette.number_data.items():
        if number == 0:
            assert data["color"] == "Green"
            assert data["parity"] is None
            assert data["third"] is None
            assert data["row"] is None
            assert data["half"] is None
        else:
            assert data["color"] in ["Red", "Black"]
            assert data["parity"] in ["Even", "Odd"]
            assert data["third"] in [1, 2, 3]
            assert data["row"] in [1, 2, 3]
            assert data["half"] in [1, 2]


def test_spin_returns_valid_structure(roulette):
    result = roulette.spin()
    assert "number" in result
    assert "color" in result
    assert "parity" in result
    assert "third" in result
    assert "row" in result
    assert "half" in result

    assert 0 <= result["number"] <= 36
    assert result["color"] in ["Green", "Red", "Black"]
    assert result["parity"] in [None, "Even", "Odd"]
    assert result["third"] in [None, 1, 2, 3]
    assert result["row"] in [None, 1, 2, 3]
    assert result["half"] in [None, 1, 2]


def test_spin_consistency_with_data(roulette):
    for _ in range(10):
        result = roulette.spin()
        number = result["number"]
        expected_data = roulette.number_data[number]
        assert result["color"] == expected_data["color"]
        assert result["parity"] == expected_data["parity"]
        assert result["third"] == expected_data["third"]
        assert result["row"] == expected_data["row"]
        assert result["half"] == expected_data["half"]


def test_correct_color_representation(roulette):
    for i in range(37):
        color = roulette.number_data[i]["color"]
        if i == 0:
            assert color == "Green"
        elif ((1 <= i <= 10 or 19 <= i <= 28) and i % 2 == 0) or (
            (11 <= i <= 18 or 29 <= i <= 36) and i % 2 != 0
        ):
            assert color == "Black"
        else:
            assert color == "Red"


def test_correct_parity_representation(roulette):
    for i in range(37):
        parity = roulette.number_data[i]["parity"]
        if i == 0:
            assert parity is None
        elif i % 2 == 0:
            assert parity == "Even"
        else:
            assert parity == "Odd"


def test_correct_third_representation(roulette):
    for i in range(37):
        third = roulette.number_data[i]["third"]
        if i == 0:
            assert third is None
        elif i <= 12:
            assert third == 1
        elif i <= 24:
            assert third == 2
        else:
            assert third == 3


def test_correct_row_representation(roulette):
    for i in range(37):
        row = roulette.number_data[i]["row"]
        if i == 0:
            assert row is None
        elif i % 3 == 0:
            assert row == 1
        elif i % 3 == 1:
            assert row == 3
        else:
            assert row == 2


def test_correct_half_representation(roulette):
    for i in range(37):
        half = roulette.number_data[i]["half"]
        if i == 0:
            assert half is None
        elif i <= 18:
            assert half == 1
        else:
            assert half == 2
