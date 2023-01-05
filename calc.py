import sys
from enum import Enum 
from collections import deque
import re

class ParseError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)

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
	VARIABLE = 8
	END_OF_STMT = 9
	POW = 12

	# non-terminals
	START = 10
	A_EXPR = 11
	I_EXPR = 13
	B_EXPR = 14


class Token():
	def __init__(self, tokenT : TokenType, value = None) -> None:
		self.type = tokenT
		self.value = value

		self.children = []
		self.parent = None
		self.id = 0

	def __repr__(self):
		type_without_prefix = str(self.type).split('.')[-1]
		return f"{type_without_prefix} {self.value if self.value is not None else '-'}"

	def add_children(self, tokens: list):
		self.children.extend(tokens)

def build_token(str_token):
	# simple terminals
	match str_token:
		case '(':
			return Token(TokenType.L_PAREN)
		case ')':
			return Token(TokenType.R_PAREN)
		case '=':
			return Token(TokenType.EQUALS)
		case '+':
			return Token(TokenType.PLUS)
		case '-':
			return Token(TokenType.MINUS)
		case '*':
			return Token(TokenType.TIMES)
		case '/':
			return Token(TokenType.DIVIDE)
		case ';':
			return Token(TokenType.END_OF_STMT)
		case '**':
			return Token(TokenType.POW) 
		
	# integer test
	match = re.compile("\d").match(str_token)
	if match is not None:
		return Token(TokenType.VALUE, value=int(str_token))
	
	match = re.compile("^[a-zA-Z]+$").match(str_token)
	if match is not None:
		return Token(TokenType.VARIABLE, value=str_token)
	
	raise ValueError(f"Unexpected token : {str_token}")


def lex(user_in : list):
	user_in = [x for x in user_in if x != "" or x != " "]

	print(f"start build token")
	tokens = []
	for char in user_in:
		print(f"\t in : {char}")
		token = build_token(char)
		print(f"\t out: {token}")
		tokens.append(token)
	print("end build token")
	return tokens

"""
Grammer: 
	https://www.usna.edu/Users/cs/wcbrown/courses/F20SI413/lec/l10/lec.html
	https://www.usna.edu/Users/cs/wcbrown/courses/F20SI413/firstFollowPredict/ffp.html

	START -> A_EXPR $
	
	A_EXPR -> I_EXPR (+ | -) A_EXPR
		| I_EXPR 
		| B_EXPR (* | /) A_EXPR
		| B_EXPR

	B_EXPR -> I_EXPR (* | /) B_EXPR
		| I_EXPR

	I_EXPR -> value ** value
		| value
		| -(I_EXPR) | (A_EXPR)

	division and subtraction will need to be unrolled during SDT to produce the correct operator associativity
"""

class Parser():
	def __init__(self, tokens : list[Token]) -> None:
		self.root_node = None
		self.tokens = tokens

	def _pop_tokens(self, token_list : list) -> None:
		for tok in token_list:
			self.tokens.remove(tok)


	def _peek(self, token_type_list : list[TokenType]) -> bool:
		if len(self.tokens) < len(token_type_list):
			return False 

		for i, token_t in enumerate(token_type_list):
			if self.tokens[i].type != token_t:
				return False

		return True

	# https://www.graphviz.org/pdf/dotguide.pdf
	def Create_GraphViz(self):
		# visualize with : dot -Tpdf parse.dot > parse.pdf
		with open('parse.dot', 'w') as f:
			f.write("digraph G { \n")
			
			nodeId = 0
			# traverse tree and list all nodes
			Q = deque()
			self.root_node.id = nodeId
			Q.append(self.root_node)
			while len(Q) > 0:
				current_node : Token = Q.pop()
				nodeId = nodeId + 1
				current_node.id = nodeId
				f.write(f'{nodeId} [label="{current_node}"];\n')
				Q.extend(current_node.children)
			
			# traverse tree and list all connections
			Q = deque()
			Q.append(self.root_node)
			while len(Q) > 0:
				current_node : Token = Q.pop()
				for child in current_node.children:
					f.write(f"{current_node.id} -> {child.id};\n")
				Q.extend(current_node.children)

			f.write("} \n")
				
	def Parse(self):
		self.START()

	# S -> A_EXPR ;
	def START(self) -> Token:
		current_node = Token(TokenType.START)
		self.root_node = current_node
		self.A_EXPR(current_node)
		
	# generally:
	# consume terminals, call function for Non-terminal

	def A_EXPR(self, parent_node : Token):
		# non terminals make their own nodes
		current_node = Token(TokenType.A_EXPR)
		parent_node.add_children([current_node])
		
		# 5 + ...
		# 5 - ...
		if self._peek([TokenType.VALUE, TokenType.PLUS]) or self._peek([TokenType.VALUE, TokenType.MINUS]):
			self.I_EXPR(current_node)
			current_node.add_children([tokens.pop(0)]) # the plus
			self.A_EXPR(current_node)
		# 5
		elif self._peek([TokenType.VALUE]):
			self.I_EXPR(current_node)
		else:
			raise ParseError(f"Unexpected tokens in A_EXPR {tokens}")

	def B_EXPR(self, parent_node : Token):
		pass

	def I_EXPR(self, parent_node : Token):
		current_node = Token(TokenType.I_EXPR)
		parent_node.add_children([current_node])

		# 5 ** 2
		if self._peek([TokenType.VALUE, TokenType.POW, TokenType.VALUE]):
			current_node.add_children([tokens.pop(0), tokens.pop(0), tokens.pop(0)])
		# 5
		elif self._peek([TokenType.VALUE]):
			current_node.add_children([tokens.pop(0)])
		else:
			raise ParseError(f"Unexpected tokens in I_EXPR {tokens}")



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("usage python calc.py [expression]")
		exit(-1)

	print("aruments",sys.argv)

	tokens : list = lex(sys.argv[1].split(' '))
	print(tokens)
	
	parser = Parser(tokens)
	print("begin parse")
	parser.Parse()
	print("end parse")
	print("begin graphviz")
	parser.Create_GraphViz() # creates file
	print("end graphviz")