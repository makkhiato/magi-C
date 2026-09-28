import string
from dataclasses import dataclass
from typing import List, Optional


# ========== DELIMITERS & CHARACTER DEFINITIONS ==========

# CHARACTER SETS
LETTERS = set(string.ascii_letters)
NONZERO = set("123456789")
NUMBERS = set("0123456789")
ASCII = set(string.printable)
GLYPH_ASCII = {"'"}
INSC_ASCII = {'"'}

# WHITESPACE & PUNCTUATION
WHITESPACE = {" ", "\t"}
NEWLINE = {"\n", "\r"}
TERMINATOR = {"~"}
COMMA = {","}
DOT = {"."}

# OPERATORS
MATH_OP = {"+", "-", "*", "/", "%"}
NEG_OP = {"-"}
REL_OP = {"<", ">", "="}
EQUAL_OP = {"="}
AND_OR_OP = {"&", "|"}
NOT_OP = {"!"}

# GROUPINGS & QUOTES
OPEN_PAREN = {"("}
CLOSE_PAREN = {")"}
OPEN_CURLY = {"{"}
CLOSE_CURLY = {"}"}
OPEN_BRACKET = {"["}
CLOSE_BRACKET = {"]"}
OPEN_QUOTE = {"'", '"'}

# GENERAL DELIMITERS
SPACE_DEL = WHITESPACE | NEWLINE
PAREN_DEL = WHITESPACE | OPEN_PAREN
CURLY_DEL = WHITESPACE | OPEN_CURLY
TRANSFER_DEL = WHITESPACE | TERMINATOR
CONJURE_DEL = LETTERS | WHITESPACE
LIT_DEL = (
    TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | AND_OR_OP | EQUAL_OP | SPACE_DEL
)

# GROUPING DELIMITERS
OPEN_PAREN_DEL = (
    LETTERS | NUMBERS | NEG_OP | NOT_OP | CLOSE_PAREN | OPEN_QUOTE | PAREN_DEL
)
CLOSE_PAREN_DEL = (
    WHITESPACE
    | NEWLINE
    | TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | AND_OR_OP
    | CLOSE_PAREN
    | OPEN_CURLY
    | CLOSE_CURLY
    | CLOSE_BRACKET
)
OPEN_CURLY_DEL = (
    LETTERS
    | NUMBERS
    | WHITESPACE
    | NEWLINE
    | NEG_OP
    | OPEN_CURLY
    | CLOSE_CURLY
    | OPEN_QUOTE
)
CLOSE_CURLY_DEL = LETTERS | WHITESPACE | NEWLINE | TERMINATOR | COMMA | CLOSE_CURLY
OPEN_BRACKET_DEL = LETTERS | NUMBERS | PAREN_DEL
CLOSE_BRACKET_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | EQUAL_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | OPEN_BRACKET
    | CLOSE_BRACKET
    | SPACE_DEL
)

# OPERATOR DELIMITERS
MINUS_DEL = LETTERS | NUMBERS | PAREN_DEL
MATH_DEL = NEG_OP | MINUS_DEL
CREMENT_DEL = (
    WHITESPACE | TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | CLOSE_BRACKET
)
REL_LOG_DEL = LETTERS | NUMBERS | WHITESPACE | NEG_OP | OPEN_PAREN
NOT_DEL = LETTERS | PAREN_DEL

ASSIGN_DEL = LETTERS | NUMBERS | WHITESPACE | NEG_OP | OPEN_PAREN
BASE_ASSIGN_DEL = OPEN_CURLY | OPEN_QUOTE | ASSIGN_DEL

# PUNCTUATION DELIMITERS
TERMINATOR_DEL = CLOSE_CURLY | SPACE_DEL
COMMA_DEL = (
    LETTERS | NUMBERS | NEG_OP | OPEN_PAREN | OPEN_CURLY | OPEN_QUOTE | SPACE_DEL
)
CLOSE_QUOTE_DEL = (
    WHITESPACE | TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | SPACE_DEL
)
CLOSE_SINGLE_QUOTE_DEL = OPEN_CURLY | CLOSE_QUOTE_DEL

