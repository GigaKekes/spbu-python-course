import random
from ..Bot import Bot, CrazyBot
from ..Croupier import Croupier

if __name__ == "__main__":

    Bot.add_strategy(
        "Numerical bet", lambda: {"type": "number", "choice": random.randint(0, 36)}
    )
    Bot.add_strategy(
        "Parity bet",
        lambda: {"type": "parity", "choice": random.choice(["Even", "Odd"])},
    )
    Bot.add_strategy(
        "Color bet",
        lambda: {"type": "color", "choice": random.choice(["Red", "Black", "Green"])},
    )

    bots = [
        Bot("Vasya", "Numerical bet"),
        Bot("Kolya", "Parity bet"),
        Bot("Misha", "Color bet"),
        CrazyBot("Dmitry", "Color bet"),
    ]
    Croupier.max_rounds = 10
    game = Croupier(bots)
    game.play_game()
