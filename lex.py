import re
from collections import deque
from ast_types import *



'''
	Much of the source code for this Lexer was taken from this excellent example found in the python RE docs
	Many thanks to: Friedl, Jeffrey. Mastering Regular Expressions. 3rd ed., O'Reilly Media, 2009.
	https://docs.python.org/3/library/re.html#functions

'''
class Lexer():
	# https://www.calormen.com/jsbasic/reference.html

	reserved_keywords = {
		'GOTO',
		'END',
		'IF',
		'THEN',
		'PRINT'
		'LET'
	}

	token_specification = [
		('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
		('ASSIGN',   r':='),           # Assignment operator
		('END',      r';'),            # Statement terminator
		('ID',       r'[A-Za-z]+'),    # Identifiers
		('OP',       r'[+\-*/]'),      # Arithmetic operators
		('NEWLINE',  r'\n'),           # Line endings
		('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
		('MISMATCH', r'.'),            # Any other character
	]

	def __init__(self, filename : str) -> None:

		# related to files
		self._filename = filename
		self.file = open(self._filename, 'r')

		# setup regex for matching tokens
		tok_regex_str = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
		self.token_regex = re.compile(tok_regex_str)

		# queue for tokens
		# fill it with more by calling _tokenize
		self._tokens = deque()

		# lexer position within file
		self.line_no = 1


	def _tokenize(self):
		line: str = self.file.readline()

		if line == []:
			self._tokens.append(Token(TokenType.EOF,'',self.line_no, 0))

		for match_obj in self.token_regex.finditer(line):
			kind = match_obj.lastgroup
			value = match_obj.group()
			column = match_obj.start()

			if kind == 'NUMBER':
				value = float(value) if '.' in value else int(value)
			elif kind == 'ID' and value in self.reserved_keywords:
				kind = value
			elif kind == 'NEWLINE':
				line_start = match_obj.end()
				self.line_no += 1
				break
			elif kind == 'SKIP':
				continue
			elif kind == 'MISMATCH':
				raise RuntimeError(f'{value!r} unexpected on line {self.line_no}')
			
			tokenEnum = 
			token = Token(kind, value, self.line_no, column) # type: ignore	(pretty sure this is caught by the MISMATCH case)

			self._tokens.append(token)


	def peek(self, tokenType: TokenType) -> bool:
		return False

	def pop(self, number_tokens_to_pop: int):
		for i in range(number_tokens_to_pop):
			self._tokens.pop()