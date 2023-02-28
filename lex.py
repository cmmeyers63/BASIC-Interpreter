import re
from collections import deque
from b_types import *


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
		'LET',
		'REM',
		'TO',
		'NEXT',
		'EOL',
		'EOF',
		'DIM',
		'PRINT'
	}

	token_specification = [
		('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
		('ASSIGN',   r'='),            # Assignment operator
		('IDENT',    r'[A-Za-z]+'),    # Identifiers
		('BOP',      r'[*/]'),         # Bianary operators
		('AOP',		 r'[+-]'),		   # Arithmetic operators
		('COMPARE',  r'>=|<=|>|<|<>'), # comparison operators
		('L_PAREN',  r'\('),
		('R_PAREN',  r'\)'),
		('COMMA',    r','),
		('QUOTE',	 r'"'),
		('NEWLINE',  r'\n'),           # Line endings
		('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
		('MISMATCH', r'.'),            # Any other character
	]

	def __init__(self, filename : str) -> None:

		# related to files
		self._filename = filename
		self.file = open(self._filename, 'r')

		# setup regex for matching tokens
		# each token is a named group
		tok_regex_str = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
		self.token_re = re.compile(tok_regex_str)

		# queue for tokens
		self._tokens: deque[Node] = deque()

		# lexer position within file
		self.line_no = 1

	@staticmethod
	def pretty_print_token(token : Node):
		print(f"\t{token.type:<15} value: {(token.value if token.type is not TokenType.NEWLINE else 'newline'):<10} ln:{token.line:<5} col:{token.col:<6}")

	# Takes in a string representing a line of text and returns an array of tokens 
	def Tokenize(self):
		with open(self._filename, 'r') as f:
			file_lines: list[str] = f.readlines()


		line_comment_re = re.compile(r'^\d+ REM')

		for line in file_lines:
			print("line:",line)
			# skip over comments
			mo = line_comment_re.match(line)
			if mo is not None:
				self.line_no += 1
				print("\tCOMMENT SKIPPED")
				continue

			self._tokenize_line(line)
			
		# manually append a EOF
		node = Node(TokenType('EOF'),'',self.line_no + 1,0)
		Lexer.pretty_print_token(node)
		self._tokens.append(node)


	def _tokenize_line(self, line : str):
		for match_obj in self.token_re.finditer(line):
			kind = match_obj.lastgroup
			value = match_obj.group()
			column = match_obj.start()

			if kind == 'NUMBER':
				# value = float(value) if '.' in value else int(value)
				pass
			elif kind == 'IDENT' and value in self.reserved_keywords:
				# create a keyword ex: PRINT 
				# otherwise if value isn't a reserved keyword a variable identifer will be created
				kind = value
			elif kind == 'NEWLINE':
				line_start = match_obj.end()
				self.line_no += 1
			elif kind == 'SKIP':
				continue
			elif kind == 'MISMATCH':
				raise RuntimeError(f'\n{value!r} unexpected on line {self.line_no}\nline: {line}')
			elif kind == None:
				# I don't think this will ever be raised due to the Mismatch rule
				raise RuntimeError(f'fail to match on {self.line_no}')

			token_type = TokenType(kind)
			node = Node(token_type, value, self.line_no, column)
			Lexer.pretty_print_token(node)

			self._tokens.append(node)


	def peek_n(self, token_types: list[TokenType]) -> bool:
		if len(token_types) > len(self._tokens):
			return False
		
		for i, expected_type in enumerate(token_types):
			if self._tokens[i].type is not expected_type:
				return False

		return True

	def peek(self, token_type: TokenType) -> bool:
		return len(token_type) > 0 and self._tokens[0].type is token_type
			
	def pop(self):
		if len(self._tokens) == 0:
			raise RuntimeError(f"Cannot remove token. None remaining")

		return(self._tokens.popleft())