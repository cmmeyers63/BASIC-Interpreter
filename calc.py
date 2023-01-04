import sys
from enum import Enum 
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


class Token():
	def __init__(self, tokenT : TokenType, value = None, name = None) -> None:
		self.type = tokenT
		self.value = value
		self.name = name

		self.children = []
		self.parent = None

	def __repr__(self):
		return f"{self.type} {self.value if self.value is not None else '-'} {self.name if self.name is not None else '-'}"

	def add_child(self, token):
		self.children.append(token)

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
		return Token(TokenType.VARIABLE, name=str_token)
	
	raise ValueError(f"Unexpected token : {str_token}")


def lex():
	user_in = input("enter expression: ").rstrip().split(' ')
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

	START -> A_EXPR 
	
	A_EXPR -> I_EXPR (+ | -) A_EXPR
		| I_EXPR 
		| I_EXPR (+ | -) B_EXPR
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

	def _pop_tokens(self, token_list : list):
		for tok in token_list:
			self.tokens.remove(tok)
				
	def Parse(self):
		self.START()

	# S -> A_EXPR ;
	def START(self) -> Token:
		current_node = Token(TokenType.START)
		self.A_EXPR(current_node)

		self.root_node = current_node
		

	def A_EXPR(self, parent_node : Token):
		# non terminals make their own nodes
		current_node = Token(TokenType.A_EXPR)

		parent_node.add_child(current_node)

		# terminals attach themselves since they were already constructed by the lexer
		match self.tokens:
			case [a]: 
				current_node.add_child(a)
				tokens.remove(a)
				return
			case [a, b, c]:
				current_node.add_child(a)
				current_node.add_child(b)
				current_node.add_child(c)
				self._pop_tokens([a,b,c])
				return
			case [a, b, *rest]:
				current_node.add_child(a)
				current_node.add_child(b)
				self._pop_tokens([a,b])
				self.A_EXPR(current_node)
			case _:
				raise ParseError("A_EXPR fell through")


if __name__ == "__main__":
	tokens : list = lex()
	print(tokens)
	
	parser = Parser(tokens)
	print("begin parse")
	parser.Parse()
	print("end parse")