import string
from dataclasses import dataclass
from typing import List, Optional

# ========== DELIMITERS & CHARACTER DEFINITIONS ==========

# CHARACTER SETS
LETTERS = set(string.ascii_letters)
NONZERO = set("123456789")
NUMBERS = set("0123456789")
ASCII = set(string.printable)
INSC_ASCII = ASCII - {'"', "\\"}
UNDERSCORE = {"_"}
ID_CHAR = LETTERS | NUMBERS | UNDERSCORE

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
OPEN_QUOTE = {'"'}

# GENERAL DELIMITERS
SPACE_DEL = WHITESPACE | NEWLINE
LIT_DEL = WHITESPACE | TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | AND_OR_OP | EQUAL_OP
PAREN_DEL = WHITESPACE | OPEN_PAREN
CURLY_DEL = WHITESPACE | OPEN_CURLY
TRANSFER_DEL = WHITESPACE | TERMINATOR
CONJURE_DEL = LETTERS | WHITESPACE

# GROUPING DELIMITERS
OPEN_PAREN_DEL = LETTERS | NUMBERS | NEG_OP | NOT_OP | CLOSE_PAREN | OPEN_QUOTE | PAREN_DEL
CLOSE_PAREN_DEL = TERMINATOR | COMMA | MATH_OP | REL_OP | AND_OR_OP | CLOSE_PAREN | OPEN_CURLY | CLOSE_CURLY | CLOSE_BRACKET | SPACE_DEL
OPEN_CURLY_DEL = LETTERS | NUMBERS | NEG_OP | OPEN_CURLY | CLOSE_CURLY | OPEN_QUOTE | SPACE_DEL
CLOSE_CURLY_DEL = LETTERS | TERMINATOR | COMMA | CLOSE_CURLY | SPACE_DEL
OPEN_BRACKET_DEL = LETTERS | NUMBERS | PAREN_DEL
CLOSE_BRACKET_DEL = TERMINATOR | COMMA | MATH_OP | REL_OP | EQUAL_OP | CLOSE_PAREN | CLOSE_CURLY | OPEN_BRACKET | CLOSE_BRACKET | SPACE_DEL

# OPERATOR DELIMITERS
MATH_DEL = LETTERS | NUMBERS | PAREN_DEL
CREMENT_DEL = WHITESPACE | TERMINATOR | COMMA | CLOSE_PAREN | CLOSE_CURLY | CLOSE_BRACKET
REL_LOG_DEL = LETTERS | NUMBERS | WHITESPACE | NEG_OP | OPEN_PAREN
NOT_DEL = LETTERS | PAREN_DEL

ASSIGN_DEL = LETTERS | NUMBERS | WHITESPACE | NEG_OP | OPEN_PAREN
BASE_ASSIGN_DEL = OPEN_CURLY | OPEN_QUOTE | ASSIGN_DEL

# PUNCTUATION DELIMITERS
TERMINATOR_DEL = CLOSE_CURLY | SPACE_DEL
COMMA_DEL = LETTERS | NUMBERS | NEG_OP | OPEN_PAREN | OPEN_CURLY | OPEN_QUOTE | SPACE_DEL
CLOSE_QUOTE_DEL = WHITESPACE | TERMINATOR | COMMA | CLOSE_PAREN | OPEN_CURLY | CLOSE_CURLY

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

    def advance(self) -> str:
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
        return ""

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

