from b_types import *
from collections import deque
from collections import OrderedDict
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
				current_node : Node = Q.popleft()
				nodeId = nodeId + 1
				current_node.id = nodeId
				f.write(f'{nodeId} [label="{current_node}"];\n')
				Q.extend(current_node.children)
			
			# traverse tree and list all edges
			Q = deque()
			Q.append(self._root_node)
			while len(Q) > 0:
				current_node : Node = Q.popleft()
				for child in current_node.children:
					f.write(f"{current_node.id} -> {child.id};\n")
				Q.extend(current_node.children)

			f.write("} \n")
				
	def Parse(self) -> Node:
		# build the parse tree
		self._root_node = self.START()

		# a program in BASIC is really just a list of statments.
		# the parser will just remove the START node and return the resultant ast
		return self._root_node.children[0]



	# S -> A_EXPR ;
	def START(self) -> Node:
		current_node = Node(TokenType('START'))
		current_node.add_children(self.STMT_LIST(current_node))

		return current_node
	
	def STMT_LIST(self, parent_node : Node) -> Node:
		current_node = Node(TokenType('STMT_LIST'))
		current_node.attach_parent(parent_node)

		# Process statements untill EOF encountered
		while not self._lexer.peek(TokenType.EOF):
			if not self._lexer.peek(TokenType.NUMBER):
				raise ParseError("ERROR: line_number expected")
			
			# ex: 100 goto 5
			current_node.add_children([self._lexer.pop(), self.STMT(current_node)])

			if not self._lexer.peek(TokenType.NEWLINE):
				raise ParseError("ERROR: newline expected at end of statement")
			self._lexer.pop()

		# adding EOF
		current_node.add_children(self._lexer.pop())
		return current_node


	def STMT(self, parent_node : Node) -> Node:
		current_node = Node(TokenType('STMT'))
		current_node.attach_parent(parent_node)

		if self._lexer.peek(TokenType.GOTO):
			goto = self._lexer.pop()
			a_expr = self.A_EXPR(current_node)
			current_node.add_children([goto, a_expr])
		# identifer = A_EXPR
		elif self._lexer.peek([TokenType.IDENT, TokenType.ASSIGN]):
			identifier = self._lexer.pop()
			assign = self._lexer.pop()
			a_expr = self.A_EXPR(current_node)
			current_node.add_children([identifier, assign, a_expr])
		# if L_EXPR then goto value
		elif self._lexer.peek(TokenType.IF):
			_if = self._lexer.pop()
			l_expr = self.L_EXPR(current_node)
			if not self._lexer.peek([TokenType.THEN, TokenType.GOTO, TokenType.NUMBER]):
				raise ParseError(f"expected then goto after if L_EXPR line={_if.line}")
			then = self._lexer.pop()
			goto = self._lexer.pop()
			line_number = self._lexer.pop()
			current_node.add_children([_if, l_expr, then, goto, line_number])
		# PRINT(A_EXPR)
		elif self._lexer.peek([TokenType.PRINT, TokenType.L_PAREN]):
			_print = self._lexer.pop()
			l_paren = self._lexer.pop()
			a_expr = self.A_EXPR(current_node)
			if not self._lexer.peek([TokenType.R_PAREN]):
				raise ParseError(f"expected then r_paren to close PRINT line={l_paren.line}")
			r_paren = self._lexer.pop()
			current_node.add_children([_print, l_paren, a_expr, r_paren])
		else:
			raise ParseError(f"Unexpected thing in STMT")
		
		return current_node


	def L_EXPR(self, parent_node : Node) -> Node:
		return self.A_EXPR(parent_node)
		
	# generally:
	# consume terminals, call function for Non-terminal

	def A_EXPR(self, parent_node : Node) -> Node:
		# non terminals make their own nodes
		current_node = Node(TokenType('A_EXPR'))
		current_node.attach_parent(parent_node)

		
		b_expr = self.B_EXPR(current_node)
		current_node.add_children(b_expr)

		# + ...
		# - ... 
		if self._lexer.peek([TokenType('AOP')]):
			token = self._lexer.pop()
			current_node.add_children(token) # capture terminal
			a_expr = self.A_EXPR(current_node)
			current_node.add_children(a_expr)

			# if token.value == '-':
			# 	# flip order for correct operator precedence
			# 	current_node.children.clear()
			# 	current_node.add_children([a_expr, token, b_expr])


		return current_node


	def B_EXPR(self, parent_node : Node) -> Node:
		# non terminals make their own nodes
		current_node = Node(TokenType('B_EXPR'))
		current_node.attach_parent(parent_node)

		
		i_expr = self.I_EXPR(current_node)
		current_node.add_children([i_expr])

		# / ...
		# * ... 
		if self._lexer.peek([TokenType('BOP')]):
			token = self._lexer.pop()

			
			current_node.add_children(token) # capture terminal
			a_expr = self.A_EXPR(current_node)
			current_node.add_children(a_expr)

			# if token.value == '/':
			# 	# flip order for correct operator precedence
			# 	current_node.children.clear()
			# 	current_node.add_children([a_expr, token, i_expr])

		return current_node


	def I_EXPR(self, parent_node : Node) -> Node:
		current_node = Node(TokenType('I_EXPR'))
		current_node.attach_parent(parent_node)

		# number or variable
		if self._lexer.peek(TokenType.IDENT) or self._lexer.peek(TokenType.NUMBER):
			current_node.add_children(self._lexer.pop())
		# ( A_EXPR )
		elif self._lexer.peek([TokenType.L_PAREN]):
			# consume both L_PAREN and A_EXPR
			current_node.add_children([self._lexer.pop(), self.A_EXPR(current_node)])
			if (self._lexer.peek([TokenType.R_PAREN])):
				current_node.add_children(self._lexer.pop())
			else:
				raise ParseError("No match to L_PAREN")
		else:
			raise ParseError(f"Unexpected tokens in I_EXPR")

		return current_node
