from type import Type
from token import Token
from node import Node
from ast import AST
import re

class LexicalError(Exception):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def lex_source_file(fd):
    with open(fd, 'r') as file:
        data = file.read()
    return lex_source_string(data)


def lex_source_string(string):
    tokens = list()
    index = 0
    while index < len(string):
        token = separate_token(string, index)
        if token is None:
            break
        index = token.end
        tokens.append(token)
    if index != len(string):
        raise LexicalError('Lexical error at position ' + str(index))
    return tokens


def separate_token(string, begin):
    if begin < 0 or begin >= len(string):
        raise IndexError(string, 'Index out of bounds: ' + begin)
    for type in Type:
        pattern = r'.{' + str(begin) + '}' + type.value
        match = re.match(pattern, string, re.DOTALL)
        if match:
            end = match.end(1)
            if type == Type.STRING_LITERAL or type == Type.CHARACTER_LITERAL:
                end += 1
            return Token(begin, end, string[begin:end], type)
    return None

##########################################################################################################
'''PARSER'''

def parser(tokens):
    current = 23
    

    def walk():
        nonlocal current
        token = tokens[current]
        types = [Type.MINUS,Type.NULL,Type.STRING_LITERAL, Type.TRUE, Type.FALSE, Type.INT_CONSTANT, Type.POINT, Type.CLOSE_PAREN, Type.ASSIGNMENT, Type.PLUS, 
                Type.OPEN_PAREN, Type.IDENTIFIER, Type.ASSIGNMENT, Type.SPACE, Type.SEMICOLON,Type.RETURN,  
                Type.OPEN_CURLY_BRACE, Type.TAB, Type.BREAK, Type.CLOSE_CURLY_BRACE, Type.NEW_LINE, Type.MULTIPLY, Type.DIVIDE]
        
        assigning = [Type.INT, Type.FLOAT,Type.STRING, Type.BOOLEAN, Type.DOUBLE, Type.CHAR]

        if token.type in types:
            current+=1
            return token


        if token.type in assigning:#int c = 1;

            node = Node(token.type, token.value)

            current += 2
            token = tokens[current]

           
            while True:
                node.params.append(walk())
                token = tokens[current]
                if(token.type == Type.SEMICOLON):
                    node.params.append(walk())
                    token = tokens[current]
                    break
            current += 1

            return node
        if token.type == Type.IF:#if(c == 1){return c;}

            node = Node(token.type, token.value)

            current += 1
            token = tokens[current]


            if token.type == Type.OPEN_PAREN:

                expression = []


                while True:
                    if token.type == Type.CLOSE_PAREN:
                        expression.append(token)
                        current += 1
                        token = tokens[current]
                        node.params.append(expression)
                        break

                    expression.append(token)
                    current += 1
                    token = tokens[current]

            while True:

                node.params.append(walk())
                token = tokens[current]

                if(token.type == Type.CLOSE_CURLY_BRACE):
                    node.params.append(walk())
                    token = tokens[current]
                    break

            return node

        if token.type == Type.ELSE:#if(c == 1){return c;}

            node = Node(token.type, token.value)

            current += 1
            token = tokens[current]

            while True:

                node.params.append(walk())
                token = tokens[current]

                if(token.type == Type.CLOSE_CURLY_BRACE):
                    node.params.append(walk())
                    token = tokens[current]
                    break

            return node



        

        if token.type == Type.WHILE:

            node = Node(token.type, token.value)

            current += 1
            token = tokens[current]

            if token.type == Type.OPEN_PAREN:

                expression = []


                while True:
                    if token.type == Type.CLOSE_PAREN:
                        expression.append(token)
                        current += 1
                        token = tokens[current]
                        node.params.append(expression)
                        break

                    expression.append(token)
                    current += 1
                    token = tokens[current]

            while True:
                node.params.append(walk())
                token = tokens[current]

                if(token.type == Type.CLOSE_CURLY_BRACE):
                    node.params.append(walk())
                    token = tokens[current]
                    break

            return node

    #Create AST
    ast = AST('body')

    while current < len(tokens):
        ast.params.append(walk())

    return ast


def create_new_ast(ast):
    new_ast = AST('body')#[]

    tokens_java = [Type.OPEN_CURLY_BRACE, Type.SEMICOLON, Type.CLOSE_CURLY_BRACE, Type.TAB]
    tokens_java_val = ['System', '.', 'out']

    for i in range(len(ast.params)):

        if type(ast.params[i]) != Node:

            if ast.params[i].type not in tokens_java:
                if ast.params[i].value == 'println':
                    
                    node.params.append((Token)(ast.params[i].begin,ast.params[i].end,'\nprint', Type.IDENTIFIER))

                elif ast.params[i].value not in tokens_java_val:
                    if ast.params[i].type not in tokens_java:
                        node.params.append(ast.params[i])

        else:
            node = Node(ast.params[i].type, ast.params[i].name)

            if type(ast.params[i].params[0]) is list:
                index = []

                for j in range(len(ast.params[i].params[0])):
                    index.append(ast.params[i].params[0][j])
                    
                node.params.append(index)

                for j in range(1, len(ast.params[i].params)):

                    if ast.params[i].params[j].value == 'println':
                        #node.params.append(ast[i].params[j])
                        node.params.append((Token)(ast.params[i].params[j].begin,ast.params[i].params[j].end,'print', Type.IDENTIFIER)) 
                    elif ast.params[i].params[j].value not in tokens_java_val:
                        if ast.params[i].params[j].type not in tokens_java:
                            node.params.append(ast.params[i].params[j])
            else:

                for j in range(len(ast.params[i].params)):
                    if ast.params[i].params[j].type not in tokens_java:
                        node.params.append(ast.params[i].params[j])
            new_ast.params.append(node)
    return new_ast



def code_generator(new_ast):

    python_code = ""
    assigning = ['int', 'float', 'double', 'boolean', 'char', 'String']
    for i in range(len(new_ast.params)):

        if type(new_ast.params[i]) is Token:
            python_code += "\n"

        else:

            if new_ast.params[i].name in assigning:

                for j in range(len(new_ast.params[i].params)):
                    python_code += new_ast.params[i].params[j].value

            else:
                python_code += new_ast.params[i].name

                start = 0
                if type(new_ast.params[i].params[0]) is list:
                    for j in range(len(new_ast.params[i].params[0])):
                        python_code += new_ast.params[i].params[0][j].value
                    start = 1
                python_code += ':'

                for j in range(start, len(new_ast.params[i].params)):

                    python_code += new_ast.params[i].params[j].value

                    if new_ast.params[i].params[j].type == Type.NEW_LINE:

                        python_code += '    '

            python_code += "\n"
    return python_code

file = lex_source_file('main.java')

    

def main():
    file = lex_source_file('main.java')
    #for i in range(len(file)):
    #    print(file[i])
    
    ast = parser(file)

    #    for i in range(len(ast.params)):
    #        print(ast.params[i])


    new_ast = create_new_ast(ast)
    #print("\n---------------\n")

    #for i in range(len(new_ast.params)):
    #    print(new_ast.params[i])
    #print("\n\n")


    code = code_generator(new_ast)

    print("\n<---CODE--->\n")
    print(code)

    with open("Output.py", "w") as text_file:
        text_file.write(code)


if __name__== "__main__":
    main()
