import argparse
from pathlib import Path
import sys
import ply.lex as lex


reserved = {
    'function': 'FUNCTION',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'return': 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE'
}

tokens = (
    'ID', 'INTEGER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'INCREMENT', 'DECREMENT', 'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA',
) + tuple(reserved.values())

t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'
t_EQ = r'=='
t_NE = r'!='
t_LE = r'<='
t_GE = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ASSIGN = r'='
t_LT = r'<'
t_GT = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_ignore = ' \t\r\f\v'


def t_ID(token):
    r'[A-Za-z_][A-Za-z_0-9]*'
    if token.value in reserved:
        token.type = reserved[token.value]
    return token


def t_INTEGER(token):
    r'[0-9]+'
    return token


def t_newline(token):
    r'\n+'
    token.lexer.lineno += len(token.value)


def column(source, position):
    return position - source.rfind('\n', 0, position)


def t_error(token):
    message = (
        f'{token.lineno}:{column(token.lexer.lexdata, token.lexpos)}: '
        f'illegal character {token.value[0]!r}'
    )
    token.lexer.errors.append(message)
    token.lexer.skip(1)


def build_lexer():
    lexer = lex.lex(module=sys.modules[__name__])
    lexer.errors = []
    return lexer


def main(argv=None):
    parser = argparse.ArgumentParser(description='Lexical analyzer for PLT')
    parser.add_argument('source', type=Path, help='PLT source file (UTF-8)')
    args = parser.parse_args(argv)

    try:
        source = args.source.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as error:
        print(f'{args.source}: {error}', file=sys.stderr)
        return 2

    lexer = build_lexer()
    lexer.input(source)
    print(f"{'LINE:COL':<12} {'TOKEN':<12} LEXEME")

    for token in lexer:
        location = f'{token.lineno}:{column(source, token.lexpos)}'
        print(f'{location:<12} {token.type:<12} {token.value}')

    for error in lexer.errors:
        print(f'{args.source}:{error}', file=sys.stderr)

    if lexer.errors:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
