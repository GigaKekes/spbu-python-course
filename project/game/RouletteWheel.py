import random


class RouletteWheel:
    """
    Represents a roulette wheel with numbers and their associated properties.

    Attributes:
        number_data (Dict[int, Dict[str, Any]]): A dictionary containing properties for each number on the wheel.
    """

    def __init__(self):
        """
        Initializes the RouletteWheel, setting up the number data for each roulette number.
        Each number has associated properties: color, parity, third, row, and half.
        """
        self.number_data = {
            i: {
                "color": "Green"
                if i == 0
                else (
                    "Black"
                    if ((1 <= i <= 10 or 19 <= i <= 28) and i % 2 == 0)
                    or ((11 <= i <= 18 or 29 <= i <= 36) and i % 2 != 0)
                    else "Red"
                ),
                "parity": None if i == 0 else ("Even" if i % 2 == 0 else "Odd"),
                "third": None if i == 0 else (1 if i <= 12 else (2 if i <= 24 else 3)),
                "row": None
                if i == 0
                else (1 if i % 3 == 0 else (3 if i % 3 == 1 else 2)),
                "half": None if i == 0 else (1 if i <= 18 else 2),
            }
            for i in range(37)
        }

    def spin(self):
        """
        Spins the roulette wheel, randomly selecting a number from 0 to 36.

        Returns:
            Dict[str, Any]: A dictionary containing the properties of the selected number,
            including the number itself and its associated attributes.
        """
        number = random.choice(list(range(37)))
        result = self.number_data[number]
        result["number"] = number
        return result
