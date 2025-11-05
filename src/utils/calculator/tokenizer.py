import re

from .errors import CalculatorError


class Tokenizer:
    """
        Отвечает за разбиение исходного выражения на токены.
    """

    def tokenize(self, expression: str) -> list[str]:
        """
            Разбивает выражение на токены.

            Args:
                expression (str): исходное выражение.

            Returns:
                list[str]: список токенов (числа, операторы, скобки).

            Raises:
                Exception: если встречены недопустимые символы или некорректная запись.
        """
        expression = expression.replace('**', '^').replace('//', '$')
        tokens = re.findall(r'\d+\.\d+|\.\d+|\d+|[-+/%*()^$]',
                            expression.replace(' ', ''))
        rebuild_exp = ''.join(i for i in tokens)

        if rebuild_exp != expression.replace(' ', ''):
            raise CalculatorError('Invalid symbols in expression')

        if re.search(r'\d+\s+\d+|\d+\s+\.\s+\d+', expression):
            raise CalculatorError(
                'Two numbers/number and dot with space between')

        return tokens
