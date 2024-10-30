import pytest
import random
from project.game.Bot import Bot, CrazyBot

# Sample strategy functions for testing
def random_strategy():
    return {"type": "number", "choice": random.randint(0, 36)}


def always_even():
    return {"type": "number", "choice": 2 * random.randint(0, 18)}


# Register the strategies with BotMeta
Bot.add_strategy("random", random_strategy)
Bot.add_strategy("even", always_even)


@pytest.fixture
def bot():
    return Bot(name="TestBot", strategy_name="random")


@pytest.fixture
def crazy_bot():
    return CrazyBot(name="CrazyBot", strategy_name="even")


def test_meta_strategies(bot):
    assert "random" in Bot.strategies
    assert "even" in Bot.strategies
    assert len(Bot.strategies) == 2


def test_bot_initialization(bot):
    assert bot.name == "TestBot"
    assert bot.balance == 100
    assert bot.strategy == random_strategy


def test_invalid_strategy():
    with pytest.raises(ValueError):
        Bot(name="InvalidBot", strategy_name="nonexistent")


def test_consider_bet_amount(bot):
    assert bot.consider_bet_amount() == 10


def test_crazy_bot_consider_bet_amount(crazy_bot):
    assert crazy_bot.consider_bet_amount() == crazy_bot.balance


def test_place_bet(bot):
    initial_balance = bot.balance
    amount, bet = bot.place_bet()
    assert amount == 10
    assert bot.balance == initial_balance - amount


def test_place_bet_with_low_balance():
    bot = Bot(name="LowBalanceBot", strategy_name="random", balance=5)
    amount, _ = bot.place_bet()
    assert amount == 5
    assert bot.balance == 0


def test_receive_winnings(bot):
    bot.receive_winnings(50)
    assert bot.balance == 150


def test_receive_winnings_negative_amount(bot):
    with pytest.raises(ValueError):
        bot.receive_winnings(-10)
