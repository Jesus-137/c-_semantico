from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Define the keywords, symbols, and regex patterns for tokens
KEYWORDS = {'for', 'int', 'system', 'out', 'println'}
SYMBOLS = {';', '{', '}', '=', '<=', '++', '(', ')', '<', '>' '.',}
IDENTIFIER = r'[a-zA-Z_]\w*'
NUMBER = r'\d+'
STRING = r'".*?"'

# Adjust TOKEN_REGEX to handle multi-character symbols first
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

def syntactic_analysis(tokens):
    try:
        idx = 0
        # Parse int main()
        if tokens[idx] != ('KEYWORD', 'int'):
            return f"Error: Se esperaba int tiene: {tokens[idx]}"
        idx += 1
        validar=tokens[idx][0] != 'IDENTIFIER' and re.match(r'^[A-Za-z]+$', tokens[idx][1])
        if validar==None:
            return f"Error: Se esperaba una variable tiene: {tokens[idx]}"
        variable = tokens[idx][1]
        idx += 1
        if tokens[idx] != ('SYMBOL', ';'):
            return f"Error: Se esperaba ; tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('KEYWORD', 'for'):
            return f"Error: Se esperaba for tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', '('):
            return f"Error: Se esperaba ( tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('IDENTIFIER', variable):
            return f"Error: Se esperaba la variable {variable} tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', '='):
            return f"Error: Se esperaba = tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx][0] != 'NUMBER':
            return f"Error: Se esperaba un numero tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', ';'):
            return f"Error: Se esperaba ; tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('IDENTIFIER', variable):
            return f"Error: Se esperaba la variable {variable} tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', '<='):
            return f"Error: Se esperaba <= tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx][0] != 'NUMBER':
            return f"Error: Se esperaba un numero tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', ';'):
            return f"Error: Se esperaba ; tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('IDENTIFIER', variable):
            return f"Error: Se esperaba la variable {variable} tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', '++'):
            return f"Error: Se esperaba ++ tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', ')'):
            return f"Error: Se esperaba ) tiene: {tokens[idx]}"
        idx += 1
        if tokens[idx] != ('SYMBOL', '{'):
            return "Error: Se esperaba { tiene: " + str(tokens[idx])
        idx+=1

        # Parse statements
        while tokens[idx] != ('SYMBOL', '}'):
            # Parse std::cout << "Hola, mundo";
            if tokens[idx] == ('KEYWORD', 'system'):
                idx += 1
                if tokens[idx] != ('KEYWORD', 'out'):
                    return f"Error: Se esperaba out después de system. tiene: {tokens[idx]}"
                idx += 1
                if tokens[idx] != ('KEYWORD', 'println'):
                    return f"Error: Se esperaba println despues de system.out. tiene: {tokens[idx]}"
                idx+=1
                if tokens[idx] != ('SYMBOL', '('):
                    return f"Error: Se esperaba ( tiene: {tokens[idx]}"
                idx += 1
                if tokens[idx] != ('IDENTIFIER', variable):
                    return f"Error: Se esperaba la variable {variable} tiene: {tokens[idx]}"
                idx+=1
                if tokens[idx] != ('SYMBOL', ')'):
                    return f"Error: Se esperaba ) tiene: {tokens[idx]}"
                idx += 1
                if tokens[idx] != ('SYMBOL', ';'):
                    return f"Error: Se esperaba ; al final de la línea tiene: {tokens[idx]}"
                idx += 1
            else:
                return f"Error: Se esperaba system.out.println tiene: {tokens[idx]}"

        return "Sintaxis Correcta"
    except IndexError:
        return "Error: Sintaxis incompleta"

def semantic_analysis(tokens):
    declared_identifiers = set()
    for token_type, value in tokens:
        if token_type == 'KEYWORD' and value == 'int':
            idx = tokens.index((token_type, value)) + 1
            if tokens[idx][0] == 'IDENTIFIER':
                declared_identifiers.add(tokens[idx][1])

    for token_type, value in tokens:
        if token_type == 'IDENTIFIER' and value not in declared_identifiers:
            return f"Error: Identificador no declarado: {value}"
    return "Análisis Semántico Correcto"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lexical', methods=['POST'])
def lexical():
    code = request.json['code']
    tokens = tokenize(code)
    return jsonify({'result': tokens})

@app.route('/syntactic', methods=['POST'])
def syntactic():
    code = request.json['code']
    tokens = tokenize(code)
    result = syntactic_analysis(tokens)
    return jsonify({'result': result})

@app.route('/semantic', methods=['POST'])
def semantic():
    code = request.json['code']
    tokens = tokenize(code)
    result = semantic_analysis(tokens)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
