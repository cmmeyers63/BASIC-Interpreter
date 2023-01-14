from enum import StrEnum, unique, auto

@unique
class TokenType(StrEnum):
	# keywords
	GOTO 		= 'GOTO'
	END 		= 'END'
	IF			= 'IF'
	THEN		= 'THEN'
	PRINT		= 'PRINT'
	LET			= 'LET'
	REM			= 'REM'
	TO			= 'TO'
	NEXT		= 'NEXT'
	EOL			= 'EOL'
	EOF			= 'EOF'
	DIM			= 'DIM'
	
	# re keywords
	NUMBER 		= 'NUMBER'
	ASSIGN		= 'ASSIGN'
	IDENT		= 'IDENT'
	OP			= 'OP'
	COMPARE 	= 'COMPARE'
	L_PAREN		= 'L_PAREN'
	R_PAREN		= 'R_PAREN'
	NEWLINE		= 'NEWLINE'
	COMMA		= 'COMMA'
	QUOTE		= 'QUOTE'



class Node():
	# terminal symbol constructor
	def __init__(self, type : TokenType, value: str = "", line: int = -1, col: int = -1) -> None:
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