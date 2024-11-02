import random
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class RouletteNumber:
    """
    Represents a single number on a roulette wheel and its associated properties.

    Attributes:
        number (int): The number on the roulette wheel (0-36).
        color (str): The color of the number, either "Green", "Red", or "Black".
        parity (Optional[str]): Whether the number is "Even" or "Odd"; None if 0.
        third (Optional[int]): Indicates which third of the wheel the number belongs to (1, 2, or 3); None if 0.
        row (Optional[int]): The row in which the number is located (1, 2, or 3); None if 0.
        half (Optional[int]): Which half of the numbers the number belongs to (1 for 1-18, 2 for 19-36); None if 0.
    """

    number: int
    color: str
    parity: str | None
    third: int | None
    row: int | None
    half: int | None


class RouletteWheel:
    """
    Represents a roulette wheel with numbers from 0 to 36, each with specific properties.

    Attributes:
        number_data (Dict[int, RouletteNumber]): A dictionary mapping each roulette number
            to its associated properties as a RouletteNumber instance.
    """

    def __init__(self):
        """
        Initializes the RouletteWheel with detailed properties for each number (0-36).
        Sets up color, parity, third, row, and half attributes for each number.
        """
        self.number_data: Dict[int, RouletteNumber] = {
            i: RouletteNumber(
                number=i,
                color="Green"
                if i == 0
                else (
                    "Black"
                    if ((1 <= i <= 10 or 19 <= i <= 28) and i % 2 == 0)
                    or ((11 <= i <= 18 or 29 <= i <= 36) and i % 2 != 0)
                    else "Red"
                ),
                parity=None if i == 0 else ("Even" if i % 2 == 0 else "Odd"),
                third=None if i == 0 else (1 if i <= 12 else (2 if i <= 24 else 3)),
                row=None if i == 0 else (1 if i % 3 == 0 else (3 if i % 3 == 1 else 2)),
                half=None if i == 0 else (1 if i <= 18 else 2),
            )
            for i in range(37)
        }

    def spin(self) -> Dict[str, str | int | None]:
        """
        Simulates spinning the roulette wheel by selecting a random number (0-36) and returning its properties.

        Returns:
            Dict[str, Any]: A dictionary containing the selected number and its associated properties:
                - "number": The selected number (int).
                - "color": The color of the number ("Green", "Red", or "Black") (str).
                - "parity": Whether the number is "Even" or "Odd" (str or None).
                - "third": The third of the wheel the number belongs to (int or None).
                - "row": The row in which the number is located (int or None).
                - "half": Which half of the wheel the number belongs to (int or None).
        """
        number = random.choice(list(range(37)))
        result = self.number_data[number]
        return {
            "number": result.number,
            "color": result.color,
            "parity": result.parity,
            "third": result.third,
            "row": result.row,
            "half": result.half,
        }
