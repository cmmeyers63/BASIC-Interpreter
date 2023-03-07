import sys
import os.path
from collections import OrderedDict
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
	try:
		lexer = lex.Lexer(filename)
		lexer.Tokenize()
	except Exception as ex:
		print(f"[ERROR] lex failed")
		raise ex
	try:
		parser = parse.Parser(lexer)
		parse_tree = parser.Parse()
		# creates a .dot file based on the original parse_tree. This may be slightly different than
		# the stmt_dict which is returned
		parser.Create_GraphViz() 
	except Exception as ex:
		print(f"[ERROR] parse failed")
		raise ex
	try:
		comp = interpreter.Interpreter(parse_tree)
		comp.eval_program()
	except Exception as ex:
		print(f"[ERROR] interpret failed")
		raise ex