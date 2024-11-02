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

    def multy_strategy():
        r = random.randint(0, 6)
        if r == 0:
            return {"type": "color", "choice": random.choice(["Red", "Black", "Green"])}
        if r == 1:
            return {"type": "parity", "choice": random.choice(["Even", "Odd"])}
        if r == 2:
            return {"type": "number", "choice": random.randint(1, 36)}
        if r == 3:
            return {"type": "number", "choice": 0}
        if r == 4:
            return {"type": "row", "choice": random.randint(1, 3)}
        if r == 5:
            return {"type": "half", "choice": random.randint(1, 2)}
        if r == 6:
            return {"type": "third", "choice": random.randint(1, 3)}

    Bot.add_strategy(
        "Schizo bet",
        multy_strategy,
    )

    bots = [
        Bot("Vasya", "Numerical bet"),
        Bot("Kolya", "Parity bet"),
        Bot("Misha", "Color bet"),
        Bot("Oleg", "Schizo bet"),
        CrazyBot("Dmitry", "Color bet"),
    ]
    Croupier.max_rounds = 10
    game = Croupier(bots)
    game.play_game()
