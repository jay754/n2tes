import re

# Jack Keywords and Symbols
KEYWORDS = {
    'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 
    'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 
    'let', 'do', 'if', 'else', 'while', 'return'
}

SYMBOLS = {
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', 
    '|', '<', '>', '=', '~'
}

class JackTokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0
        self.tokenize()

    def tokenize(self):
        while self.current_pos < len(self.source_code):
            char = self.source_code[self.current_pos]

            if char in " \t\n\r":
                self.current_pos += 1
                continue

            if char == '/' and self.peek(1) == "/":
                self.skip_single_line_comment()
                continue

            if char == '/' and self.peek(1) == "*":
                self.skip_multi_line_comment()
                continue

            if char.isalpha() or char == "_":
                self.tokens.append(self.consume_identifier())
                continue

            if char.isdigit():
                self.tokens.append(self.consume_integer())
                continue

            if char == "\"":
                self.tokens.append(self.consume_string())
                continue

            if char in SYMBOLS:
                self.tokens.append(self.consume_symbol())
                continue

            # If we encounter an unknown character
            raise ValueError(f"Unexpected character: {char}")

    def skip_single_line_comment(self):
        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos] != '\n':
            self.current_pos += 1

    def skip_multi_line_comment(self):
        self.current_pos += 2
        while self.current_pos < len(self.source_code):
            if self.source_code[self.current_pos] == "*" and self.peek(1) == "/":
                self.current_pos += 2
                break
            self.current_pos += 1

    def consume_identifier(self):
        start_pos = self.current_pos

        while self.current_pos < len(self.source_code) and (self.source_code[self.current_pos].isalnum() or self.source_code[self.current_pos] == "_"):
            self.current_pos += 1

        identifier = self.source_code[start_pos:self.current_pos]

        if identifier in KEYWORDS:
            return f"KEYWORD: {identifier}"

        return f"IDENTIFIER: {identifier}"

    def consume_integer(self):
        start_pos = self.current_pos

        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos].isdigit():
            self.current_pos += 1

        return f"NUMBER: {self.source_code[start_pos:self.current_pos]}"

    def consume_string(self):
        self.current_pos += 1  # Skip the opening quote
        start_pos = self.current_pos

        while self.current_pos < len(self.source_code) and self.source_code[self.current_pos] != "\"":
            self.current_pos += 1

        string = self.source_code[start_pos:self.current_pos]
        self.current_pos += 1  # Skip the closing quote

        return f"STRING: \"{string}\""

    def consume_symbol(self):
        symbol = self.source_code[self.current_pos]
        self.current_pos += 1
        return f"SYMBOL: {symbol}"

    def peek(self, n):
        if self.current_pos + n < len(self.source_code):
            return self.source_code[self.current_pos + n]
        return None

    def get_tokens(self):
        return self.tokens


source_code = """
class Main {
    function void main() {
        var int x;
        let x = 5;
        do Output.printString("Hello, world!");
        return;
    }
}
"""

tokenizer = JackTokenizer(source_code)
tokenizer.tokenize()

# for token in tokenizer.get_tokens():
    # print(token)

print(tokenizer.get_tokens())
