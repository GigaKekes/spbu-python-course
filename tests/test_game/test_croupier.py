import pytest
from project.game.Croupier import Croupier
from project.game.RouletteWheel import RouletteWheel
from project.game.Bot import Bot


class TestRouletteWheel(RouletteWheel):
    def __init__(self, outcome):
        self._outcome = outcome

    def spin(self):
        return self._outcome


class TestBot(Bot):
    def __init__(self, name, balance=100):
        self.name = name
        self.balance = balance

    def place_bet(self):
        bet_amount = 10 if self.balance >= 10 else self.balance
        self.balance -= bet_amount
        return bet_amount, {"choice": 1, "type": "number"}


@pytest.fixture
def winning_outcome():
    return {
        "color": "Red",
        "parity": "Odd",
        "third": 1,
        "row": 2,
        "half": 1,
        "number": 1,
    }


@pytest.fixture
def losing_outcome():
    return {
        "color": "Black",
        "parity": "Even",
        "third": 1,
        "row": 3,
        "half": 1,
        "number": 2,
    }


@pytest.fixture
def croupier_with_winning_bot(winning_outcome):
    bot = TestBot(name="WinningBot")
    roulette = TestRouletteWheel(outcome=winning_outcome)
    return Croupier(bots=[bot]), bot, roulette


@pytest.fixture
def croupier_with_losing_bot(losing_outcome):
    bot = TestBot(name="LosingBot")
    roulette = TestRouletteWheel(outcome=losing_outcome)
    return Croupier(bots=[bot]), bot, roulette


def test_play_round_winning_bet(croupier_with_winning_bot):
    croupier, bot, roulette = croupier_with_winning_bot
    croupier.roulette_wheel = roulette
    initial_balance = bot.balance

    croupier.play_round()
    expected_winnings = 350
    assert bot.balance == initial_balance - 10 + expected_winnings


def test_play_round_losing_bet(croupier_with_losing_bot):
    croupier, bot, roulette = croupier_with_losing_bot
    croupier.roulette_wheel = roulette
    initial_balance = bot.balance

    croupier.play_round()
    assert bot.balance == initial_balance - 10


def test_bot_removed_when_balance_zero(losing_outcome):
    bot = TestBot(name="ZeroBalanceBot", balance=10)
    roulette = TestRouletteWheel(outcome=losing_outcome)
    croupier = Croupier(bots=[bot])
    croupier.roulette_wheel = roulette

    croupier.play_round()
    assert bot not in croupier.bots


def test_game_ends_when_all_bots_are_out(losing_outcome):
    bot = TestBot(name="LastBot", balance=10)
    roulette = TestRouletteWheel(outcome=losing_outcome)
    croupier = Croupier(bots=[bot])
    croupier.roulette_wheel = roulette

    croupier.play_game()
    assert croupier.rounds_played == 1


def test_game_max_rounds(losing_outcome):
    bot = TestBot(name="EnduranceBot", balance=5000)
    roulette = TestRouletteWheel(outcome=losing_outcome)
    croupier = Croupier(bots=[bot])
    croupier.roulette_wheel = roulette

    croupier.play_game()
    assert croupier.rounds_played == Croupier.max_rounds
