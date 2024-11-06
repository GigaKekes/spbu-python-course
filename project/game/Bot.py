import random
from typing import Callable, Dict, Tuple, TypedDict


class BetDict(TypedDict):
    """
    Typing entity representing the betting dictionary of strucure
    {'type' : int, 'choice' : int | str}
    """

    type: str
    choice: int | str


class BotMeta(type):
    """
    Metaclass for Bots, enabling the addition of betting strategies as class-level methods.
    Each strategy is a callable that defines betting rules.
    """

    strategies: Dict[str, Callable[[], BetDict]] = {}

    def __new__(cls, name: str, bases: tuple, namespace: dict):
        return super().__new__(cls, name, bases, namespace)

    def add_strategy(cls, name: str, strategy_func: Callable[[], BetDict]) -> None:
        """
        Adds a new strategy to the Bot class.

        Parameters:
            name (str): The name of the strategy.
            strategy_func (Callable[[], BetDict]): The strategy function.
        """
        cls.strategies[name] = strategy_func


class Bot(metaclass=BotMeta):
    """
    A bot that participates in the roulette game, making bets according to a specific strategy.

    Attributes:
        name (str): The name of the bot.
        _balance (int): The current balance of the bot.
        strategy (Callable[[], BetDict): The betting strategy function.
    """

    strategies: Dict[str, Callable[[], BetDict]]

    def __init__(self, name: str, strategy_name: str, balance: int = 100):
        """
        Initializes the bot with a name, strategy, and initial balance.

        Parameters:
            name (str): The name of the bot.
            strategy_name (str): The name of the strategy to be used.
            _balance (int): The starting balance for the bot (default is 100).
        """
        self.name = name
        self._balance = balance
        self._strategy = self.get_strategy(strategy_name)

    def get_strategy(self, strategy_name: str) -> Callable[[], BetDict]:
        """
        Retrieves a betting strategy by name.

        Parameters:
            strategy_name (str): The name of the strategy to retrieve.

        Returns:
            Callable[[], Dict[str, str | int]]: The strategy function.

        Raises:
            ValueError: If the strategy name is not found.
        """
        if strategy_name not in Bot.strategies:
            raise ValueError(f"Strategy '{strategy_name}' not found")
        return Bot.strategies[strategy_name]

    def consider_bet_amount(self) -> int:
        """
        Determines the bet amount based on the bot's current balance.

        Returns:
            int: The amount to bet (minimum of 10 or the current balance).
        """
        return min(10, self._balance)

    def place_bet(self) -> Tuple[int, BetDict]:
        """
        Places a bet using the selected strategy, deducting the amount from the bot's balance.

        Returns:
            Tuple[int, Dict[str, str | int]]: The bet amount and the bet details.
        """
        amount = self.consider_bet_amount()
        self._balance -= amount
        return amount, self._strategy()

    def receive_winnings(self, amount: int) -> None:
        """
        Adds winnings to the bot's balance.

        Parameters:
            amount (int): The amount won; must be non-negative.

        Raises:
            ValueError: If the amount is negative.
        """
        if amount < 0:
            raise ValueError("Amount received after winning shouldn't be negative")
        self._balance += amount

    def get_balance(self) -> int:
        return self._balance


class CrazyBot(Bot):
    """
    A bot with a 'crazy' betting strategy, betting its entire balance on each round.
    """

    def consider_bet_amount(self) -> int:
        """
        Determines the bet amount as the bot's entire balance.

        Returns:
            int: The bot's entire balance.
        """
        return self._balance
