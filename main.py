import sys
import os.path
import lex

# https://mirrors.apple2.org.za/Apple%20II%20Documentation%20Project/Software/Languages/Applesoft%20BASIC/Manuals/Applesoft%20II%20BASIC%20Programming%20Reference%20Manual.pdf
# https://www.calormen.com/jsbasic/reference.html

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("usage: python calc.py [args]")
		exit(1)

	filename = sys.argv[1]
	if not os.path.isfile(filename):
		print("first arg must be a file")
		exit(1)

	# initalize the lexer with the passed filename
	lexer = lex.Lexer(filename)

	lexer.Tokenize()
	
	exit()

	# parser = parse.Parser(lexer)


	# tokens : list = lexer.lex(filename)
	# print(tokens)
	
	# parser = parse.Parser(tokens)
	# print("begin parse")
	# parser.Parse()
	# print("end parse")
	# print("begin graphviz")
	# parser.Create_GraphViz() # creates file
	# print("end graphviz")