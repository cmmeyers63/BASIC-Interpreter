from b_types import *
from collections import deque
from lex import *

class ParseError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)


class Parser():
	def __init__(self, lexer : Lexer) -> None:
		self._root_node = None
		self._lexer = lexer


	# https://www.graphviz.org/pdf/dotguide.pdf
	def Create_GraphViz(self):
		# visualize with : dot -Tpdf parse.dot > parse.pdf
		with open('parse.dot', 'w') as f:
			f.write("digraph G { \n")
			
			nodeId = 0
			# traverse tree and list all nodes
			Q = deque()
			self._root_node.id = nodeId
			Q.append(self._root_node)
			while len(Q) > 0:
				current_node : Token = Q.pop()
				nodeId = nodeId + 1
				current_node.id = nodeId
				f.write(f'{nodeId} [label="{current_node}"];\n')
				Q.extend(current_node.children)
			
			# traverse tree and list all edges
			Q = deque()
			Q.append(self._root_node)
			while len(Q) > 0:
				current_node : Token = Q.pop()
				for child in current_node.children:
					f.write(f"{current_node.id} -> {child.id};\n")
				Q.extend(current_node.children)

			f.write("} \n")
				
	def Parse(self):
		self._root_node = self.START()

	# S -> A_EXPR ;
	def START(self) -> Node:
		current_node = Node(TokenType.START)
		current_node.add_children(self.A_EXPR(current_node))

		return current_node
		
	# generally:
	# consume terminals, call function for Non-terminal

	def A_EXPR(self, parent_node : Node) -> Node:
		# non terminals make their own nodes
		current_node = Node(TokenType.A_EXPR)
		current_node.attach_parent(parent_node)

		
		b_expr = self.B_EXPR(current_node)

		# + ...
		# - ... 
		if self._lexer.peek(TokenType.OP):
			current_node.add_children([self._lexer.pop()]) # capture terminal
			self.A_EXPR(current_node)


	def B_EXPR(self, parent_node : Token):
		current_node = Token(TokenType.B_EXPR)
		parent_node.add_children([current_node])
		
		self.I_EXPR(current_node)

		if self._peek([TokenType.TIMES] or self._peek([TokenType.DIVIDE])):
			current_node.add_children([self.tokens.pop(0)])
			self.B_EXPR(current_node)


	def I_EXPR(self, parent_node : Token):
		current_node = Token(TokenType.I_EXPR)
		parent_node.add_children([current_node])

		# 5 ** 2
		if self._peek([TokenType.VALUE, TokenType.POW, TokenType.VALUE]):
			current_node.add_children([self.tokens.pop(0), self.tokens.pop(0), self.tokens.pop(0)])
		# -(5)
		elif self._peek([TokenType.MINUS, TokenType.L_PAREN]):
			# -(
			current_node.add_children([self.tokens.pop(0), self.tokens.pop(0)])
			self.A_EXPR(current_node) 
			# )
			current_node.add_children([self.tokens.pop(0)])
		elif self._peek([TokenType.L_PAREN]):
			# (
			current_node.add_children([self.tokens.pop(0)])
			self.A_EXPR(current_node)
			# ) 
			current_node.add_children([self.tokens.pop(0)])
		# 5
		elif self._peek([TokenType.VALUE]):
			current_node.add_children([self.tokens.pop(0)])
		else:
			raise ParseError(f"Unexpected tokens in I_EXPR {self.tokens}")
