import sys
import warnings
from typing import TextIO, Union

from .converter_rpn import RPNConverter
from .evaluator import Evaluator
from .tokenizer import Tokenizer


def custom_warn(
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    file: TextIO | None = None,
    line: str | None = None,
) -> None:
    """
    Кастомный вывод предупреждений в stdout вместо stderr.
    """
    sys.stdout.write(f"\033[33m{message}\033[0m\n")


warnings.showwarning = custom_warn


class Calculator:
    """
    Калькулятор на основе обратной польской нотации (RPN).
    """

    def __init__(self, numbers_after_dot: int = 2):
        """
        Инициализация калькулятора.
        """
        self.priority = {
            '(': 0, '+': 1, '-': 1, '*': 2, '/': 2,
            '$': 2, '%': 2, '^': 3, '~': 4, '@': 4
        }
        self.tokenizer = Tokenizer()
        self.converter = RPNConverter(self.priority)
        self.evaluator = Evaluator(numbers_after_dot)

    def solve(self, expression: str) -> float | int:
        """
        Основной метод решения выражения.
        """
        tokens = self.tokenizer.tokenize(expression)
        rpn: list[Union[str, float, int]] = self.converter.to_rpn(tokens)
        return self.evaluator.solve_rpn(rpn)
