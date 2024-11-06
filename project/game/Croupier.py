from project.game.RouletteWheel import RouletteWheel
from project.game.Bot import Bot
from typing import List, Optional


class GameMeta(type):
    """
    Metaclass for managing game-level settings, including the maximum number of rounds.
    """

    def __new__(cls, name: str, bases: tuple, dct: dict) -> type:
        dct.setdefault("max_rounds", 20)
        return super().__new__(cls, name, bases, dct)


class Croupier(metaclass=GameMeta):
    """
    Manages the gameplay for a roulette game, overseeing rounds and player bets.

    Attributes:
        max_rounds (int): The maximum number of rounds to play.
        bots (List[Bot]): The list of participating bots in the game.
        rounds_played (int): The number of rounds played so far.
        roulette_wheel (RouletteWheel): An instance of the roulette wheel.
    """

    max_rounds: int

    def __init__(
        self, bots: List[Bot], wheel: Optional["RouletteWheel"] = None
    ) -> None:
        """
        Initializes the croupier with a list of bots.

        Parameters:
            bots (List[Bot]): A list of bots participating in the game.
            wheel ('RouletteWheel' | None): RouletteWheel that will be used. None if standart wheel.
        """
        self.__bots = bots
        self.__roulette_wheel = RouletteWheel() if wheel is None else wheel
        self.__rounds_played = 0

    def play_round(self) -> None:
        """
        Plays a single round of the game, spinning the roulette wheel and processing bets from each bot.
        """
        print(f"\nRound {self.__rounds_played} begins")
        outcome = self.__roulette_wheel.spin()._asdict()
        print(f"Outcome: {outcome}")

        for bot in self.__bots:
            bet_amount, dict_bet = bot.place_bet()
            print(
                f"{bot.name} placed {bet_amount} on {dict_bet['choice']} ({dict_bet['type']})"
            )

            if outcome[dict_bet["type"]] == dict_bet["choice"]:
                winnings = bet_amount * 2
                bot.receive_winnings(winnings)
                print(f"{bot.name} won {winnings}! Balance: {bot.get_balance()}")
            else:
                print(
                    f"{bot.name} lost their bet of {bet_amount}. Balance: {bot.get_balance()}"
                )

            if bot.get_balance() <= 0:
                print(
                    f"{bot.name} has been kicked from the game due to insufficient balance."
                )
                self.__bots.remove(bot)

    def play_game(self) -> None:
        """
        Plays the game until the maximum number of rounds is reached or all bots have lost their balances.
        """
        self.__rounds_played = 0
        for _ in range(Croupier.max_rounds):
            self.__rounds_played += 1
            self.play_round()
            if len(self.__bots) == 0:
                print("The game is over. All players lost their balances.")
                return

        print("The game is over. A maximum number of rounds has been reached.")

    def get_bots(self) -> List[Bot]:
        """
        Returns the list of Bots that are still in the game

        Returns:
            List[Bot]: the list of Bots
        """
        return self.__bots

    def get_rounds_played(self) -> int:
        return self.__rounds_played
