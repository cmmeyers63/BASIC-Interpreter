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
	BOP			= 'BOP'
	AOP			= 'AOP'
	COMPARE 	= 'COMPARE'
	L_PAREN		= 'L_PAREN'
	R_PAREN		= 'R_PAREN'
	NEWLINE		= 'NEWLINE'
	COMMA		= 'COMMA'
	QUOTE		= 'QUOTE'

	# non terminals 
	START 		= 'START'
	STMT_LIST	= 'STMT_LIST'
	STMT		= 'STMT'
	A_EXPR		= 'A_EXPR'
	B_EXPR		= 'B_EXPR'
	I_EXPR		= 'I_EXPR'




class Node():
	# terminal symbol constructor
	# __match_args__ allows for structural pattern matching to be conducted  
	# w/ the first enum parameter TokenType specified
	__match_args__ = ("type")
	def __init__(self, type : TokenType, value: str = "", line: int = -1, col: int = -1) -> None:
		self.type = type
		self.value = value
		self.line = line
		self.col = col
		
		self.children: list[Node] = []
		self.parent = None
		self.id = 0

	def __repr__(self):
		type_without_prefix = str(self.type).split('.')[-1]
		return f"{type_without_prefix} {self.value if self.value is not None else '-'}"

	# takes either a list or a single node
	def add_children(self, nodes):
		if type(nodes) is list:
			self.children.extend(nodes)
		else:
			self.children.append(nodes)
		

	def attach_parent(self, node):
		self.parent = node