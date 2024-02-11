# Tokenizer
from enum import Enum
import re


class TokenType(Enum):
    N_OF = 1
    COURSE = 2
    COMMA = 3
    OR = 4
    OPEN_PAREN = 5
    CLOSE_PAREN = 6
    UNKNOWN = 7
    UNDEFINED = 8


class Token:
    def __init__(self, type: TokenType, value: int | str | None = None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.type == TokenType.UNKNOWN:
            return str(self.value)

        return f"{self.type.name}({self.value if self.value else ''})"

    def __hash__(self):
        return hash(self.type)

    def __eq__(self, other: 'Token'):
        return self.type == other.type


class Tokenizer:
    def __init__(self, text: str):
        self.text = text
        self.index = 0

        self.tokens = self.tokenize()

    def tokenize(self) -> list[Token]:
        tokens: Token = []

        tokens = self.initial_tokenization(tokens)
        tokens = self.clean_ors(tokens)

        return tokens

    def initial_tokenization(self, tokens: list[Token]) -> list[Token]:
        while self.index < len(self.text):
            buffer = self._peak()

            if buffer == " ":
                self._next()
                continue

            # Parentheses
            if buffer == "[":
                tokens.append(Token(TokenType.OPEN_PAREN))
                self._next()
                continue
            if buffer == "]":
                tokens.append(Token(TokenType.CLOSE_PAREN))
                self._next()
                continue
            if buffer == "(":
                tokens.append(Token(TokenType.OPEN_PAREN))
                self._next()
                continue
            if buffer == ")":
                tokens.append(Token(TokenType.CLOSE_PAREN))
                self._next()
                continue

            # Comma
            if buffer == ",":
                tokens.append(Token(TokenType.COMMA))
                self._next()
                continue

            # n of
            if buffer.isdigit():
                buffer += self._peak(1, 3)
                if re.match(r"[0-9] of", buffer):
                    tokens.append(Token(TokenType.N_OF, int(buffer[0])))
                    self._next(len(buffer))
                    continue

                buffer = buffer[0]

            # Course
            if buffer.isalpha():
                while not self._peak(len(buffer)) in (",", " ", "", ")", "]", "."):
                    buffer += self._peak(len(buffer))

                if re.match(r"^[A-Z]{2,4}\*[0-9]{4}$", buffer):
                    tokens.append(Token(TokenType.COURSE, buffer))
                    self._next(len(buffer))
                    continue

                buffer = buffer[0]

            # Or
            if buffer == "o":
                buffer += self._peak(len(buffer))
                if re.match(r"or", buffer):
                    tokens.append(Token(TokenType.OR))
                    self._next(len(buffer))
                    continue

                buffer = buffer[0]

            # Default
            # tokens.append(Token(TokenType.UNKNOWN, buffer))
            self._next(len(buffer))

        return tokens

    def clean_ors(self, tokens: list[Token]) -> list[Token]:
        # Remove ors that are not between courses or parentheses
        new_tokens = []

        for i, token in enumerate(tokens):
            if token.type == TokenType.OR:
                if tokens[i - 1].type not in (TokenType.COURSE, TokenType.CLOSE_PAREN) or (i + 1 < len(tokens) and tokens[i + 1].type not in (TokenType.COURSE, TokenType.OPEN_PAREN)):
                    continue

            new_tokens.append(token)

        return new_tokens

    def _peak(self, n=0, length=1):
        return self.text[self.index + n: self.index + n + length]

    def _next(self, n=1):
        self.index += n
