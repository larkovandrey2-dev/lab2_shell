import re
import warnings

from .errors import CalculatorError


class RPNConverter:
    """
        Переводит инфиксное выражение в обратную польскую нотацию (RPN).
    """

    def __init__(self, priority: dict[str, int]) -> None:
        """
            Инициализация конвертера.

            Args:
                priority (dict): словарь с приоритетами операторов.
        """
        self.priority = priority
        self.OPERATION_WARN = False

    def is_number(self, token: str) -> bool:
        """
            Проверяет, является ли токен числом.

            Args:
                token (str): токен выражения.

            Returns:
                bool: True, если токен — число, иначе False.
        """
        return token.isdigit() or re.match(r"\d+\.\d+|\.\d+", token) is not None

    def should_pop(self, token: str, top_stack: str) -> bool:
        """
            Проверяет, нужно ли выталкивать оператор из стека.

            Args:
                token (str): текущий оператор.
                top_stack (str): оператор на вершине стека.

            Returns:
                bool: True, если нужно выталкивать, иначе False.
        """
        if token == '^':
            return self.priority[top_stack] > self.priority[token]
        return self.priority[top_stack] >= self.priority[token]

    def to_rpn(self, tokens: list[str]) -> list[str | int | float]:
        """
            Преобразует список токенов в выражение в обратной польской нотации.

            Args:
                tokens (list[str]): список токенов.

            Returns:
                list: выражение в виде списка токенов RPN.

            Raises:
                Exception: при некорректных скобках или последовательности операторов.
        """
        stack: list[str | int | float] = []
        output: list[str | int | float] = []
        prev_token = None
        self.OPERATION_WARN = False

        for i, token in enumerate(tokens):
            if token == '(' and i > 0 and self.is_number(tokens[i - 1]):
                raise CalculatorError("Invalid syntax: number before '('")
            if token == ')' and i > 0 and tokens[i - 1] == '(':
                raise CalculatorError("Invalid syntax: empty parentheses")
            if (prev_token is not None and prev_token in self.priority
                    and token in self.priority):
                if (prev_token not in '()' and token not in '()'
                        and not self.OPERATION_WARN):
                    warnings.warn(
                        'Два или более знаков подряд. Выражение продолжит обработку, '
                        'но проверьте корректность введенных данных',
                        stacklevel=2
                    )
                    self.OPERATION_WARN = True
                    if token not in '+-':
                        raise CalculatorError('Invalid sequence of operators')
            prev_token = token

            if self.is_number(token):
                if '.' in token:
                    output.append(float(token))
                else:
                    output.append(int(token))

            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if not stack:
                    raise CalculatorError("Invalid parentheses")
                stack.pop()
            elif token in self.priority:
                if (token == '-') and (i == 0 or tokens[i - 1] in self.priority):
                    token = '~'
                if (token == '+') and (i == 0 or tokens[i - 1] in self.priority):
                    token = '@'
                while stack and self.should_pop(token, str(stack[-1])):
                    output.append(stack.pop())
                stack.append(token)

        while stack:
            if stack[-1] == '(':
                raise CalculatorError("Invalid parentheses")
            output.append(stack.pop())

        return output