# ========== WORDS SCANNER (KEYWORDS, IDENTIFIERS) ==========
    def scan_word(self) -> Token:
        state = 0
        start_col = self.col
        lexeme = ""

        while True:
            ch = self.current()

            # ROOT STATE 0
            if state == 0:
                if ch == "a": lexeme += self.advance(); state = 1
                elif ch == "b": lexeme += self.advance(); state = 12
                elif ch == "c": lexeme += self.advance(); state = 20
                elif ch == "d": lexeme += self.advance(); state = 68
                elif ch == "e": lexeme += self.advance(); state = 77
                elif ch == "f": lexeme += self.advance(); state = 85
                elif ch == "g": lexeme += self.advance(); state = 94
                elif ch == "i": lexeme += self.advance(); state = 103
                elif ch == "m": lexeme += self.advance(); state = 120
                elif ch == "n": lexeme += self.advance(); state = 129
                elif ch == "p": lexeme += self.advance(); state = 134
                elif ch == "r": lexeme += self.advance(); state = 142
                elif ch == "s": lexeme += self.advance(); state = 157
                elif ch == "y": lexeme += self.advance(); state = 188
                elif ch in LETTERS: lexeme += self.advance(); state = 267
                else: raise LexerError(f"Unexpected character {repr(ch)}", self.line, start_col)

            # AETHER (2-7), AURA (8-11)
            elif state == 1:
                if ch == "e": lexeme += self.advance(); state = 2
                elif ch == "u": lexeme += self.advance(); state = 8
                else: state = 267

            # aether (2 -> 6)
            elif state == 2:
                if ch == "t": lexeme += self.advance(); state = 3
                else: state = 269
            elif state == 3:
                if ch == "h": lexeme += self.advance(); state = 4
                else: state = 271
            elif state == 4:
                if ch == "e": lexeme += self.advance(); state = 5
                else: state = 273
            elif state == 5:
                if ch == "r": lexeme += self.advance(); state = 6
                else: state = 275
            elif state == 6:
                if ch in WHITESPACE:
                    state = 7
                    return Token("RW_AETHER", lexeme, self.line, start_col)
                else: state = 277

            # aura (8 -> 10)
            elif state == 8:
                if ch == "r": lexeme += self.advance(); state = 9
                else: state = 269
            elif state == 9:
                if ch == "a": lexeme += self.advance(); state = 10
                else: state = 271
            elif state == 10:
                if ch in WHITESPACE:
                    state = 11
                    return Token("RW_AURA", lexeme, self.line, start_col)
                else: state = 273

            # blessed (12-18)
            elif state == 12:
                if ch == "l": lexeme += self.advance(); state = 13
                else: state = 267
            elif state == 13:
                if ch == "e": lexeme += self.advance(); state = 14
                else: state = 269
            elif state == 14:
                if ch == "s": lexeme += self.advance(); state = 15
                else: state = 271
            elif state == 15:
                if ch == "s": lexeme += self.advance(); state = 16
                else: state = 273
            elif state == 16:
                if ch == "e": lexeme += self.advance(); state = 17
                else: state = 275
            elif state == 17:
                if ch == "d": lexeme += self.advance(); state = 18
                else: state = 277
            elif state == 18:
                if ch in LIT_DEL: 
                    state = 19
                    return Token("RW_BLESSED", lexeme, self.line, start_col)
                else: state = 279
                    
            # CAST (21-24), CHANT (25-29), CHARGE (30-33), CIRCLE (34-39), CONJURE (40-46), COUNTER (47-52), CROSSROAD (53-61), CURSED (62-67)
            elif state == 20:
                if ch == 'a': lexeme += self.advance(); state = 21
                elif ch == 'h': lexeme += self.advance(); state = 25
                elif ch == 'i': lexeme += self.advance(); state = 34
                elif ch == 'o': lexeme += self.advance(); state = 40
                elif ch == 'r': lexeme += self.advance(); state = 53
                elif ch == 'u': lexeme += self.advance(); state = 62
                else: state = 267

            # cast (21-23)
            elif state == 21:
                if ch == "s": lexeme += self.advance(); state = 22
                else: state = 269
            elif state == 22:
                if ch == "t": lexeme += self.advance(); state = 23
                else: state = 271
            elif state == 23:
                if ch in PAREN_DEL:
                    state = 24
                    return Token("RW_CAST", lexeme, self.line, start_col)
                else: state = 273

            # chant (25-28)
            elif state == 25:
                if ch == "a": lexeme += self.advance(); state = 26
                else: state = 269
            elif state == 26:
                if ch == "n": lexeme += self.advance(); state = 27
                elif ch == "r": lexeme += self.advance(); state = 30
                else: state = 271
            elif state == 27:
                if ch == "t": lexeme += self.advance(); state = 28
                else: state = 273
            elif state == 28:
                if ch in PAREN_DEL:
                    state = 29
                    return Token("RW_CHANT", lexeme, self.line, start_col)
                else: state = 275

            # charge (30-32)
            elif state == 30:
                if ch == "g": lexeme += self.advance(); state = 31
                else: state = 273
            elif state == 31:
                if ch == "e": lexeme += self.advance(); state = 32
                else: state = 275
            elif state == 32:
                if ch in PAREN_DEL:
                    state = 33
                    return Token("RW_CHARGE", lexeme, self.line, start_col)
                else: state = 277


            # circle (34-38)
            elif state == 34:
                if ch == "r": lexeme += self.advance(); state = 35
                else: state = 269
            elif state == 35:
                if ch == "c": lexeme += self.advance(); state = 36
                else: state = 271
            elif state == 36:
                if ch == "l": lexeme += self.advance(); state = 37
                else: state = 273
            elif state == 37:
                if ch == "e": lexeme += self.advance(); state = 38
                else: state = 275
            elif state == 38:
                if ch in WHITESPACE:
                    state = 39
                    return Token("RW_CIRCLE", lexeme, self.line, start_col)

            # conjure (40-45)
            elif state == 40:
                if ch == "n": lexeme += self.advance(); state = 41
                elif ch == "u": lexeme += self.advance(); state = 47
                else: state = 269
            elif state == 41:
                if ch == "j": lexeme += self.advance(); state = 42
                else: state = 271
            elif state == 42:
                if ch == "u": lexeme += self.advance(); state = 43
                else: state = 273
            elif state == 43:
                if ch == "r": lexeme += self.advance(); state = 44
                else: state = 275
            elif state == 44:
                if ch == "e": lexeme += self.advance(); state = 45
                else: state = 277
            elif state == 45:
                if ch in WHITESPACE:
                    state = 46
                    return Token("RW_CONJURE", lexeme, self.line, start_col)
                else: state = 279

            # counter (47-51)
            elif state == 47:
                if ch == "n": lexeme += self.advance(); state = 48
                else: state = 271
            elif state == 48:
                if ch == "t": lexeme += self.advance(); state = 49
                else: state = 273
            elif state == 49:
                if ch == "e": lexeme += self.advance(); state = 50
                else: state = 275
            elif state == 50:
                if ch == "r": lexeme += self.advance(); state = 51
                else: state = 277
            elif state == 51:
                if ch in CURLY_DEL:
                    state = 52
                    return Token("RW_COUNTER", lexeme, self.line, start_col)
                else: state = 279

            # crossroad (53-60)
            elif state == 53:
                if ch == "o": lexeme += self.advance(); state = 54
                else: state = 269
            elif state == 54:
                if ch == "s": lexeme += self.advance(); state = 55
                else: state = 271
            elif state == 55:
                if ch == "s": lexeme += self.advance(); state = 56
                else: state = 273
            elif state == 56:
                if ch == "r": lexeme += self.advance(); state = 57
                else: state = 275
            elif state == 57:
                if ch == "o": lexeme += self.advance(); state = 58
                else: state = 277
            elif state == 58:
                if ch == "a": lexeme += self.advance(); state = 59
                else: state = 279
            elif state == 59:
                if ch == "d": lexeme += self.advance(); state = 60
                else: state = 281
            elif state == 60:
                if ch in PAREN_DEL:
                    state = 61
                    return Token("RW_CROSSROAD", lexeme, self.line, start_col)
                else: state = 283

            # cursed (62-66)
            elif state == 62:
                if ch == "r": lexeme += self.advance(); state = 63
                else: state = 269
            elif state == 63:
                if ch == "s": lexeme += self.advance(); state = 64
                else: state = 271
            elif state == 64:
                if ch == "e": lexeme += self.advance(); state = 65
                else: state = 273
            elif state == 65:
                if ch == "d": lexeme += self.advance(); state = 66
                else: state = 275
            elif state == 66:
                if ch in LIT_DEL:
                    state = 67
                    return Token("RW_CURSED", lexeme, self.line, start_col)
                else: state = 277

            # darkness (68-76)
            elif state == 68:
                if ch == "a": lexeme += self.advance(); state = 69
                else: state = 267
            elif state == 69:
                if ch == "r": lexeme += self.advance(); state = 70
                else: state = 269
            elif state == 70:
                if ch == "k": lexeme += self.advance(); state = 71
                else: state = 271
            elif state == 71:
                if ch == "n": lexeme += self.advance(); state = 72
                else: state = 273
            elif state == 72:
                if ch == "e": lexeme += self.advance(); state = 73
                else: state = 275
            elif state == 73:
                if ch == "s": lexeme += self.advance(); state = 74
                else: state = 277
            elif state == 74:
                if ch == "s": lexeme += self.advance(); state = 75
                else: state = 279
            elif state == 75:
                if ch in WHITESPACE:
                    state = 76
                    return Token("RW_DARKNESS", lexeme, self.line, start_col)
                else: state = 281

            # essence (77-76)
            elif state == 77:
                if ch == "s": lexeme += self.advance(); state = 78
                else: state = 267
            elif state == 78:
                if ch == "s": lexeme += self.advance(); state = 79
                else: state = 269
            elif state == 79:
                if ch == "e": lexeme += self.advance(); state = 80
                else: state = 271
            elif state == 80:
                if ch == "n": lexeme += self.advance(); state = 81
                else: state = 273
            elif state == 81:
                if ch == "c": lexeme += self.advance(); state = 82
                else: state = 275
            elif state == 82:
                if ch == "e": lexeme += self.advance(); state = 83
                else: state = 277
            elif state == 83:
                if ch in WHITESPACE:
                    state = 84
                    return Token("RW_ESSENCE", lexeme, self.line, start_col)
                else: state = 279

            # fallback (85-93)
            elif state == 85:
                if ch == "a": lexeme += self.advance(); state = 86
                else: state = 267
            elif state == 86:
                if ch == "l": lexeme += self.advance(); state = 87
                else: state = 269
            elif state == 87:
                if ch == "l": lexeme += self.advance(); state = 88
                else: state = 271
            elif state == 88:
                if ch == "b": lexeme += self.advance(); state = 89
                else: state = 273
            elif state == 89:
                if ch == "a": lexeme += self.advance(); state = 90
                else: state = 275
            elif state == 90:
                if ch == "c": lexeme += self.advance(); state = 91
                else: state = 277
            elif state == 91:
                if ch == "k": lexeme += self.advance(); state = 92
                else: state = 279
            elif state == 92:
                if ch in CURLY_DEL:
                    state = 93
                    return Token("RW_FALLBACK", lexeme, self.line, start_col)
                else: state = 281

            # grimoire (94-102)
            elif state == 94:
                if ch == "r": lexeme += self.advance(); state = 95
                else: state = 267
            elif state == 95:
                if ch == "i": lexeme += self.advance(); state = 96
                else: state = 269
            elif state == 96:
                if ch == "m": lexeme += self.advance(); state = 97
                else: state = 271
            elif state == 97:
                if ch == "o": lexeme += self.advance(); state = 98
                else: state = 273
            elif state == 98:
                if ch == "i": lexeme += self.advance(); state = 99
                else: state = 275
            elif state == 99:
                if ch == "r": lexeme += self.advance(); state = 100
                else: state = 277
            elif state == 100:
                if ch == "e": lexeme += self.advance(); state = 101
                else: state = 279
            elif state == 101:
                if ch in PAREN_DEL:
                    state = 102
                    return Token("RW_GRIMOIRE", lexeme, self.line, start_col)
                else: state = 281

            # INSCRIPTION (103-114), INVOKE (115-119)
            # inscription (103 - 113)
            elif state == 103:
                if ch == "n": lexeme += self.advance(); state = 104
                else: state = 267
            elif state == 104:
                if ch == "s": lexeme += self.advance(); state = 105
                elif ch == "v": lexeme += self.advance(); state = 115
                else: state = 269
            elif state == 105:
                if ch == "c": lexeme += self.advance(); state = 106
                else: state = 271
            elif state == 106:
                if ch == "r": lexeme += self.advance(); state = 107
                else: state = 273
            elif state == 107:
                if ch == "i": lexeme += self.advance(); state = 108
                else: state = 275
            elif state == 108:
                if ch == "p": lexeme += self.advance(); state = 109
                else: state = 277
            elif state == 109:
                if ch == "t": lexeme += self.advance(); state = 110
                else: state = 279
            elif state == 110:
                if ch == "i": lexeme += self.advance(); state = 111
                else: state = 281
            elif state == 111:
                if ch == "o": lexeme += self.advance(); state = 112
                else: state = 283
            elif state == 112:
                if ch == "n": lexeme += self.advance(); state = 113
                else: state = 285
            elif state == 113:
                if ch in WHITESPACE:
                    state = 114
                    return Token("RW_INSCRIPTION", lexeme, self.line, start_col)
                else: state = 287
            
            # invoke (115-118)
            elif state == 115:
                if ch == "o": lexeme += self.advance(); state = 116
                else: state = 271
            elif state == 116:
                if ch == "k": lexeme += self.advance(); state = 117
                else: state = 273
            elif state == 117:
                if ch == "e": lexeme += self.advance(); state = 118
                else: state = 275
            elif state == 118:
                if ch in CURLY_DEL:
                    state = 119
                    return Token("RW_INVOKE", lexeme, self.line, start_col)
                else: state = 277

            # manifest (200-208)
            elif state == 120:
                if ch == "a": lexeme += self.advance(); state = 121
                else: state = 267
            elif state == 121:
                if ch == "n": lexeme += self.advance(); state = 122
                else: state = 269
            elif state == 122:
                if ch == "i": lexeme += self.advance(); state = 123
                else: state = 271
            elif state == 123:
                if ch == "f": lexeme += self.advance(); state = 124
                else: state = 273
            elif state == 124:
                if ch == "e": lexeme += self.advance(); state = 125
                else: state = 275
            elif state == 125:
                if ch == "s": lexeme += self.advance(); state = 126
                else: state = 277
            elif state == 126:
                if ch == "t": lexeme += self.advance(); state = 127
                else: state = 279
            elif state == 127:
                if ch in PAREN_DEL:
                    state = 128
                    return Token("RW_MANIFEST", lexeme, self.line, start_col)
                else: state = 281

            # null (209-213)
            elif state == 129:
                if ch == "u": lexeme += self.advance(); state = 130
                else: state = 267
            elif state == 130:
                if ch == "l": lexeme += self.advance(); state = 131
                else: state = 269
            elif state == 131:
                if ch == "l": lexeme += self.advance(); state = 132
                else: state = 271
            elif state == 132:
                if ch in LIT_DEL:
                    state = 133
                    return Token("RW_NULL", lexeme, self.line, start_col)
                else: state = 273
            
            # persist (214-221)
            elif state == 134:
                if ch == "e": lexeme += self.advance(); state = 135
                else: state = 267
            elif state == 135:
                if ch == "r": lexeme += self.advance(); state = 136
                else: state = 269
            elif state == 136:
                if ch == "s": lexeme += self.advance(); state = 137
                else: state = 271
            elif state == 137:
                if ch == "i": lexeme += self.advance(); state = 138
                else: state = 273
            elif state == 138:
                if ch == "s": lexeme += self.advance(); state = 139
                else: state = 275
            elif state == 139:
                if ch == "t": lexeme += self.advance(); state = 140
                else: state = 277
            elif state == 140:
                if ch in TRANSFER_DEL:
                    state = 141
                    return Token("RW_PERSIST", lexeme, self.line, start_col)
                else: state = 279

            # RUNE (142-146), REMANIFEST (147-156)
            elif state == 142:
                if ch == "u": lexeme += self.advance(); state = 143
                elif ch == "e": lexeme += self.advance(); state = 147 
                else: state = 267
            
            # rune (142-145)
            elif state == 143:
                if ch == "n": lexeme += self.advance(); state = 144
                else: state = 269
            elif  state == 144:
                if ch == "e": lexeme += self.advance(); state = 145
                else: state = 271
            elif state == 145:
                if ch in WHITESPACE:
                    state = 146
                    return Token("RW_RUNE", lexeme, self.line, start_col)
                else: state = 273
            
            # remanifest (147-155)
            elif state == 147:
                if ch == "m": lexeme += self.advance(); state = 148
                else: state = 269
            elif state == 148:
                if ch == "a": lexeme += self.advance(); state = 149
                else: state = 271
            elif state == 149:
                if ch == "n": lexeme += self.advance(); state = 150
                else: state = 273
            elif state == 150:
                if ch == "i": lexeme += self.advance(); state = 151
                else: state = 275
            elif state == 151:
                if ch == "f": lexeme += self.advance(); state = 152
                else: state = 277
            elif state == 152:
                if ch == "e": lexeme += self.advance(); state = 153
                else: state = 279
            elif state == 153:
                if ch == "s": lexeme += self.advance(); state = 154
                else: state = 281
            elif state == 154:
                if ch == "t": lexeme += self.advance(); state = 155
                else: state = 283
            elif state == 155:
                if ch in PAREN_DEL:
                    state = 156
                    return Token("RW_REMANIFEST", lexeme, self.line, start_col)
                else: state = 285
         
            # SCROLL (157-163), SEALED (164-169), SHATTER (170-176), SPELL (177-181), SUMMON (182-187)
            elif state == 157:
                if ch == "c": lexeme += self.advance(); state = 158
                elif ch == "e": lexeme += self.advance(); state = 164
                elif ch == "h": lexeme += self.advance(); state = 170
                elif ch == "p": lexeme += self.advance(); state = 177
                elif ch == "u": lexeme += self.advance(); state = 182
                else: state = 267

            # scroll (158-162)
            elif state == 158:
                if ch == "r": lexeme += self.advance(); state = 159
                else: state = 269
            elif state == 159:
                if ch == "o": lexeme += self.advance(); state = 160
                else: state = 271
            elif state == 160:
                if ch == "l": lexeme += self.advance(); state = 161
                else: state = 273
            elif state == 161:
                if ch == "l": lexeme += self.advance(); state = 162
                else: state = 275
            elif state == 162:
                if ch in PAREN_DEL:
                    state = 163
                    return Token("RW_SCROLL", lexeme, self.line, start_col)
                else: state = 277

            # sealed (164-168)
            elif state == 164:
                if ch == "a": lexeme += self.advance(); state = 165
                else: state = 269
            elif state == 165:
                if ch == "l": lexeme += self.advance(); state = 166
                else: state = 271
            elif state == 166:
                if ch == "e": lexeme += self.advance(); state = 167
                else: state = 273
            elif state == 167:
                if ch == "d": lexeme += self.advance(); state = 168
                else: state = 275
            elif state == 168:
                if ch in WHITESPACE:
                    state = 169
                    return Token("RW_SEALED", lexeme, self.line, start_col)
                else: state = 277

            # shatter (170-175)
            elif state == 170:
                if ch == "a": lexeme += self.advance(); state = 171
                else: state = 269
            elif state == 171:
                if ch == "t": lexeme += self.advance(); state = 172
                else: state = 271
            elif state == 172:
                if ch == "t": lexeme += self.advance(); state = 173
                else: state = 273
            elif state == 173:
                if ch == "e": lexeme += self.advance(); state = 174
                else: state = 275
            elif state == 174:
                if ch == "r": lexeme += self.advance(); state = 175
                else: state = 277
            elif state == 175:
                if ch in TRANSFER_DEL:
                    state = 176
                    return Token("RW_SHATTER", lexeme, self.line, start_col)
                else: state = 279

            # spell (177-180)
            elif state == 177:
                if ch == "e": lexeme += self.advance(); state = 178
                else: state = 269
            elif state == 178:
                if ch == "l": lexeme += self.advance(); state = 179
                else: state = 271
            elif state == 179:
                if ch == "l": lexeme += self.advance(); state = 180
                else: state = 273
            elif state == 180:
                if ch in WHITESPACE:
                    state = 181
                    return Token("RW_SPELL", lexeme, self.line, start_col)
                else: state = 275

            # summon (182-186)
            elif state == 182:
                if ch == "m": lexeme += self.advance(); state = 183
                else: state = 269
            elif state == 183:
                if ch == "m": lexeme += self.advance(); state = 184
                else: state = 271
            elif state == 184:
                if ch == "o": lexeme += self.advance(); state = 185
                else: state = 273
            elif state == 185:
                if ch == "n": lexeme += self.advance(); state = 186
                else: state = 275
            elif state == 186:
                if ch in WHITESPACE:
                    state = 187
                    return Token("RW_SUMMON", lexeme, self.line, start_col)
                else: state = 277

            # yield (188-193)
            elif state == 188:
                if ch == "i": lexeme += self.advance(); state = 189
                else: state = 267
            elif state == 189:
                if ch == "e": lexeme += self.advance(); state = 190
                else: state = 269
            elif state == 190:
                if ch == "l": lexeme += self.advance(); state = 191
                else: state = 271
            elif state == 191:
                if ch == "d": lexeme += self.advance(); state = 192
                else: state = 273
            elif state == 192:
                if ch in TRANSFER_DEL:
                    state = 193
                    return Token("RW_YIELD", lexeme, self.line, start_col)

            # IDENTIFIER STATES: 267-298
            elif 267 <= state <= 297 and state % 2 == 1:
                if ch in ID_DEL or ch is None:
                    state = state + 1  # Transition to even accepting state (268*, 270*, ..., 298*)
                    return Token("IDENTIFIER", lexeme, self.line, start_col)
                elif ch in ID_CHAR:
                    if state == 297:
                        # At state 297 (length 16), there is no transition arrow on id_char
                        raise LexerError(
                            f"Identifier '{lexeme}{ch}' exceeds maximum length of 16 characters",
                            self.line,
                            start_col,
                        )
                    lexeme += self.advance()
                    state = state + 2  # Advance to next odd reading state
                else:
                    raise LexerError(f"Invalid delimiter '{ch}' after identifier '{lexeme}'", self.line, self.col)
