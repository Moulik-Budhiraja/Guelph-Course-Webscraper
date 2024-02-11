from tokenizer import *


class Node:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"{self.value} -> ({', '.join(repr(child) for child in self.children)})"


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

        self.index = 0

    def convert_n_of_to_or(self) -> list[Token]:
        new_tokens = []

        while self.index < len(self.tokens):
            if self._peak().type == TokenType.N_OF:
                choose_n = self._peak().value

                self._next()
                courses = []
                new_courses = []

                while self._peak().type in (TokenType.COURSE, TokenType.COMMA):
                    if self._peak().type == TokenType.COURSE:
                        courses.append(self._peak())

                    self._next()

                if choose_n == 1:
                    for i in range(len(courses)):
                        new_courses.append(courses[i])
                        if i != len(courses) - 1:
                            new_courses.append(Token(TokenType.OR))

                else:
                    combinations = self._get_combinations(courses, choose_n)

                    # OR together all combinations, and AND together all courses in each combination
                    for i, combination in enumerate(combinations):
                        new_courses.append(Token(TokenType.OPEN_PAREN))
                        for j, course in enumerate(combination):
                            new_courses.append(course)
                            if j != len(combination) - 1:
                                new_courses.append(Token(TokenType.COMMA))
                            else:
                                new_courses.append(
                                    Token(TokenType.CLOSE_PAREN))

                        if i != len(combinations) - 1:
                            new_courses.append(Token(TokenType.OR))

                new_tokens += new_courses

            if self._peak().type != TokenType.UNDEFINED:
                new_tokens.append(self._peak())
                self._next()

        return new_tokens

    def gen_tree(self):
        root, _ = self.parse(0)

        return root

    def parse(self, index):
        children = []
        operator = None

        if len(self.tokens) == 0:
            return Node(value='AND', children=[]), 0

        while index < len(self.tokens):
            token = self.tokens[index]

            if token.type == TokenType.OPEN_PAREN:
                # Recurse into a new level of parentheses
                subtree, index = self.parse(index + 1)
                children.append(subtree)

            elif token.type == TokenType.CLOSE_PAREN:
                return Node(value=operator, children=children), index + 1

            elif token.type == TokenType.COURSE:
                children.append(Node(value='COURSE', children=[token.value]))
                index += 1

            elif token.type in [TokenType.OR, TokenType.COMMA]:
                if operator is None:  # The first operator we find determines the node type
                    operator = 'AND' if token.type == TokenType.COMMA else 'OR'
                index += 1

            else:
                raise ValueError(f"Unexpected token: {token}")

        if operator is None:
            if len(children) == 1:
                return Node(value='AND', children=children), index

            raise ValueError(f"Expected an operator (AND/OR) but found none at index {index}.\n---\n\n" +
                             f"{self.tokens}"
                             )

        return Node(value=operator, children=children), index

    def to_dict(self, node: Node) -> dict:
        if node.value in ['AND', 'OR']:
            return {
                'type': node.value,
                'children': [self.to_dict(child) for child in node.children]
            }

        return {
            'type': node.value,
            'value': node.children[0]
        }

    @classmethod
    def _get_combinations(cls, courses: list[Token], n: int) -> list[list[Token]]:
        if n == 1:
            return [[course] for course in courses]

        combinations = []
        for i in range(len(courses)):
            combinations += [[courses[i]] +
                             combination for combination in cls._get_combinations(courses[i + 1:], n - 1)]

        return combinations

    def _peak(self, n=0) -> Token:
        if self.index + n >= len(self.tokens):
            return Token(TokenType.UNDEFINED)

        return self.tokens[self.index + n]

    def _next(self, n=1):
        self.index += n
