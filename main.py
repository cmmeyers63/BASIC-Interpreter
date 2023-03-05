import sys
import os.path
import lex
import parse
import interpreter
from b_types import *

# https://mirrors.apple2.org.za/Apple%20II%20Documentation%20Project/Software/Languages/Applesoft%20BASIC/Manuals/Applesoft%20II%20BASIC%20Programming%20Reference%20Manual.pdf
# https://www.calormen.com/jsbasic/reference.html

if __name__ == "__main__":

 

	filename = "expr.BAS"
	if not os.path.isfile(filename):
		print("first arg must be a file")
		exit(1)

	# initalize the lexer with the passed filename
	lexer = lex.Lexer(filename)

	lexer.Tokenize()

	parser = parse.Parser(lexer)

	print("begin parse")
	parser.Parse()
	print("end parse")
	print("begin graphviz")
	parser.Create_GraphViz() # creates file
	print("end graphviz")

	ast_root : Node = parser.root_node  # type: ignore
	print("begin interpret")
	comp = interpreter.Interpreter(ast_root.children[0])
	print(comp.eval_expr(ast_root.children[0]))
	print("end interpret")