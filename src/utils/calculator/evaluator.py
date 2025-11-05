import warnings
from typing import Union

from .constants import WARN_RESULT
from .errors import CalculatorError


class Evaluator:
    """
        Выполняет вычисления выражения, представленного в обратной польской нотации.
    """

    def __init__(self, numbers_after_dot: int = 2):
        """
            Инициализация вычислителя.

            Args:
                numbers_after_dot (int): количество знаков после запятой.
        """
        self.NUMBERS_AFTER_DOT = numbers_after_dot
        self.BIG_WARN = False

    def check_operation(self, op1: float | int, op2: float | int, op_name: str) -> None:
        """
            Проверяет допустимость выполнения целочисленных операций.

            Args:
                op1 (int | float): первый операнд.
                op2 (int | float): второй операнд.
                op_name (str): название операции.

            Raises:
                Exception: если операнды не int или происходит деление на ноль.
        """
        if not all(isinstance(x, int) for x in (op1, op2)):
            raise CalculatorError(f'Invalid action for float digits in {op_name}')
        if op2 == 0:
            raise CalculatorError('Division by zero')

    def apply_result(self, op_result:float) -> float:
        """
            Обрабатывает результат операции и проверяет лимит.

            Args:
                op_result (int | float): результат операции.

            Returns:
                int | float: скорректированный результат.
        """
        if op_result >= WARN_RESULT and not self.BIG_WARN:
            warnings.warn(
                'Слишком большое значение вычисляемого значения. '
                'Программа может работать некорректно.',
                stacklevel=2
            )
        try:
            return int(op_result) if int(op_result) == op_result else op_result
        except ValueError:
            return op_result

    def solve_rpn(self, rpn: list[Union[str, float, int]]) -> float:
        """
            Вычисляет результат выражения в обратной польской нотации.

            Args:
                rpn (list): выражение в виде списка токенов.

            Returns:
                int | float: результат вычисления.

            Raises:
                Exception: если выражение некорректное или не хватает операндов.
        """
        stack: list[float] = []
        self.BIG_WARN = False
        for token in rpn:
            if isinstance(token, (float, int)):
                stack.append(token)
            else:
                if token == '~':
                    op = stack.pop()
                    stack.append(-op)
                elif token == '@':
                    op = stack.pop()
                    stack.append(op)
                else:
                    if len(stack) < 2:
                        raise CalculatorError("Invalid expression")
                    op2 = stack.pop()
                    op1 = stack.pop()

                    if token == '-':
                        stack.append(self.apply_result(op1 - op2))
                    elif token == '+':
                        stack.append(self.apply_result(op1 + op2))
                    elif token == '*':
                        stack.append(self.apply_result(op1 * op2))
                    elif token == '/':
                        stack.append(self.apply_result(op1 / op2))
                    elif token == '^':
                        stack.append(self.apply_result(op1 ** op2))
                    elif token == '$':
                        self.check_operation(op1, op2, '//')
                        stack.append(self.apply_result(op1 // op2))
                    elif token == '%':
                        self.check_operation(op1, op2, '%')
                        stack.append(self.apply_result(op1 % op2))
        if len(stack) != 1:
            raise CalculatorError("Invalid expression")
        if stack[0] == int(stack[0]):
            return int(stack[0])
        return round(stack[0], self.NUMBERS_AFTER_DOT)
