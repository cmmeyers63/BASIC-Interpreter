from b_types import *
from collections import OrderedDict

'''
		# esentially, I want to take off the START and STMT_LIST nodes and then organize the
		# orphaned stmts into a dictionary for easy access when walking the tree
		stmt_dict = OrderedDict()
		stmts = self._root_node.children[0].children
		
		for i in range(1, len(stmts) -1, 2):
			stmt_dict[int(stmts[i-1].value)] = stmts[i]

		# sort dictionary based on line_no
		stmt_dict = OrderedDict(sorted(stmt_dict.items(), key=lambda x: x[0]))
		return stmt_dict
'''
class Memory():
    def __init__(self) -> None:
        self._symbol_table = dict()
    
    def get_symbol(self, name : str):
        if name in self._symbol_table:
            return self._symbol_table
        return None
    

    def insert_symbol(self, name : str, value):
        self._symbol_table[name] = value



class Interpreter():
    def __init__(self, stmt_list_node : Node) -> None:
        self.memory = Memory()

        self.stmt_list_node = stmt_list_node

        # I want to build a list of just the statments and store the 
        # line numbers in a seperate lookup structure
        # stmts are on odd nodes [1,3,5]
		# the line number is the preceding node
		# the last node is an EOF
        unorganized_stmts = self.stmt_list_node.children
        self.stmt_table = []
        self.program_counter = 0
        # a lookup table with key: program_line_number  value: stmts array index
        self.line_lookup_table: dict[int, int] = dict() 
        j = 0
        for i in range(1, len(unorganized_stmts) -1, 2):
            self.stmt_table.append(unorganized_stmts[i])
            self.line_lookup_table[int(unorganized_stmts[i-1].value)] = j
            j += 1

        # debug print
        #for stmt, kv in zip(self.stmt_table, self.line_lookup_table):
        #    print(stmt, kv, self.line_lookup_table[kv])
    

    # evaluates the ast the program was constructed with
    def eval_program(self):
        try:
            while True:
                stmt = self.fetch_next_stmt()
                #print("executing", stmt, stmt.children)
                self.eval_statement(stmt)

        except SystemExit:
            print("end of program")

    # a statement performes some operation which mutates the symbol table, changes the pc,
    def eval_statement(self, stmt: Node):
        match stmt.children:
            case [Node(type=TokenType('GOTO')), a_expr]:
                #print("\tEvaluating GOTO")
                line_no = self.eval_expr(a_expr)
                self.jump(line_no)
            case [Node(type=TokenType('PRINT')), *rest]:
                value = self.eval_expr(rest[1])
                print(value)
                #print(value)
            case _:
                print("\tunable to evaluate stmt")

    def jump(self, line_number):
        if line_number not in self.line_lookup_table:
            raise RuntimeError(f"No statement is defined at line={line_number}")
        self.program_counter = self.line_lookup_table[line_number]
        

    def fetch_next_stmt(self):
        if self.program_counter > len(self.line_lookup_table) -1:
            raise SystemExit()
        stmt = self.stmt_table[self.program_counter]
        self.program_counter += 1
        return stmt

    
    # an expression always returns a value
    # that value may be a string, double, or integer
    def eval_expr(self, node : Node) -> object:
        children = node.children
        
        if node.type is TokenType.A_EXPR or node.type is TokenType.B_EXPR:
            # should be some form of left op right
            if len(children) == 3:
                l_val = self.eval_expr(children[0])
                r_val = self.eval_expr(children[2])
                
                # I'm pretty sure Python's semantics for addition of strings and ints
                # is pretty much the same as BASICS, this makes things a lot easier 
                match children[1].value:
                    case '+':
                        return l_val + r_val
                    case '-':
                            # left associativity
                            return l_val - r_val
                    case '/' if r_val > 0:
                            return l_val / r_val
                    case '/':
                            raise ZeroDivisionError(f"Division by zero in {l_val}/{r_val} near line={children[1].line} col={children[1].col}")
                    case '*':
                            return l_val * r_val
                    case _:
                            raise RuntimeError(f"Fell through on {children[1].value}")
            # node with a singular child, just need get the value of the child
            elif len(children) == 1:
                return self.eval_expr(children[0])
            else:
                raise RuntimeError("eval A_EXPR or B_EXPR fell through")
        # I_EXPRs may hold values, simple expressions that can be evluated without recursion
        # or a nested A_EXPR
        elif node.type is TokenType.I_EXPR:     
            
            # (expr)
            if len(children) == 3 and \
            children[0].type is TokenType.L_PAREN and children[2].type is TokenType.R_PAREN:
                return self.eval_expr(children[1])
            # value
            elif len(children) == 1:
                match children[0].type:
                    case TokenType.NUMBER:
                        return int(children[0].value)
                    case TokenType.IDENT:
                        if children[0].value in self.symbol_table:
                            return self.symbol_table[children[0].value]
                        else:
                            raise RuntimeError(f"token={children[0].value} is undefined at row={children[0].line} col={children[0].col}")
                    case _:
                        return (children[0].value)
            else: 
                raise RuntimeError("eval I_EXPR fell through")
            