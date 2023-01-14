from enum import Enum 

class TokenType(Enum):
	# terminals
	L_PAREN = 0
	R_PAREN = 1
	EQUALS = 2
	PLUS = 3
	MINUS = 4
	TIMES = 5
	DIVIDE = 6
	VALUE = 7
	IDENTIFIER = 8
	END_OF_STMT = 9
	POW = 12

	NEWLINE = 15
	EOF = 16

	# non-terminals
	START = 10
	A_EXPR = 11
	I_EXPR = 13
	B_EXPR = 14


def _init_from_str(token_type : str):
		types = {
			'(' : TokenType.L_PAREN,
			')' : TokenType.R_PAREN,
			'=' : TokenType.EQUALS,
			'+' : TokenType.PLUS,
			'-' : TokenType.MINUS,
			'*' : TokenType.TIMES,
			'/' : TokenType.DIVIDE,
			
		}


class Token():
	# terminal symbol constructor
	def __init__(self, type : TokenType, value: str, line: int, col: int) -> None:
		self.type = type
		self.value = value
		self.line = line
		self.col = col
		
		self.children = []
		self.parent = None
		self.id = 0

	def __repr__(self):
		type_without_prefix = str(self.type).split('.')[-1]
		return f"{type_without_prefix} {self.value if self.value is not None else '-'}"

	def add_children(self, tokens: list):
		self.children.extend(tokens)