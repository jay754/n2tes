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
        self.token_pos = 0    # For token position during parsing
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

    def current_token(self):
        if self.token_pos < len(self.tokens):

            # print("token position", self.token_pos)
            
            # print("token", self.tokens[self.token_pos])

            return self.tokens[self.token_pos]
        return None

    def advance(self):
        if self.token_pos + 1 < len(self.tokens):
            self.token_pos += 1
        else:
            raise ValueError("No more tokens.")


class JackParser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output = []

    def compile_class(self):
        print("class", self.tokenizer.current_token()) # Print the class keyword

        self.tokenizer.advance() # 'class' keyword
        
        print("class name", self.tokenizer.current_token()) # Print class name

        self.tokenizer.advance() # class name

        print("{")

        self.tokenizer.advance() # '{'

        self.compile_class_var_dec() # Handle class variable declarations

        print("}")  # Print the closing brace
        
        self.tokenizer.advance()  # '}'


    def compile_class_var_dec(self):
        while self.tokenizer.current_token() in ["static", "field"]:
            print("class_var_dec")

            self.tokenizer.advance() # 'static' or 'field'

            print("var type", self.tokenizer.current_token())

            self.tokenizer.advance() # type

            print("var name", self.tokenizer.current_token())

            self.tokenizer.advance()  # variable name

            while self.tokenizer.current_token() == ",":
                self.tokenizer.advance()

                print("var name", self.tokenizer.current_token())  # Print additional variable names

            print(";")

            self.tokenizer.advance()

    def compile_subroutine_dec(self):
        while self.tokenizer.current_token() in ['constructor', 'function', 'method']:
            print("subroutine_dec")

            self.tokenizer.advance()

            print("return type", self.tokenizer.current_token())

            self.tokenizer.advance()

            print("subroutine name", self.tokenizer.current_token())

            self.tokenizer.advance()

            print("(")

            self.tokenizer.advance()

            self.compile_parameter_list()

    def compile_parameter_list(self):
        print("parameter_list")

        if self.tokenizer.current_token() != ')':
            print("param type", self.tokenizer.current_token())

            self.tokenizer.advance()

            print("param name", self.tokenizer.current_token())

            self.tokenizer.advance()

            while self.tokenizer.current_token() == ",":
                self.tokenizer.advance()

                print("param type", self.tokenizer.current_token())

                self.tokenizer.advance()

                print("param name", self.tokenizer.current_token())

                self.tokenizer.advance()


    def compile_var_dec(self):
        while self.tokenizer.current_token == "var":
            print("var_dec")

            self.tokenizer.advance()

            print("var type", self.tokenizer.current_token())

            self.tokenizer.advance()

            print("var name", self.tokenizer.current_token())

            self.tokenizer.advance()

            while self.tokenizer.current_token() == ',':
                self.tokenizer.advance()

                print("var name", self.tokenizer.current_token())

                self.tokenizer.advance()

            print(';')

            self.tokenizer.advance()

    def compile_statements(self):
        while self.tokenizer.current_token() in ['let', 'if', 'while', 'do', 'return']:
            if self.tokenizer.current_token() == 'let':
                self.compile_let_statement()
            elif self.tokenizer.current_token() == 'if':
                self.compile_if_statement()
            elif self.tokenizer.current_token() == 'while':
                self.compile_while_statement()
            elif self.tokenizer.current_token() == 'do':
                self.compile_do_statement()
            elif self.tokenizer.current_token() == 'return':
                self.compile_return_statement()


    def compile_let_statement(self):
        print("let_statement")

        self.tokenizer.advance()

        print("var name", self.tokenizer.current_token())

        self.tokenizer.advance()

        print("=")  # Print assignment operator

        self.tokenizer.advance()

        print("value or expression", self.tokenizer.current_token())

        self.tokenizer.advance()

        print(";")  # Print semicolon
        
        self.tokenizer.advance()

    def compile_if_statement(self):
        print("if_statement")

        self.tokenizer.advance()

        print("condition", self.tokenizer.current_token())

        self.tokenizer.advance()

        print("if block", self.tokenizer.current_token())

        self.tokenizer.advance()

        self.compile_statements()

        if self.tokenizer.current_token() == 'else':
            print("else")

            self.tokenizer.advance()

            self.compile_statements()

    def compile_while_statement(self):
        print("while_statement")

        self.tokenizer.advance()  # while

        print("condition", self.tokenizer.current_token())

        self.tokenizer.advance()

        print("while block", self.tokenizer.current_token())

        self.tokenizer.advance()

        self.compile_statements()

    def compile_do_statement(self):
        print("do_statement")

        self.tokenizer.advance()

        print("procedure call", self.tokenizer.current_token())

        self.tokenizer.advance()

        print(";")  # Print semicolon

        self.tokenizer.advance()

    def compile_return_statement(self):
        print("returs_statement")

        self.tokenizer.advance()

        print("return value", self.tokenizer.current_token())

        self.tokenizer.advance()

        print(";") 
        
        self.tokenizer.advance()


source_code = """
class Main {
    function void main() {
        var int x;
        let x = 5;
        do Output.printString("Hello, world!");
        return;
    }

"""

# for token in tokenizer.get_tokens():
    # print(token)

tokenizer = JackTokenizer(source_code)
tokens = tokenizer.get_tokens()

print(tokens)
# print(tokens[0])

parser = JackParser(tokenizer)

# Access and print each token one by one
while tokenizer.current_token():
    print(tokenizer.current_token())
    tokenizer.advance()