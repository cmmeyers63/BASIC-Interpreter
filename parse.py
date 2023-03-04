from b_types import *
from collections import deque
from lex import *

class ParseError(Exception):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)


class Parser():
	def __init__(self, lexer : Lexer) -> None:
		self.root_node = None
		self._lexer = lexer


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
				current_node : Node = Q.pop()
				nodeId = nodeId + 1
				current_node.id = nodeId
				f.write(f'{nodeId} [label="{current_node}"];\n')
				Q.extend(current_node.children)
			
			# traverse tree and list all edges
			Q = deque()
			Q.append(self.root_node)
			while len(Q) > 0:
				current_node : Node = Q.pop()
				for child in current_node.children:
					f.write(f"{current_node.id} -> {child.id};\n")
				Q.extend(current_node.children)

			f.write("} \n")
				
	def Parse(self):
		self.root_node = self.START()
		print(self.root_node)

	# S -> A_EXPR ;
	def START(self) -> Node:
		current_node = Node(TokenType('START'))
		current_node.add_children([self.A_EXPR(current_node)])

		return current_node
		
	# generally:
	# consume terminals, call function for Non-terminal

	def A_EXPR(self, parent_node : Node) -> Node:
		# non terminals make their own nodes
		current_node = Node(TokenType('A_EXPR'))
		current_node.attach_parent(parent_node)

		
		b_expr = self.B_EXPR(current_node)
		current_node.add_children([b_expr])

		# + ...
		# - ... 
		if self._lexer.peek_n([TokenType('AOP')]):
			token = self._lexer.pop()
			current_node.add_children([token]) # capture terminal
			a_expr = self.A_EXPR(current_node)
			current_node.add_children([a_expr])

			if token.value == '-':
				# flip order for correct operator precedence
				current_node.children.clear()
				current_node.add_children([a_expr, token, b_expr])


		return current_node


	def B_EXPR(self, parent_node : Node) -> Node:
		# non terminals make their own nodes
		current_node = Node(TokenType('B_EXPR'))
		current_node.attach_parent(parent_node)

		
		i_expr = self.I_EXPR(current_node)
		current_node.add_children([i_expr])

		# / ...
		# * ... 
		if self._lexer.peek_n([TokenType('BOP')]):
			token = self._lexer.pop()

			
			current_node.add_children([token]) # capture terminal
			a_expr = self.A_EXPR(current_node)
			current_node.add_children([a_expr])

			if token.value == '/':
				# flip order for correct operator precedence
				current_node.children.clear()
				current_node.add_children([a_expr, token, i_expr])

		return current_node


	def I_EXPR(self, parent_node : Node) -> Node:
		current_node = Node(TokenType('I_EXPR'))
		current_node.attach_parent(parent_node)

		# number
		if self._lexer.peek_n([TokenType.NUMBER]):
			current_node.add_children([self._lexer.pop()])
		# ( A_EXPR )
		elif self._lexer.peek_n([TokenType.L_PAREN]):
			# consume both L_PAREN and A_EXPR
			current_node.add_children([self._lexer.pop(), self.A_EXPR(current_node)])
			if (self._lexer.peek_n([TokenType.R_PAREN])):
				current_node.add_children([self._lexer.pop()])
			else:
				raise RuntimeError("No match to L_PAREN")

		# elif self._lexer.peek_n([TokenType.L_PAREN]):
		# 	current_node.add_children([self._lexer.pop()])
		else:
			raise ParseError(f"Unexpected tokens in I_EXPR")

		return current_node