# IDENTIFIER & LITERAL DELIMITERS
ID_DEL = (
    TERMINATOR
    | COMMA
    | DOT
    | MATH_OP
    | REL_OP
    | EQUAL_OP
    | AND_OR_OP
    | NOT_OP
    | OPEN_PAREN
    | CLOSE_PAREN
    | OPEN_CURLY
    | CLOSE_CURLY
    | OPEN_BRACKET
    | CLOSE_BRACKET
    | SPACE_DEL
)
AETHER_LIT_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | AND_OR_OP
    | NOT_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | CLOSE_BRACKET
    | SPACE_DEL
)
ESSENCE_LIT_DEL = (
    TERMINATOR
    | COMMA
    | MATH_OP
    | REL_OP
    | AND_OR_OP
    | NOT_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | SPACE_DEL
)
GLYPH_LIT_DEL = TERMINATOR | COMMA | CLOSE_PAREN | OPEN_CURLY | CLOSE_CURLY | SPACE_DEL
INSCRIPTION_LIT_DEL = TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | SPACE_DEL
AURA_LIT_DEL = (
    TERMINATOR
    | COMMA
    | EQUAL_OP
    | AND_OR_OP
    | NOT_OP
    | CLOSE_PAREN
    | CLOSE_CURLY
    | SPACE_DEL
)

# ========== TOKEN STRUCTURE & CURSOR NAVIGATION ==========

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type:<18}, {repr(self.value):<15}, Line: {self.line:<2}, Col: {self.column:<2})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexical Error [Line {line}, Col {column}: {message}]")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source_code: str):
        self.source: str = source_code
        self.pos: int = 0
        self.line: int = 1
        self.col: int = 1
        self.tokens: List[Token] = []

        self.keywords = {
            # PRIMITIVE DATA TYPES
            "aether": WHITESPACE,
            "aura": WHITESPACE,
            "essence": WHITESPACE,
            "glyph": WHITESPACE,
            "inscription": WHITESPACE,
            # LITERALS
            "blessed": LIT_DEL,
            "cursed": LIT_DEL,
            "null": LIT_DEL,
            # TYPE QUALIFIERS & STRUCTURE
            "circle": WHITESPACE,
            "sealed": WHITESPACE,
            "spell": WHITESPACE,
            # INPUT/OUTPUT STATEMENTS
            "cast": PAREN_DEL,
            "scroll": PAREN_DEL,
            # CONDITIONAL STATEMENTS
            "crossroad": PAREN_DEL,
            "counter": CURLY_DEL,
            "fallback": CURLY_DEL,
            "manifest": PAREN_DEL,
            "remanifest": PAREN_DEL,
            "rune": WHITESPACE,
            # LOOPING STATEMENTS
            "chant": PAREN_DEL,
            "charge": PAREN_DEL,
            "invoke": CURLY_DEL,
            # CONTROL TRANSFER
            "persist": TRANSFER_DEL,
            "shatter": TRANSFER_DEL,
            "yield": TRANSFER_DEL,
            # PROGRAM STRUCTURE & DIRECTIVES
            "conjure": WHITESPACE,
            "darkness": WHITESPACE,
            "grimoire": PAREN_DEL,
            "summon": WHITESPACE,
        }

    def current(self) -> Optional[str]:
        """Returns the character under the cursor without consuming it."""
        return self.source[self.pos] if self.pos < len(self.source) else None

    def peek(self) -> Optional[str]:
        """Returns the 1-character lookahead without consuming it."""
        next_pos = self.pos + 1
        return self.source[next_pos] if next_pos < len(self.source) else None

    def advance(self) -> Optional[str]:
        """Consumes the current character and updates coordinate tracking."""
        ch = self.current()
        if ch is not None:
            self.pos += 1
            if ch == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
        return ch

    def match(self, expected: str) -> bool:
        """Consumes the current character if it matches expected."""
        if self.current() == expected:
            self.advance()
            return True
        return False

    def verify_delimiter(self, token_name: str, allowed_delims: set):
        """Strict 1-character lookahead delimiter verification."""
        lookahead = self.current()
        if lookahead is None:
            return
        if lookahead not in allowed_delims:
            raise LexerError(
                f"Invalid delimiter '{lookahead}' after {token_name}.",
                self.line,
                self.col,
            )

# ========== WHITESPACE AND COMMENTS TRIMMER ==========
    def skip_whitespace_and_comments(self):
        """Silently consumes spaces, tabs, newlines, and block commments (#/ /#)."""
        while self.current() is not None:
            ch = self.current()
            if ch in SPACE_DEL:
                self.advance()
            elif ch == "#" and self.peek() == "/":
                start_line, start_col, = self.line, self.col
                self.advance()
                self.advance()
                closed = False
                while self.current() is not None:
                    if self.current == "/" and self.peek() == "#":
                        self.advance()
                        self.advance()
                        closed = True
                        break
                    self.advance()
                if not closed:
                    raise LexerError("Unclosed comment block '#/'", start_line, start_col)
            else:
                break
            