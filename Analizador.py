from flask import Flask, request, jsonify, render_template
import ply.yacc as yacc
from lexer import tokens
import re

app = Flask(__name__)

KEYWORDS = {'for', 'int', 'return', 'include', 'iostream'}
SYMBOLS = {';', '{', '}', '#', '=', '::', '<', '>','<=', '++', '(', ')', '.'}
IDENTIFIER = r'[a-zA-Z_]\w*'
NUMBER = r'\d+'
STRING = r'".*?"'

TOKEN_REGEX = re.compile(f'({"|".join(map(re.escape, sorted(SYMBOLS, key=len, reverse=True)))})|{IDENTIFIER}|{NUMBER}|{STRING}')

def tokenize(code):
    tokens = []
    for match in TOKEN_REGEX.finditer(code):
        token = match.group(0)
        if token in KEYWORDS:
            tokens.append(('KEYWORD', token))
        elif token in SYMBOLS:
            tokens.append(('SYMBOL', token))
        elif re.match(NUMBER, token):
            tokens.append(('NUMBER', token))
        elif re.match(STRING, token):
            tokens.append(('STRING', token))
        else:
            tokens.append(('IDENTIFIER', token))
    return tokens

def classify_tokens(tokens):
    classification = {
        'PR': 0,
        'ID': 0,
        'Numeros': 0,
        'Simbolos': 0,
        'valor': 0,
        'Error': 0
    }

    for token_type, _ in tokens:
        if token_type == 'KEYWORD':
            classification['PR'] += 1
        elif token_type == 'IDENTIFIER':
            classification['ID'] += 1
        elif token_type == 'NUMBER':
            classification['Numeros'] += 1
        elif token_type == 'SYMBOL':
            classification['Simbolos'] += 1
        elif token_type == 'STRING':
            classification['valor'] += 1
        else:
            classification['Error'] += 1
    
    return classification

def parse_syntactic(data):
    parser = yacc.yacc(module=syntactic_module, debug=False)
    parser.has_error = False
    parser.declared_var = None
    result = parser.parse(data)
    if parser.has_error:
        print(parser.has_error)
        return 'Error sintactico'
    if parser == None:
        return 'Error sintactico'
    return result

def parse_semantic(data):
    parser = yacc.yacc(module=semantic_module, debug=False)
    parser.has_error = False
    parser.declared_var = None
    result = parser.parse(data)
    if parser.has_error:
        return 'Error semántico'
    return result

class syntactic_module:
    tokens = tokens

    def p_exprecion(p):
        '''exprecion : inicio var funtion'''
        p[0] = 'Sintaxis Correcta'

    def p_var(p):
        '''var : INT VARIABLE EQUALS VALOR SEMICOLON'''
        p[0] =  'Sintaxis Correcta'

    def p_inicio(p):
        '''inicio : HASH INCLUDE MENOR IOSTREAM MAYOR'''
        p[0] = 'Sintaxis Correcta'

    def p_funtion(p):
        '''funtion : INT MAIN LPAREN RPAREN statement_block'''
        p[0] = 'Sintaxis Correcta'

    def p_statement_block(p):
        '''statement_block : LBRACE statement return RBRACE'''
        p[0] = 'Sintaxis Correcta'

    def p_return(p):
        'return : RETURN VALOR SEMICOLON'
        p[0] = 'Sintaxis Correcta'

    def p_statement(p):
        '''statement : STD DOTDOT DOTDOT COUT MENOR MENOR VARIABLE SEMICOLON'''
        p[0] = 'Sintaxis Correcta'

    def p_error(p):
        if p:
            print(f"Error de sintaxis en '{p}' '{p.value}'")
            p.lexer.has_error = True
        else:
            print(p)
            print("Error de sintaxis en EOF")
            return None

class semantic_module:
    tokens = tokens

    def p_program(p):
        '''program : inicio variable funtion'''
        p[0] = 'Semantico Correcta'

    def p_variable(p):
        '''variable : INT VARIABLE EQUALS VALOR SEMICOLON'''
        p.parser.declared_variable = p[2]
        p[0] =  'Sintaxis Correcta'

    def p_inicio(p):
        '''inicio : HASH INCLUDE MENOR IOSTREAM MAYOR'''
        p[0] = 'Sintaxis Correcta'

    def p_declaracion(p):
        '''funtion : INT MAIN LPAREN RPAREN statement_block'''
        p[0] = 'Sintaxis Correcta'

    def p_statement_block(p):
        '''statement_block : LBRACE statement return RBRACE'''
        p[0] = 'Sintaxis Correcta'

    def p_proceso(p):
        'return : RETURN VALOR SEMICOLON'
        p[0] = 'Sintaxis Correcta'

    def p_statement(p):
        '''statement : STD DOTDOT DOTDOT COUT MENOR MENOR VARIABLE SEMICOLON'''
        if p[7] != p.parser.declared_variable:
            p.parser.has_error = True
            p[0] = f"Error: Se esperaba la variable declarada {p.parser.declared_var}"
            return p[0]
        p[0] = 'Sintaxis Correcta'

    def p_error(p):
        if p:
            print(f"Error de sintaxis en '{p.value}'")
            p.lexer.has_error = True
        else:
            print("Error de sintaxis en EOF")
            p.parser.has_error = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lexical', methods=['POST'])
def lexical():
    code = request.json['code']
    tokens = tokenize(code)
    classification = classify_tokens(tokens)
    return jsonify({'tokens': tokens, 'classification': classification})

@app.route('/syntactic', methods=['POST'])
def syntactic():
    code = request.json['code']
    result = parse_syntactic(code)
    print(result)
    if result == None:
        return jsonify({'result': 'Error sintactico'})
    return jsonify({'result': result})

@app.route('/semantic', methods=['POST'])
def semantic():
    code = request.json['code']
    result = parse_semantic(code)
    if result==None:
        return jsonify({'result': 'Error semantico'})
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
