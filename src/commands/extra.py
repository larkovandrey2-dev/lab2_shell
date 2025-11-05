from errors.shell_errors import ShellError
from ..utils.calculator.calculator import Calculator
from ..utils.calculator.errors import CalculatorError


def cmd_bc(args):
    if args:
        for exp in args:
            calc = Calculator()
            try:
                res = calc.solve(exp)
                print(f"{exp} = {res}")
            except CalculatorError as e:
                raise ShellError("bc: " + str(e).lower())
    else:
        print("Entering interactive mode. Press Ctrl+D or Ctrl+C to exit.")
        while True:
            calc = Calculator()
            try:
                expr = input(">>> ").strip()
                if not expr:
                    continue
                try:
                    result = calc.solve(expr)
                    print(result)
                except CalculatorError as e:
                    print(f"Error: {e}")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting bc.")
                break
