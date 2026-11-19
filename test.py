"""Paste a Magi-C program into SAMPLE_PROGRAM to inspect its tokens and parse trace."""

from lexer.Lexer import Lexer
from parser.Parser import LL1Parser


# Replace this text with the program you want to analyze.
SAMPLE_PROGRAM = """
aether test = 1 + 2 * (3 - 4) / 5;
"""


def main() -> None:
    lexer = Lexer(SAMPLE_PROGRAM)
    tokens = lexer.tokenize()

    print("=== TOKENS ===")
    if tokens:
        for index, token in enumerate(tokens, start=1):
            print(f"{index:>3}. {token}")
    else:
        print("(no tokens)")

    if lexer.errors:
        print("\n=== LEXER ERRORS ===")
        for error in lexer.errors:
            print(error)

    result = LL1Parser().parse(tokens)

    print("\n=== PARSER TRACE ===")
    if result.steps:
        for step in result.steps:
            print(step.action)
    else:
        print("(no parse steps)")

    if result.valid:
        print("\nParse result: valid")
    else:
        location = ""
        if result.line is not None:
            location = f" at line {result.line}"
            if result.column is not None:
                location += f", column {result.column}"
        print(f"\nParse result: invalid{location}")
        if result.error:
            print(f"Error: {result.error}")


if __name__ == "__main__":
    main()
